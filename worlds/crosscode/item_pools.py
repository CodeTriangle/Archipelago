# WARNING: THIS FILE HAS BEEN GENERATED!
# Modifications to this file will not be kept.
# If you need to change something here, check out codegen.py and the templates directory.


import typing

from .items import items_dict
from .types.items import ItemData, ItemPoolEntry
from .types.condition import *

item_pools: dict[str, list[ItemPoolEntry]] = {
    "required": [
        ItemPoolEntry(item=items_dict['Heat', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Cold', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Shock', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Wave', 1], quantity=1),
        ItemPoolEntry(item=items_dict['SP Upgrade', 1], quantity=2),
        ItemPoolEntry(item=items_dict['Disc of Flora', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Disc of Insight', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Cursed Coin', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Mine Pass', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Guild Pass', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Maroon Cave Pass', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Pond Slums Pass', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Blue Ice Shade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Meteor Shade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Red Flame Shade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Yellow Sand Shade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Purple Bolt Shade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Star Shade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Azure Drop Shade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Green Leaf Shade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Green Seed Shade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Mine Key', 1], quantity=5),
        ItemPoolEntry(item=items_dict['Mine Key', 1], quantity=-4, metadata={'keyrings': True}),
        ItemPoolEntry(item=items_dict["Faj'ro Key", 1], quantity=9),
        ItemPoolEntry(item=items_dict["Faj'ro Key", 1], quantity=-8, metadata={'keyrings': True}),
        ItemPoolEntry(item=items_dict["Zir'vitar Key", 1], quantity=2),
        ItemPoolEntry(item=items_dict["Zir'vitar Key", 1], quantity=-1, metadata={'keyrings': True}),
        ItemPoolEntry(item=items_dict["So'najiz Key", 1], quantity=4),
        ItemPoolEntry(item=items_dict["So'najiz Key", 1], quantity=-3, metadata={'keyrings': True}),
        ItemPoolEntry(item=items_dict["Krys'kajo Key", 1], quantity=2),
        ItemPoolEntry(item=items_dict["Krys'kajo Key", 1], quantity=-1, metadata={'keyrings': True}),
        ItemPoolEntry(item=items_dict["Thief's Key", 1], quantity=1),
        ItemPoolEntry(item=items_dict['White Key', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Radiant Key', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Mine Master Key', 1], quantity=1),
        ItemPoolEntry(item=items_dict["Faj'ro Master Key", 1], quantity=1),
        ItemPoolEntry(item=items_dict['Kajo Master Key', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Old Dojo Key', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Broken Gauntlet', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Broken Shield', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Broken Chakrams', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Broken Sword', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Broken Deck', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Old Blueprint', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Very Large Ember', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Halcyon Droplet', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Portrait of Ruin', 1], quantity=1),
        ItemPoolEntry(item=items_dict["Heaven's Seed", 1], quantity=1),
        ItemPoolEntry(item=items_dict['Everlasting Amber', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Galaxy Berry', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Dream Globe', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Tremor Engine', 1], quantity=4),
        ItemPoolEntry(item=items_dict['Geta Wood', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Geta Glue', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Hungry Salmon', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Mysterious Box', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Omni Lock', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Golden Triangle', 1], quantity=3),
        ItemPoolEntry(item=items_dict["King's Ring", 1], quantity=1),
    ],
    "fillerCommon": [
        ItemPoolEntry(item=items_dict['Sandwich', 3], quantity=50),
        ItemPoolEntry(item=items_dict['Hi-Sandwich', 3], quantity=40),
        ItemPoolEntry(item=items_dict['Green Leaf Tea', 2], quantity=40),
        ItemPoolEntry(item=items_dict['Spicy Bun', 3], quantity=30),
        ItemPoolEntry(item=items_dict['Meaty Risotto', 1], quantity=30),
        ItemPoolEntry(item=items_dict['Fruit Salad', 3], quantity=25),
        ItemPoolEntry(item=items_dict['Veggie Wraps', 3], quantity=20),
        ItemPoolEntry(item=items_dict['Autumn Leaves', 4], quantity=18),
        ItemPoolEntry(item=items_dict['Gold Beetle', 4], quantity=18),
        ItemPoolEntry(item=items_dict['Feather Leaf', 5], quantity=20),
        ItemPoolEntry(item=items_dict['Pike Wood', 5], quantity=20),
        ItemPoolEntry(item=items_dict['Bergen Ice', 5], quantity=12),
        ItemPoolEntry(item=items_dict['Bug Shell', 5], quantity=16),
        ItemPoolEntry(item=items_dict['Tough Sand', 4], quantity=16),
        ItemPoolEntry(item=items_dict['Vivid Water', 5], quantity=28),
        ItemPoolEntry(item=items_dict['Crystal Leek', 4], quantity=18),
        ItemPoolEntry(item=items_dict['Old Bones', 4], quantity=15),
        ItemPoolEntry(item=items_dict['Parched Leaves', 4], quantity=16),
        ItemPoolEntry(item=items_dict['White Grain', 4], quantity=16),
        ItemPoolEntry(item=items_dict['Curly Fern', 4], quantity=14),
        ItemPoolEntry(item=items_dict['Common Planter', 4], quantity=14),
        ItemPoolEntry(item=items_dict['Blue Mango', 4], quantity=14),
        ItemPoolEntry(item=items_dict['Venom Shroom', 4], quantity=14),
        ItemPoolEntry(item=items_dict['Green Arbor', 4], quantity=12),
        ItemPoolEntry(item=items_dict['Blue Grass', 4], quantity=12),
        ItemPoolEntry(item=items_dict['Dirty Rubble', 4], quantity=12),
    ],
    
}