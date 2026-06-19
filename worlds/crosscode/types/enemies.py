from dataclasses import dataclass, field

from .items import ItemData
from .locations import LocationData

@dataclass
class Booster:
    level: int
    """Level that the enemy gets boosted to in vanilla"""
    booster: ItemData
    """Booster that effects the boost"""

@dataclass
class Enemy:
    name: str
    """The human-readable name of the enemy"""
    area: str
    """The internal area where the enemy is found"""
    internal_name: str
    """The enemy's name in the game files"""
    level: int
    """The enemy's base level in vanilla"""
    first_encounter_event: LocationData
    """The event that unlocks whether you can fight one instance of the enemy (for killsanity)"""
    grind_access_event: LocationData | None = field(default=None)
    """The event that unlocks whether you can grind the enemy -- if null, enemy cannot be grinded"""
    booster: Booster | None = field(default=None)
    """If the enemy can be boosted, the details about that"""
