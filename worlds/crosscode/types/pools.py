from collections import defaultdict

from .metadata import IncludeOptions
from .locations import LocationData
from .items import ItemData
from ..item_pools import item_pools
from ..locations import locations_data

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
    location_pool: set[LocationData]
    item_pools: dict[str, dict[ItemData, int]]

    def __init__(self, opts: IncludeOptions):
        self.location_pool = set()
        self.item_pools = {}

        for loc in locations_data:
            # Technically the class allows metadata to be None.
            # So we'll assign a local variable and use that instead.
            metadata = loc.metadata if loc.metadata is not None else {}

            # This is where we check the item conditions.
            # These are manually coded for now.
            # The default is to include the item.
            # Continue the loop if it should instead not be included.
            if not metadata.get("questRandoOnly", True):
                continue

            self.location_pool.add(loc)

        for name, pool in item_pools.items():
            counter = defaultdict(lambda: 0)
            for entry in pool:
                # See the comments for the location data for the structure of
                # this session.
                metadata = entry.metadata if entry.metadata is not None else {}

                if not metadata.get("keyrings", True):
                    continue

                counter[entry.item] += entry.quantity

            self.item_pools[name] = counter
