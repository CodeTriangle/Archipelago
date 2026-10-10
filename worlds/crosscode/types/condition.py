from __future__ import annotations
import typing
import abc
from dataclasses import dataclass, field

from BaseClasses import CollectionState
from ..options import ShopReceiveMode

from .items import ItemPoolEntry

if typing.TYPE_CHECKING:
    from ..world import CrossCodeWorld

class Condition(abc.ABC):
    """
    An abstract representation of a condition that can be stored once and used in all CrossCode worlds.

    This mimics rule builder but was made far before it and is better-adapted to this world's architecture.
    """

    is_stateless: bool
    """
    A variable that indicates whether this condition is stateless. See check_stateless for more details.
    """

    @abc.abstractmethod
    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        """
        A function that returns a closure representing whether the condition is satisfied given a collection state
        full of items.

        You are advised to do as much work before returning the closure as possible as it is only run once per world per
        condition. This will speed up runtime logic, which will be called repeatedly.
        """
        pass

    @abc.abstractmethod
    def check_stateless(self, player: int, location: int | None, world: CrossCodeWorld) -> bool:
        """
        A function that returns a bool representing whether the stateless condition is satisfied.

        This function should only be defined if, for the condition, the collection state is immaterial to calculating
        the satisfaction of the condition; i.e. it will return the same answer no matter what items the player has.

        This function should be defined when possible because several optimizations can be performed if it is. When
        defining this, the is_stateless flag should be set. You should also consider using the StatelessCondition
        subclass, which provides a boilerplate satisfied method.
        """
        pass

class StatefulCondition(Condition):
    """
    A condition whose truth value varies depending on the collection state of the multiworld.

    This subclass simply fills out a default check_stateless that fails.
    """

    is_stateless = False

    def check_stateless(self, player: int, location: int | None, world: CrossCodeWorld) -> bool:
        raise RuntimeError("Attempted to statically check a stateful condition")

class StatelessCondition(Condition):
    """
    A condition whose truth value does not vary depending on the collection state of the multiworld.

    This subclass simply fills out a default satisfied that defers to the check_stateless.
    """

    is_stateless = True

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        value = self.check_stateless(player, location, world)
        return lambda _: value

@dataclass
class ItemCondition(StatefulCondition):
    item_name: str
    amount: int = 1

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        target = self.amount
        if self.item_name in world.keyrings:
            target = 1

        replacements = world.pools.item_progressive_replacements

        if self.item_name in replacements:
            def callback(state: CollectionState) -> bool:
                for prog_item_name, quantity in replacements[self.item_name]:
                    if state.has(prog_item_name, player, quantity):
                        return True
                return  state.has(self.item_name, player, target)

            return callback

        return lambda state: state.has(self.item_name, player, target)

@dataclass
class QuestCondition(StatefulCondition):
    quest_name: str
    event_name: str = field(init=False)

    def __post_init__(self):
        self.event_name = f"{self.quest_name} (Event)"

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        return lambda state: state.has(self.event_name, player)

@dataclass
class LocationCondition(StatefulCondition):
    location_name: str
    event_name: str = field(init=False)

    def __post_init__(self):
        self.event_name = f"{self.location_name} (Event)"

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        return lambda state: state.has(self.event_name, player)

@dataclass
class RegionCondition(StatefulCondition):
    target_mode: typing.Optional[str]
    region_name: str

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        # target_mode == None means that it matches in all modes.
        # so if target_mode == None, check if we can reach that region.
        # else, if the target mode matches, also check if we can reach that region.
        # otherwise, if the target mode does not match, return true (assume that it's being ANDed with other conditions)

        mode: str = world.logic_mode
        if self.target_mode is None or mode == self.target_mode:
            if self.region_name not in world.multiworld.regions.region_cache[player]:
                return lambda _: False
            return lambda state: state.can_reach_region(self.region_name, player)

        return lambda _: True

@dataclass
class AnyElementCondition(StatefulCondition):
    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        return lambda state: any([
            state.has("Heat", player),
            state.has("Cold", player),
            state.has("Shock", player),
            state.has("Wave", player),
        ])

