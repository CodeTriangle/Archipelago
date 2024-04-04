import json
import os
import typing
import pkgutil

from BaseClasses import ItemClassification

from .merge import merge

BASE_ID = 3235824000

# I reserve some item IDs at the beginning of our slot for elements
# and other items that don't map to CrossCode items
RESERVED_ITEM_IDS = 100

NUM_ITEMS = 676

SP_UPGRADE_ID_OFFSET = 4
SP_UPGRADE_NAME = "SP Upgrade"

CIRCUIT_OVERRIDE = 428

GENERATED_COMMENT = """WARNING: THIS FILE HAS BEEN GENERATED!
Modifications to this file will not be kept.
If you need to change something here, check out codegen.py and the templates directory.
"""

K = typing.TypeVar("K")
V = typing.TypeVar("V")

class keydefaultdict(dict[K, V]):
    default_factory: typing.Callable[[K], V] | None
    def __init__(self, default_factory, *args, **kwargs):
        self.default_factory = default_factory
        super(dict, self).__init__(*args, **kwargs)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def get_json_object(package, filename: str):
    return json.loads(pkgutil.get_data(package, filename).decode())


def load_json_with_includes(package, filename: str, patch: bool = False) -> typing.Dict[str, typing.Any]:
    master = get_json_object(package, filename)
    dirname = os.path.dirname(filename)

    if "_comment" in master:
        master.pop("_comment")

    if not isinstance(master, dict):
        raise RuntimeError(f"error loading file '{filename}': root should be an object")
    if "_includes" not in master:
        return master

    includes = master.pop("_includes")
    for subfilename in includes:
        subfile = load_json_with_includes(package, os.path.join(dirname, subfilename), patch)

        if "_global" in subfile:
            diff = subfile.pop("_global")
            subfile = merge(subfile, diff, patch=True)

        master = merge(master, subfile, patch=False)

    return master


def get_item_classification(item: dict) -> ItemClassification:
    """Deduce the classification of an item based on its item-database entry"""
    if item["type"] == "CONS" or item["type"] == "TRADE": return ItemClassification.filler
    elif item["type"] == "KEY":
        return ItemClassification.progression
    elif item["type"] == "EQUIP":
        return ItemClassification.useful
    elif item["type"] == "TOGGLE":
        if "Booster" in item["name"]["en_US"]:
            return ItemClassification.progression
        else:
            return ItemClassification.filler
    else:
        raise RuntimeError(f"I don't know how to classify this item: {item['name']}")
