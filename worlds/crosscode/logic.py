"""
This module contains various logic functions
"""

from __future__ import annotations
import typing
from BaseClasses import CollectionState
from .types.condition import Condition

if typing.TYPE_CHECKING:
    from .world import CrossCodeWorld

def condition_satisfied(
    player: int,
    conditions: list[Condition],
    location: int | None,
    world: CrossCodeWorld
) -> typing.Callable[[CollectionState], bool]:
    """
    Factory function. Return value is a rule that checks whether all the conditions are satisfied.
    """
    callbacks = [c.satisfied(player, location, world) for c in conditions]

    return lambda state: all(map(lambda x: x(state), callbacks))

def check_stateless(
    player: int,
    conditions: list[Condition],
    location: int | None,
    world: CrossCodeWorld
) -> bool:
    """
    Return whether the condition is true in a stateless fashion.
    """
    return all(c.check_stateless(player, location, world) for c in conditions)
