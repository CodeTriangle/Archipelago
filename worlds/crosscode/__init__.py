from copy import copy
from collections import defaultdict
import traceback
from copy import deepcopy
import sys
import typing
from BaseClasses import ItemClassification, Location, LocationProgressType, Region, Item
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World
from worlds.crosscode.types.condition import LocationCondition
from worlds.generic.Rules import add_rule, set_rule

from .codegen.context import Context, make_context_from_package

from .common import *
from .logic import condition_satisfied, has_clearance
from .regions import region_packs

from .types.items import CrossCodeItem
from .types.locations import CrossCodeLocation
from .types.condition import Condition
from .types.world import WorldData
from .types.regions import RegionsData
from .types.metadata import IncludeOptions
from .types.pools import Pools
from .options import CrossCodeOptions, Reachability, addon_options

loaded_correctly = True

try:
    from .items import single_items_dict, items_by_full_name, keyring_items
    from .locations import locations_data, locations_dict
    from .item_pools import item_pools
    from .vars import variable_definitions

except Exception as e:
    loaded_correctly = False
    print("Failed to import items, locations, or regions, probably due to faulty code generation.", file=sys.stderr)
    traceback.print_exception(*sys.exc_info())
    print(e, file=sys.stderr)
    single_items_data = []
    single_items_dict = {}
    keyring_items = set()
    items_by_full_name = {}
    locations_data = []
    locations_dict = {}
    crosscode_options = {}
    item_pools = {}
    variable_definitions = {}

class CrossCodeWebWorld(WebWorld):
    theme="ocean"

pools_cache: dict[tuple, Pools] = {}

