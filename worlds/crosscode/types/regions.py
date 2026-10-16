from dataclasses import dataclass, field
import typing

from .condition import Condition

@dataclass
class RegionConnection:
    region_from: str
    region_to: str
    cond: typing.Optional[list[Condition]]
    bidirectional: bool = True
    include: typing.Optional[list[Condition]] = None

@dataclass
class Goal:
    region: str
    condition: typing.Optional[typing.List[Condition]]

@dataclass
class RegionsData:
    starting_region: str
    excluded_regions: typing.List[str]
    region_connections: typing.List[RegionConnection]
    goals: typing.Dict[str, Goal]
