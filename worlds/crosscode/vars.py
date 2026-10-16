# WARNING: THIS FILE HAS BEEN GENERATED!
# Modifications to this file will not be kept.
# If you need to change something here, check out codegen.py and the templates directory.


from .types.condition import *

variable_definitions: dict[str, dict[str, list[Condition]]] = {
    "vtShadeLock": {
        "shades": [
            ItemCondition(item_name='Blue Ice Shade'),
            ItemCondition(item_name='Red Flame Shade'),
            ItemCondition(item_name='Purple Bolt Shade'),
            ItemCondition(item_name='Azure Drop Shade'),
        ],"bosses": [
            LocationCondition(location_name='Temple Mine Shade Statue'),
            LocationCondition(location_name="Faj'ro Shade Statue"),
            LocationCondition(location_name="Zir'vitar Shade Statue"),
            LocationCondition(location_name="So'najiz Shade Statue"),
        ],
    },
    "vwPassage": {
        "meteor": [
            ItemCondition(item_name='Meteor Shade'),
        ],
    },
    "canGrind": {
        "noShadeWarp": [
            OrCondition(subconditions=[ItemCondition(item_name='Green Leaf Shade'), ItemCondition(item_name='Red Flame Shade')]),
        ],
    },
}