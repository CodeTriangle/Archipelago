import typing
from dataclasses import dataclass

from .condition import Condition
from .locations import AccessInfo


@dataclass
class ShopData:
    internal_name: str
    name: str
    access: AccessInfo
    include: typing.Optional[list[Condition]] = None
