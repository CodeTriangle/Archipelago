from typing import TypedDict

class IncludeOptions(TypedDict, total=False):
    dlc: bool
    trade: bool
    shop: bool
    arena: bool
    chest: bool
    quest: bool
    botanics: bool
    combat: bool
    kill: bool
