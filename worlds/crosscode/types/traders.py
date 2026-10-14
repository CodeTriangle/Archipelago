import typing
from dataclasses import dataclass

from .locations import AccessInfo
from .metadata import IncludeOptions
from .items import ItemData

@dataclass
class TraderData:
    internal_name: str
    name: str
    access: AccessInfo
    metadata: typing.Optional[IncludeOptions] = None

@dataclass
class SingleTrade:
    display_name: str
    reward: ItemData
    cost: list[ItemData]
    index: int

