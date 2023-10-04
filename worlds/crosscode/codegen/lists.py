import typing

from .ast import AstGenerator
from .parse import JsonParser
from .context import Context
from .util import BASE_ID

from ..types.Items import ItemData
from ..types.Locations import LocationData


class ListInfo:
    ctx: Context
    ast_generator: AstGenerator
    json_parser: JsonParser
    current_location_code: int = BASE_ID

    locations_data: dict[str, LocationData]
    events_data: dict[str, LocationData]
    
    items_dict: dict[tuple[str, int], ItemData]

    reward_amounts: dict[str, int]

    def __init__(self, ctx: Context):
        self.ctx = ctx

        self.ast_generator = AstGenerator()
        self.json_parser = JsonParser(self.ctx)

        self.locations_data = {}
        self.events_data = {}

        self.items_dict = {}
        
        self.reward_amounts = {}

        for file in [self.ctx.rando_data, *self.ctx.addons.values()]:
            if "chests" in file: self.__add_location_list(file["chests"])
            if "cutscenes" in file: self.__add_location_list(file["cutscenes"])
            if "elements" in file: self.__add_location_list(file["elements"])
            if "quests" in file: self.__add_location_list(file["quests"], True)

    def __add_location(self, name: str, raw_loc: dict[str, typing.Any], create_event=False):
        num_rewards = 1
        found = False
        if "reward" in raw_loc:
            if len(raw_loc["reward"]) == 0:
                raise RuntimeError(f"Error while adding location {name}: need one or more rewards (get rid of the entry if there are no rewards)")
            num_rewards = len(raw_loc["reward"])

        if name in self.reward_amounts:
            if num_rewards != self.reward_amounts[name]:
                found = True
                num_rewards = 0
                raise RuntimeError(f"Location of name '{name}' already exists with {self.reward_amounts[name]} rewards. Cannot add or overwrite with {num_rewards}.")

        location_names: list[str] = []

        for idx in range(num_rewards):
            full_name = name
            if num_rewards > 1:
                full_name = full_name + f" - Reward {idx + 1}"

            location_names.append(full_name)

            loc = LocationData(name, self.current_location_code)
            self.current_location_code += 1

            self.locations_data[name] = loc

        if not found and (num_rewards > 1 or create_event):
            event_name = f"{name} (Event)"
            event = LocationData(
                name=f"{name} (Event)",
                code=None
            )
            self.events_data[event_name] = event

        if "reward" in raw_loc:
            for reward in raw_loc["reward"]:
                item = self.json_parser.parse_reward(reward) 
                key = (item.name, item.amount)
                if key in self.items_dict:
                    item = self.items_dict[key]
                elif key not in self.items_dict:
                    self.items_dict[key] = item

    def __add_location_list(self, loc_list: dict[str, dict[str, typing.Any]], create_events=False):
            for name, raw_loc in loc_list.items():
                self.__add_location(name, raw_loc, create_events)
