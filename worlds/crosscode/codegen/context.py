from dataclasses import dataclass, field
import typing

from .util import get_json_object, load_json_with_includes


@dataclass
class Context:
    rando_data: dict[str, typing.Any]
    item_data: list[typing.Dict[str, typing.Any]]
    database: dict[str, typing.Any]
    num_items: int = field(init=False)

    def __post_init__(self):
        self.num_items = len(self.item_data)


def make_context_from_package(package, with_assets=True) -> Context:
    master = load_json_with_includes(package, "data/in/master.json")
    if with_assets:
        return Context(
            master,
            get_json_object(package, "data/assets/data/item-database.json")["items"],
            get_json_object(package, "data/assets/data/database.json")
        )

    else:
        return Context(
            master,
            [],
            {}
        )
