from collections import defaultdict
import typing

from worlds.crosscode.types.condition import Condition

from .codegen.ast import AstGenerator
from .codegen.lists import ListInfo
from .codegen.parse import JsonParser
from .codegen.context import Context
from .codegen.util import BASE_ID
from .codegen.merge import merge

from .types.items import ItemData
from .types.locations import AccessInfo, LocationData
from .types.regions import RegionsData
from .types.world import WorldData

from .items import items_dict, single_items_dict
from .locations import locations_dict, events_dict

class WorldBuilder:
    ctx: Context
    ast_generator: AstGenerator
    json_parser: JsonParser

    variable_definitions: dict[str, dict[str, list[Condition]]]

    lists: ListInfo

    region_packs: dict[str, RegionsData]
    locations_access: dict[str, tuple[LocationData, AccessInfo]]
    events_access: dict[str, tuple[LocationData, AccessInfo]]
    shops_access: dict[str, tuple[LocationData, AccessInfo]]
    items_dict: dict[tuple[str, int], tuple[ItemData, dict[str, int]]]

    num_needed_items: dict[str,int]
    keyring_items: set[str]

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.ast_generator = AstGenerator()
        self.json_parser = JsonParser(self.ctx)

        self.variable_definitions = defaultdict(dict)

        self.lists = ListInfo(self.ctx)
        self.lists.events_data = events_dict
        self.lists.locations_data = locations_dict
        self.lists.single_items_dict = single_items_dict

        self.json_parser.single_items_dict = single_items_dict
        self.json_parser.items_dict = items_dict

        self.region_packs = {}
        self.locations_access = {}
        self.events_access = {}
        self.shops_access = {}
        self.items_dict = {}

    def __add_reward(self, raw_loc: dict[str, typing.Any], prefix: str | None = None):
        for reward in raw_loc["reward"]:
            item = self.json_parser.parse_reward(reward) 
            key = (item.name, item.amount)
            if key in self.items_dict:
                item, quantity = self.items_dict[key]
            else:
                quantity = defaultdict(lambda: 0)
                self.items_dict[key] = (item, quantity)

            for mode in raw_loc["region"].keys():
                true_mode = mode if prefix is None else f"{prefix}_{mode}"
                quantity[true_mode] += 1

    def __add_location(self, name: str, raw_loc: dict[str, typing.Any], create_event=False):
        num_rewards = 1
        if "reward" in raw_loc:
            if len(raw_loc["reward"]) == 0:
                raise RuntimeError(f"Error while adding location {name}: need one or more rewards (get rid of the entry if there are no rewards)")
            num_rewards = len(raw_loc["reward"])

        access_info = self.json_parser.parse_location_access_info(raw_loc)

        for idx in range(num_rewards):
            full_name = name
            if num_rewards > 1:
                full_name = full_name + f" - Reward {idx + 1}"

            self.locations_access[full_name] = (locations_dict[full_name], access_info)

        if access_info is not None and (num_rewards > 1 or create_event):
            event = events_dict[f"{name} (Event)"]
            self.events_access[name] = (event, access_info)

        if "reward" not in raw_loc or len(raw_loc["reward"]) == 0:
            for mode in raw_loc["region"].keys():
                self.num_needed_items[mode] += 1
            return

        self.__add_reward(raw_loc)

    def __add_location_list(self, loc_list: dict[str, dict[str, typing.Any]], create_events=False):
        for name, raw_loc in loc_list.items():
            self.__add_location(name, raw_loc, create_events)

    def __add_shop(self, shop_display_name: str, raw_shop: dict[str, typing.Any]):
        access_info = self.json_parser.parse_location_access_info(raw_shop)

        self.__add_reward(raw_shop, "shop")

        ids = set()

        for reward in raw_shop["reward"]:
            item = self.json_parser.parse_reward(reward) 

            item_data = self.ctx.rando_data["items"][item.name]

            if item_data["id"] in ids:
                continue

            ids.add(item_data["id"])

            full_name = f"{shop_display_name} - {item.name} Slot"

            self.shops_access[full_name] = (locations_dict[full_name], access_info)

    def __add_shop_list(self, loc_list: dict[str, dict[str, typing.Any]]):
        for name, raw_shop in loc_list.items():
            self.__add_shop(name, raw_shop)

    def __add_vars(self, variables: dict[str, dict[str, list[typing.Any]]]):
        for name, values in variables.items():
            for value, conds in values.items():
                self.variable_definitions[name][value] = self.json_parser.parse_condition(conds)

    def build(self, addons: list[str]) -> WorldData:
        for name in addons:
            self.ctx.rando_data = merge(self.ctx.rando_data, self.ctx.addons[name])

        self.region_packs = self.json_parser.parse_regions_data_list(self.ctx.rando_data["regions"])

        self.num_needed_items = {mode: 0 for mode in self.region_packs}
        
        self.__add_vars(self.ctx.rando_data["vars"])

        self.__add_location_list(self.ctx.rando_data["chests"])
        self.__add_location_list(self.ctx.rando_data["cutscenes"])
        self.__add_location_list(self.ctx.rando_data["elements"])
        self.__add_location_list(self.ctx.rando_data["quests"], True)
        self.__add_shop_list(self.ctx.rando_data["shops"])

        self.keyring_items = set(self.ctx.rando_data["keyringItems"])

        for (data, quantities) in self.items_dict.values():
            try:
                max_quantities = self.ctx.rando_data["items"][data.item.name]["maxQuantity"]
            except KeyError:
                continue

            for mode, quantity in quantities.items():
                new_quantity = min(quantity, max_quantities[mode])
                self.num_needed_items[mode] += quantity - new_quantity
                quantities[mode] = new_quantity

        return WorldData(
            region_packs=self.region_packs,
            locations_data=self.locations_access,
            events_data=self.events_access,
            shops_data=self.shops_access,
            num_needed_items=self.num_needed_items,
            items_dict=self.items_dict,
            keyring_items=self.keyring_items,
            variable_definitions=self.variable_definitions
        )
