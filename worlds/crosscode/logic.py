"""
This module contains various logic functions
"""

import typing
from BaseClasses import CollectionState
from .types.condition import Condition, LogicDict

def condition_satisfied(
    player: int,
    conditions: list[Condition],
    location: int | None,
    cond_args: LogicDict
) -> typing.Callable[[CollectionState], bool]:
    """
    Factory function. Return value is a rule that checks whether all the conditions are satisfied.
    """
    callbacks = [c.satisfied(player, location, cond_args) for c in conditions]

    return lambda state: all(map(lambda x: x(state), callbacks))