class CrossCodeWorld(World):
    """CrossCode is a retro-inspired 2D Action RPG set in the distant future,
    combining 16-bit SNES-style graphics with butter-smooth physics, a
    fast-paced combat system, and engaging puzzle mechanics, served with a
    gripping sci-fi story.
    """

    game = NAME
    web = CrossCodeWebWorld()

    options_dataclass = CrossCodeOptions
    options: CrossCodeOptions
    topology_present = True

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a propery.
    base_id = BASE_ID
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {
        key: value.combo_id for key, value in items_by_full_name.items()
    }

    location_name_to_id = {
        location.name: location.code for location in locations_data if location.code is not None
    }

    region_dict: dict[str, Region]
    logic_mode: str
    region_pack: RegionsData

    pre_fill_specific_dungeons_names: dict[str, set[str]]
    pre_fill_any_dungeon_names: set[str]

    pre_fill_specific_dungeons: dict[str, list[CrossCodeItem]]
    pre_fill_any_dungeon: list[CrossCodeItem]

    dungeon_location_list: dict[str, set[CrossCodeLocation]]
    dungeon_areas = {"cold-dng", "heat-dng", "shock-dng", "wave-dng", "tree-dng"}

    location_events: dict[str, Location]

    variables: dict[str, list[str]]

    pools: Pools

    def get_include_options(self) -> IncludeOptions:
        """The metadata dict is a dict that will be matched against the
        `metadata` fields in the ItemPoolEntry and Location classes to check
        for inclusion.
        """
        return {
            "questRandoOnly": bool(self.options.quest_rando.value),
            "keyrings": bool(self.options.keyrings.value),
        }

    def create_location(self, location: str, event_from_location=False) -> CrossCodeLocation:
        data = locations_dict[location]
        return CrossCodeLocation(self.player, data, self.logic_mode, self.region_dict, event_from_location=event_from_location)

    def create_item(self, item: str) -> CrossCodeItem:
        return CrossCodeItem(self.player, items_by_full_name[item])

    def create_event_conditions(self, condition: typing.Optional[list[Condition]]):
        if condition is None:
            return

        for c in condition:
            if isinstance(c, LocationCondition):
                name = c.location_name
                location = self.create_location(name, event_from_location=True)
                self.location_events[name] = location
                self.region_dict[location.region].locations.append(location)
                location.place_locked_item(Item(location.name, ItemClassification.progression, None, self.player))

    def generate_early(self):
        if not loaded_correctly:
            raise RuntimeError("Attempting to generate a CrossCode World after unsuccessful code generation")

        self.include_options = self.get_include_options()

        include_options_tuple = tuple(self.include_options.items())

        if include_options_tuple in pools_cache:
            self.pools = pools_cache[include_options_tuple]
        else:
            pools_cache[include_options_tuple] = self.pools = Pools(self.include_options)

        self.variables = defaultdict(list)

        start_inventory = self.options.start_inventory.value
        self.logic_mode = self.options.logic_mode.current_key
        self.region_pack = region_packs[self.logic_mode]

        if self.options.vt_shade_lock.value in [1, 2]:
            self.variables["vtShadeLock"].append("shades")
        if self.options.vt_shade_lock.value in (1, 3):
            self.variables["vtShadeLock"].append("bosses")
        if self.options.vw_meteor_passage.value:
            self.variables["vwPassage"].append("meteor")

        if self.options.start_with_green_leaf_shade.value:
            start_inventory["Green Leaf Shade"] = 1

        if self.options.start_with_chest_detector.value:
            start_inventory["Chest Detector"] = 1

        self.pre_fill_any_dungeon_names = set()
        self.pre_fill_specific_dungeons_names = defaultdict(set)

        self.pre_fill_any_dungeon = []
        self.pre_fill_specific_dungeons = defaultdict(list)
        
        self.dungeon_location_list = defaultdict(set)

        local_items = self.multiworld.local_items[self.player].value
        non_local_items = self.multiworld.non_local_items[self.player].value

        for key in ("shade_shuffle", "element_shuffle", "small_key_shuffle", "master_key_shuffle", "chest_key_shuffle"):
            getattr(self.options, key).register_locality(local_items, non_local_items)

        for key in ("element_shuffle", "small_key_shuffle", "master_key_shuffle", "chest_key_shuffle"):
            getattr(self.options, key).register_pre_fill_lists(
                self.pre_fill_specific_dungeons_names,
                self.pre_fill_any_dungeon_names
            )

        self.logic_dict = {
            "mode": self.logic_mode,
            "variables": self.variables,
            "variable_definitions": variable_definitions,
            "keyrings": keyring_items,
        }

    def create_regions(self):
        self.region_dict = {name: Region(name, self.player, self.multiworld) for name in self.region_pack.region_list if name not in self.region_pack.excluded_regions}
        self.multiworld.regions.extend([val for val in self.region_dict.values()])
        self.location_events = {}

        for conn in self.region_pack.region_connections:
            self.region_dict[conn.region_from].connect(
                self.region_dict[conn.region_to],
                f"{conn.region_from} => {conn.region_to}",
                condition_satisfied(self.player, conn.cond, **self.logic_dict) if conn.cond is not None else None
            )

            self.create_event_conditions(conn.cond)

            connection_event = Location(self.player, f"{conn.region_from} => {conn.region_to} (Event)", None, self.region_dict[conn.region_from])

            connection_event.place_locked_item(Item(f"{conn.region_to} (Event)", ItemClassification.progression, None, self.player))

            self.region_dict[conn.region_from].locations.append(connection_event)

        menu_region = Region("Menu", self.player, self.multiworld)
        menu_region.add_exits({self.region_pack.starting_region: "login"})
        self.multiworld.regions.append(menu_region)

        for name, region in self.region_dict.items():
            for data in self.pools.location_pool:
                if self.logic_mode in data.access.region and data.access.region[self.logic_mode] == name:
                    location = CrossCodeLocation(self.player, data, self.logic_mode, self.region_dict)
                    if location.data.area is not None:
                        self.dungeon_location_list[location.data.area].add(location)
                    region.locations.append(location)
                    self.create_event_conditions(data.access.cond)

            for data in self.pools.event_pool:
                if self.logic_mode in data.access.region and data.access.region[self.logic_mode] == name:
                    location = CrossCodeLocation(self.player, data, self.logic_mode, self.region_dict)
                    region.locations.append(location)
                    location.place_locked_item(Item(location.data.name, ItemClassification.progression, None, self.player))

            if name in self.region_pack.excluded_regions:
                for location in region.locations:
                    location.progress_type = LocationProgressType.EXCLUDED

        # also add any event conditions referenced in any possible value of a variable
        for conds in variable_definitions.values():
            for cond in conds.values():
                self.create_event_conditions(cond)

        goal_region = self.region_dict[self.region_pack.goal_region]
        goal = Location(self.player, "The Creator", parent=goal_region)
        goal.place_locked_item(Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        goal_region.locations.append(goal)

    def create_items(self):
        exclude = self.multiworld.precollected_items[self.player][:]

        # initially, we need as many items as there are locations
        num_needed_items = len(self.pools.location_pool)

        for data, quantity in self.pools.item_pools["required"].items():
            # if the item needs to be a keyring, limit its quantity to one.
            if self.options.keyrings.value and data.item.name in keyring_items:
                quantity = 1

            for _ in range(quantity):
                # create the item
                item = CrossCodeItem(self.player, data)

                try:
                    # Check if the item is precollected.
                    # If it is, we'll need a replacement for it.
                    idx = exclude.index(item)
                    exclude.pop(idx)
                    continue
                except ValueError:
                    # If we can't find the item in the precollected list, it
                    # goes in the item pool and we need to add one less item.
                    num_needed_items -= 1

                # HOWEVER! We might not actually add the item to the pool.
                # If the item is set to be in the player's own dungeons or
                # its original dungeon, then we don't want to add it to the
                # pool after all.
                add_to_pool = True

                if item.name in self.pre_fill_any_dungeon_names:
                    self.pre_fill_any_dungeon.append(item)
                    add_to_pool = False

                for dng, names in self.pre_fill_specific_dungeons_names.items():
                    if item.name in names:
                        self.pre_fill_specific_dungeons[dng].append(item)
                        add_to_pool = False

                if add_to_pool:
                    self.multiworld.itempool.append(item)

        filler_items = self.pools.pull_items_from_pool("fillerCommon", self.random, num_needed_items)
        for data in filler_items:
            self.multiworld.itempool.append(CrossCodeItem(self.player, data))

    def set_rules(self):
        for _, region in self.region_dict.items():
            for loc in region.locations:
                if not isinstance(loc, CrossCodeLocation):
                    continue
                if loc.data.access.cond is not None:
                    add_rule(loc, condition_satisfied(self.player, loc.data.access.cond, **self.logic_dict))
                if loc.data.access.clearance != "Default":
                    add_rule(loc, has_clearance(self.player, loc.data.access.clearance))

    def pre_fill(self):
        allowed_locations_by_item: dict[Item, set[CrossCodeLocation]] = {}
        all_items_list = list(self.pre_fill_any_dungeon)
        all_locations: set[CrossCodeLocation] = set()

        for dungeon in self.dungeon_areas:
            for item in self.pre_fill_specific_dungeons[dungeon]: 
                allowed_locations_by_item[item] = self.dungeon_location_list[dungeon]

            all_items_list.extend(self.pre_fill_specific_dungeons[dungeon])
            all_locations |= self.dungeon_location_list[dungeon]

        for _, locations in self.dungeon_location_list.items():
            for location in locations:
                orig_rule = location.item_rule
                location.item_rule = lambda item, location=location, orig_rule=orig_rule: \
                    (item not in allowed_locations_by_item or location in allowed_locations_by_item[item]) and orig_rule(item)
        
        for item in self.pre_fill_any_dungeon:
            allowed_locations_by_item[item] = all_locations

        all_locations_list = list(all_locations)
        self.random.shuffle(all_locations_list)

        # Get the list of items and sort by priority
        def priority(item) -> int:
            # 0 - Master dungeon-specific
            # 1 - Element dungeon-specific
            # 2 - Key dungeon-specific
            # 3 - Other dungeon-specific
            # 4 - Master any local dungeon
            # 5 - Element any local dungeon
            # 6 - Key any local dungeon
            # 7 - Other any local dungeon
            i = 3
            if item.name in ("Heat", "Cold", "Shock", "Wave"):
                i = 0
            if "Master" in item.name:
                i = 1
            elif "Key" in item.name:
                i = 2
            if allowed_locations_by_item[item] is all_locations:
                i += 4
            return i
        all_items_list.sort(key=priority)

        # Set up state
        all_state = self.multiworld.get_all_state(use_cache=False)
        # Remove dungeon items we are about to put in from the state so that we don't double count
        for item in all_items_list:
            all_state.remove(item)

        print(f"master_key_shuffle: {self.options.master_key_shuffle}")
        print(f"small_key_shuffle: {self.options.small_key_shuffle}")
        print(f"element_shuffle: {self.options.element_shuffle}")
        print(f"chest_key_shuffle: {self.options.chest_key_shuffle}")

        # Finally, fill!
        fill_restrictive(
            self.multiworld,
            all_state,
            all_locations_list,
            all_items_list,
            lock=True,
            single_player_placement=True,
            allow_partial=False,
            on_place=lambda loc: print(f"{self.player}: {loc.name} <- {loc.item.name}")
        )

    def fill_slot_data(self):
        return {
            "mode": self.logic_mode,
            "options": {
                "vtShadeLock": self.options.vt_shade_lock.value,
                "meteorPassage": self.options.vw_meteor_passage.value,
                "vtSkip": self.options.vt_skip.value,
                "keyrings": [single_items_dict[name].item_id for name in self.logic_dict["keyrings"]],
                "questRando": self.options.quest_rando.value,
                "hiddenQuestRewardMode": self.options.hidden_quest_reward_mode.current_key,
                "hiddenQuestObfuscationLevel": self.options.hidden_quest_obfuscation_level.current_key,
                "questDialogHints": self.options.quest_dialog_hints.value,
            }
        }
