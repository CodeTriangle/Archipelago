import typing
from dataclasses import dataclass, field

from BaseClasses import Location, Region
from .metadata import IncludeOptions

from .condition import Condition

@dataclass
class AccessInfo:
    region: typing.Dict[str, str]
    cond: typing.Optional[list[Condition]] = None

@dataclass
class LocationData:
    name: str
    """The Archipelago item name"""
    code: typing.Optional[int]
    """The Archipelago item ID"""
    access: AccessInfo
    area: typing.Optional[str] = None
    """The in-game area (i.e. rookie-harbor for Rookie Harbor)"""
    metadata: typing.Optional[IncludeOptions] = None
    """Metadata (used to decide whether to include this location)"""

    def __hash__(self):
        # Every LocationData instance will have a unique name, so we should not
        # need to use any other fields to hash it.
        return hash(self.name)

class CrossCodeLocation(Location):
    game: str = "CrossCode"
    data: LocationData
    region: str

    def __init__(self, player: int, data: LocationData, mode, region_dict: dict[str, Region], event_from_location=False):
        event_from_location = event_from_location and data.code is not None

        super(CrossCodeLocation, self).__init__(
            player,
            data.name if not event_from_location else data.name + " (Event)",
            data.code if not event_from_location else None,
            region_dict[data.access.region[mode]]
        )

        self.data = data
        self.event = False
        self.region = data.access.region[mode]
