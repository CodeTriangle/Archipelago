import typing
import abc
from dataclasses import dataclass, field

from BaseClasses import CollectionState
from ..options import ShopReceiveMode

from .items import ItemPoolEntry

class LogicDict(typing.TypedDict):
    mode: str
    variables: dict[str, list[str]]
    variable_definitions: dict[str, dict[str, list["Condition"]]]
    keyrings: set[str]
    item_progressive_replacements: dict[str, list[tuple[str, int]]]
    chest_clearance_levels: dict[int, str]
    shop_receive_mode: int | None
    shop_unlock_by_id: dict[int, ItemPoolEntry]
    shop_unlock_by_shop: dict[str, ItemPoolEntry]
    shop_unlock_by_shop_and_id: dict[tuple[str, int], ItemPoolEntry]
    region_botanics_amounts: dict[str, int]
    botanics_completion_amount: int

class Condition(abc.ABC):
    @abc.abstractmethod
    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        pass

@dataclass
class ItemCondition(Condition):
    item_name: str
    amount: int = 1

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        target = self.amount
        if self.item_name in args["keyrings"]:
            target = 1

        replacements = args["item_progressive_replacements"]

        if self.item_name in replacements:
            def callback(state: CollectionState) -> bool:
                for prog_item_name, quantity in replacements[self.item_name]:
                    if state.has(prog_item_name, player, quantity):
                        return True
                return  state.has(self.item_name, player, target)

            return callback

        return lambda state: state.has(self.item_name, player, target)

@dataclass
class QuestCondition(Condition):
    quest_name: str
    event_name: str = field(init=False)

    def __post_init__(self):
        self.event_name = f"{self.quest_name} (Event)"

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        return lambda state: state.has(self.event_name, player)

@dataclass
class LocationCondition(Condition):
    location_name: str
    event_name: str = field(init=False)

    def __post_init__(self):
        self.event_name = f"{self.location_name} (Event)"

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        return lambda state: state.has(self.event_name, player)

@dataclass
class RegionCondition(Condition):
    target_mode: typing.Optional[str]
    region_name: str

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        # target_mode == None means that it matches in all modes.
        # so if target_mode == None, check if we can reach that region.
        # else, if the target mode matches, also check if we can reach that region.
        # otherwise, if the target mode does not match, return true (assume that it's being ANDed with other conditions)

        mode: str = args["mode"]
        if self.target_mode is None or mode == self.target_mode:
            return lambda state: state.can_reach_region(self.region_name, player)

        return lambda _: True

@dataclass
class AnyElementCondition(Condition):
    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        return lambda state: any([
            state.has("Heat", player),
            state.has("Cold", player),
            state.has("Shock", player),
            state.has("Wave", player),
        ])

@dataclass
class OrCondition(Condition):
    subconditions: list[Condition]

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        callbacks = [x.satisfied(player, location, args) for x in self.subconditions]
        return lambda state: any(map(lambda x: x(state), callbacks))

@dataclass
class AndCondition(Condition):
    subconditions: list[Condition]

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        callbacks = [x.satisfied(player, location, args) for x in self.subconditions]
        return lambda state: all(map(lambda x: x(state), callbacks))

@dataclass
class VariableCondition(Condition):
    name: str

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        variables = args["variables"]
        variable_definitions = args["variable_definitions"]

        if self.name not in variables:
            return lambda _: True

        callbacks = sum(
            [
                [
                    x.satisfied(player, location, args)
                    for x in variable_definitions[self.name][value]
                ] for value in variables[self.name]
            ],
            start=[]
        )

        return lambda state: all(map(lambda x: x(state), callbacks))

@dataclass
class VariableEntryCondition(Condition):
    name: str
    value: str
    desired: bool

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        valid = (self.value in args["variables"][self.name]) == self.desired
        return lambda _: valid

@dataclass
class ChestKeyCondition(Condition):
    default_level: str

    clearance_items: typing.ClassVar[dict[str, str]] =  {
        "Bronze": "Thief's Key",
        "Silver": "White Key",
        "Gold": "Radiant Key",
    }

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        chest_levels = args["chest_clearance_levels"]

        if location is None:
            raise RuntimeError("An event cannot have a chest key condition")

        level: str = chest_levels.get(location, self.default_level)

        if level == "Default":
            return lambda _: True

        return lambda state: state.has(ChestKeyCondition.clearance_items[level], player)

@dataclass
class ShopSlotCondition(Condition):
    shop_name: str
    item_id: int

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        if args["shop_receive_mode"] is None:
            return lambda _: True
        if args["shop_receive_mode"] == ShopReceiveMode.option_per_item_type:
            return lambda state: state.has(args["shop_unlock_by_id"][self.item_id].item.name, player)
        if args["shop_receive_mode"] == ShopReceiveMode.option_per_shop:
            return lambda state: state.has(args["shop_unlock_by_shop"][self.shop_name].item.name, player)
        if args["shop_receive_mode"] == ShopReceiveMode.option_per_slot:
            return lambda state: state.has(args["shop_unlock_by_shop_and_id"][self.shop_name, self.item_id].item.name, player)
        return lambda _: True

@dataclass
class BotanicsCompletionCondition(Condition):
    amount: float

    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        def satisfied_internal(state: CollectionState):
            collected = sum([
                amount
                for region, amount in args["region_botanics_amounts"].items()
                if state.can_reach_region(region, player)
            ])

            return collected / args["botanics_completion_amount"] >= self.amount
        return satisfied_internal

class NeverCondition(Condition):
    def satisfied(self, player: int, location: int | None, args: LogicDict) -> typing.Callable[[CollectionState], bool]:
        return lambda _: False

__all__ = [
    "Condition",
    "ItemCondition",
    "QuestCondition",
    "LocationCondition",
    "RegionCondition",
    "AnyElementCondition",
    "OrCondition",
    "AndCondition",
    "VariableCondition",
    "VariableEntryCondition",
    "ChestKeyCondition",
    "ShopSlotCondition",
    "BotanicsCompletionCondition",
    "NeverCondition"
]