@dataclass
class OrCondition(Condition):
    subconditions: list[Condition]

    def __post_init__(self):
        self.is_stateless = all(c.is_stateless for c in self.subconditions)

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        if self.is_stateless: # optimization: if all subconditions are stateless, precompute the sum value.
            return lambda _: self.check_stateless(player, location, world)
        callbacks = [x.satisfied(player, location, world) for x in self.subconditions]
        return lambda state: any(map(lambda x: x(state), callbacks))

    def check_stateless(self, player: int, location: int | None, world: CrossCodeWorld) -> bool:
        if not self.is_stateless:
            raise RuntimeError("Tried to statelessly check an or condition that has non-stateless subconditions")
        return any(c.check_stateless(player, location, world) for c in self.subconditions)

@dataclass
class AndCondition(Condition):
    subconditions: list[Condition]

    def __post_init__(self):
        self.is_stateless = all(isinstance(c, StatelessCondition) for c in self.subconditions)

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        if self.is_stateless: # optimization: if all subconditions are stateless, precompute the sum value.
            return lambda _: self.check_stateless(player, location, world)
        callbacks = [x.satisfied(player, location, world) for x in self.subconditions]
        return lambda state: all(map(lambda x: x(state), callbacks))

    def check_stateless(self, player: int, location: int | None, world: CrossCodeWorld) -> bool:
        if not self.is_stateless:
            raise RuntimeError("Tried to statelessly check an and condition that has non-stateless subconditions")
        return all(c.check_stateless(player, location, world) for c in self.subconditions)

@dataclass
class VariableCondition(StatefulCondition):
    name: str

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        variables = world.variables
        variable_definitions = world.world_data.variable_definitions

        if self.name not in variables:
            return lambda _: True

        callbacks = sum(
            [
                [
                    x.satisfied(player, location, world)
                    for x in variable_definitions[self.name][value]
                ] for value in variables[self.name]
            ],
            start=[]
        )

        return lambda state: all(map(lambda x: x(state), callbacks))

@dataclass
class VariableEntryCondition(StatelessCondition):
    name: str
    value: str
    desired: bool

    def check_stateless(self, player: int, location: int | None, world: CrossCodeWorld) -> bool:
        valid = (self.value in world.variables[self.name]) == self.desired
        return valid

@dataclass
class ChestKeyCondition(StatefulCondition):
    default_level: str

    clearance_items: typing.ClassVar[dict[str, str]] =  {
        "Bronze": "Thief's Key",
        "Silver": "White Key",
        "Gold": "Radiant Key",
    }

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        chest_levels = world.chest_clearance_levels

        if location is None:
            raise RuntimeError("An event cannot have a chest key condition")

        level: str = chest_levels.get(location, self.default_level)

        if level == "Default":
            return lambda _: True

        return lambda state: state.has(ChestKeyCondition.clearance_items[level], player)

@dataclass
class ShopSlotCondition(StatefulCondition):
    shop_name: str
    item_id: int

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        if world.shop_receive_mode is None:
            return lambda _: True
        if world.shop_receive_mode == ShopReceiveMode.option_per_item_type:
            return lambda state: state.has(world.world_data.shop_unlock_by_id[self.item_id].item.name, player)
        if world.shop_receive_mode == ShopReceiveMode.option_per_shop:
            return lambda state: state.has(world.world_data.shop_unlock_by_shop[self.shop_name].item.name, player)
        if world.shop_receive_mode == ShopReceiveMode.option_per_slot:
            return lambda state: state.has(world.world_data.shop_unlock_by_shop_and_id[self.shop_name, self.item_id].item.name, player)
        return lambda _: True

@dataclass
class BotanicsCompletionCondition(StatefulCondition):
    amount: float

    def satisfied(self, player: int, location: int | None, world: CrossCodeWorld) -> typing.Callable[[CollectionState], bool]:
        regions = {
            region: amount
            for region, amount in world.world_data.region_botanics_amounts[world.logic_mode].items()
            if region in world.multiworld.regions.region_cache[player]
        }

        def satisfied_internal(state: CollectionState):
            collected = sum([
                amount
                for region, amount in regions.items()
                if state.can_reach_region(region, player)
            ])

            return collected / world.options.botanics_completion_amount >= self.amount
        return satisfied_internal

class NeverCondition(StatelessCondition):
    def check_stateless(self, player: int, location: int | None, world: CrossCodeWorld) -> bool:
        return False

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
