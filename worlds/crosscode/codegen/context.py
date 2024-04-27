import typing
import os
import json

from .util import get_json_object, load_json_with_includes, load_world_json


class Context:
    rando_data: dict[str, typing.Any]
    addons: dict[str, dict[str, typing.Any]]
    item_data: list[typing.Dict[str, typing.Any]]
    database: dict[str, typing.Any]
    cached_location_ids: dict[str, int]
    num_items: int

    def __init__(self, rando_data, addons, cached_location_ids, item_data, database):
        self.rando_data = rando_data
        self.addons = addons
        self.item_data = item_data
        self.database = database
        self.cached_location_ids = cached_location_ids
        self.num_items = len(self.item_data)


def make_context_from_package(package, with_assets=True) -> Context:
    master, addons = load_world_json(package, "data/in/master.json")

    cached_location_ids = {}
    try:
        with open("data/out/locations.json") as f:
            cached_location_ids = json.load(f)
    except:
        pass

    if with_assets:
        return Context(
            master,
            addons,
            cached_location_ids,
            get_json_object(package, "data/assets/data/item-database.json")["items"],
            get_json_object(package, "data/assets/data/database.json")
        )
    else:
        return Context(
            master,
            addons,
            cached_location_ids,
            [],
            {}
        )
