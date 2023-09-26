from Options import AssembleOptions, Choice, DefaultOnToggle
import typing

class VTShadeLock(DefaultOnToggle):
    """
    If enabled, adds a locked gate before the final dungeon that only opens when all four shades are collected and all four bosses are beaten.
    """
    display_name = "Vermillion Tower Shade Lock"

class StartWithGreenLeafShade(DefaultOnToggle):
    """
    If enabled, the player will start with the green leaf shade, unlocking Autumn's Fall. This makes the early game far more open.
    """
    display_name = "Start with Green Leaf Shade"

class Reachability(Choice):
    option_local = 0
    option_non_local = 1
    option_any = 2

    default = 2

class ShadeLocations(Reachability):
    """
    Where shades will appear
    [Local] In your own world
    [Non-local] In someone else's world
    [Any] Anywhere in the multiworld
    """

    display_name = "Shade Locations"

class ElementLocations(Reachability):
    """
    Where elements will appear
    [Local] In your own world
    [Non-local] In someone else's world
    [Any] Anywhere in the multiworld
    """

    display_name = "Element Locations"

crosscode_options_pairs = [
    ("vt_shade_lock", VTShadeLock),
    ("start_with_green_leaf_shade", StartWithGreenLeafShade),
    ("shade_locations", ShadeLocations),
    ("element_locations", ElementLocations),
]

try:
    from .OptionsGenerated import LogicMode
    crosscode_options_pairs.insert(0, ("logic_mode", LogicMode))
except ImportError:
    pass

crosscode_options: typing.Dict[str, AssembleOptions] = dict(crosscode_options_pairs)
