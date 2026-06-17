from dataclasses import dataclass, field
import typing

from .condition import Condition

@dataclass
class RegionConnection:
    region_from: str
    """The region that this connection comes from"""
    region_to: str
    """The region that this connection leads to"""
    cond: typing.Optional[list[Condition]]
    """The condition for accessing this connection"""

@dataclass
class Goal:
    region: str
    condition: typing.Optional[typing.List[Condition]]

@dataclass
class RegionsData:
    starting_region: str
    """The region in which you start"""
    excluded_regions: typing.List[str]
    """Regions that should not actually be generated (deprecated)"""
    region_list: typing.List[str]
    """A list of region names found in the connections"""
    region_connections: typing.List[RegionConnection]
    """A list of region connections"""
    goals: typing.Dict[str, Goal]
    """Goals and the conditions required to access them"""
