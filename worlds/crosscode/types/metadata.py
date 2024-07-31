from ..options import CrossCodeOptions
from typing import TypedDict

class IncludeOptions(TypedDict):
    trade: bool
    shop: bool
    arena: bool
    chest: bool
    quest: bool
