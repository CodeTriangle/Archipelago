from collections import defaultdict
from random import Random
import itertools

from .metadata import IncludeOptions
from .locations import LocationData
from .items import ItemData, ItemPoolEntry
from .world import WorldData


ItemPool = dict[ItemData, int]


class Pools:
    """A class which stores information about item and location pools.

    A location pool represents the set of locations to include in a world.

    An item pool represents a list of items and their integer weight. This
    weight can be interpreted as a quantity if the pool is meant to be always
    included (such as with the "required" pool in the CrossCode data) or as a
    probability if the pool is to be pulled from repeatedly to fill slots
    (such as with the *Filler pools in the CrossCode data).

    There are expected to be multiple instances of Pools in the Generator.py
    runtime if there are two or more CrossCode worlds therein. Instances of
    Pools are included based on different options. In CrossCode there will be
    a separate instance of Pools when quest rando is included versus when it
    is not.
    """

    options: IncludeOptions
    location_pool: set[LocationData]
    event_pool: set[LocationData]
    item_pools: dict[str, ItemPool]
    _item_pool_lists: dict[str, tuple[list[ItemData], list[int]]]

    def __init__(self, world_data: WorldData, opts: IncludeOptions):
        self.options = opts
        self.location_pool = set()
        self.event_pool = set()
        self.item_pools = {}
        self._item_pool_lists = {}

        weights = {}

        for loc in world_data.locations_dict.values():
            if self.__should_include_location(loc):
                self.location_pool.add(loc)

        for ev in world_data.events_dict.values():
            if self.__should_include_location(ev):
                self.event_pool.add(ev)

        for name, pool in world_data.item_pools_template.items():
            counter = defaultdict(lambda: 0)
            for entry in pool:
                if self.__should_include_item(entry):
                    counter[entry.item] += entry.quantity

            self.item_pools[name] = counter

            weights[name] = list(itertools.accumulate(counter.values()))

        for name, pool in self.item_pools.items():
            self._item_pool_lists[name] = (list(pool.keys()), weights[name])

    def __should_include_location(self, loc: LocationData) -> bool:
        # Technically the class allows metadata to be None.
        # So we'll assign a local variable and use that instead.
        metadata = loc.metadata if loc.metadata is not None else {}

        # This is where we check the item conditions.
        # These are manually coded for now.
        # The default is to include the item.
        # Return false if at any point it is discovered we shouldn't.
        if metadata.get("questRandoOnly", False):
            return self.options["questRandoOnly"]

        return True

    def __should_include_item(self, entry: ItemPoolEntry) -> bool:
        # See the comments for the location data for the structure of
        # this section.
        metadata = entry.metadata if entry.metadata is not None else {}

        if not metadata.get("keyrings", True):
            return False

        return True

    def pull_items_from_pool(self, name: str, rand: Random, k=1) -> list[ItemData]:
        population, weights = self._item_pool_lists[name]
        return rand.choices(population, cum_weights=weights, k=k)
