# WARNING: THIS FILE HAS BEEN GENERATED!
# Modifications to this file will not be kept.
# If you need to change something here, check out codegen.py and the templates directory.


import typing

from .items import items_dict
from .types.items import ItemData, ItemPoolEntry
from .types.condition import *

item_pools_template: dict[str, list[ItemPoolEntry]] = {
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
        ItemPoolEntry(item=items_dict["Faj'ro Key", 1], quantity=9),
        ItemPoolEntry(item=items_dict["Zir'vitar Key", 1], quantity=2),
        ItemPoolEntry(item=items_dict["So'najiz Key", 1], quantity=4),
        ItemPoolEntry(item=items_dict["Krys'kajo Key", 1], quantity=2),
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
    "equipChests": [
        ItemPoolEntry(item=items_dict['Daikon', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Copper Gull', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Rocksplitter', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Prickly Bracer', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Winterclaw', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Hidden Blade', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Bright Bracer', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Humming Razor', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Sunset Claw', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Aehre', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Sneaky Shiv', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Sonic Spike', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Shining Bracer', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Warkeeper', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Cooling Veil', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Mighty Strand', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Furry Cap', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Assault Vest', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Bronze Chest Plate', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Tattered Satchel', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Silver Chest Plate', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Vermillion Mantle', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Timeworn Belt', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Bluefiber Robe', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Golden Chest Plate', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Ancient Sandals', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Lead Boots', 1], quantity=1),
    ],
    "equipQuests": [
        ItemPoolEntry(item=items_dict["Edge o' All", 1], quantity=2),
        ItemPoolEntry(item=items_dict['Bronze Edge', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Battered Fist', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Disciple Gloves', 1], quantity=1),
        ItemPoolEntry(item=items_dict["Hunter's Bolt", 1], quantity=1),
        ItemPoolEntry(item=items_dict['Adept Gloves', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Infinity Spiral Drill', 1], quantity=1),
        ItemPoolEntry(item=items_dict["Explorer's Cap", 1], quantity=1),
        ItemPoolEntry(item=items_dict["Miner's Helmet", 1], quantity=1),
        ItemPoolEntry(item=items_dict['Scarecrown', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Climate Cowl', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Second Hide', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Grasswalkers', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Wooly Socks', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Weird Skates', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Lunatic Paws', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Strawhat', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Dried Grass Hat', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Strawberry Hat', 1], quantity=1),
        ItemPoolEntry(item=items_dict['The Last Strawhat', 1], quantity=1),
    ],
    "fillerCommonCons": [
        ItemPoolEntry(item=items_dict['Sandwich', 3], quantity=50),
        ItemPoolEntry(item=items_dict['Hi-Sandwich', 3], quantity=40),
        ItemPoolEntry(item=items_dict['Green Leaf Tea', 2], quantity=40),
        ItemPoolEntry(item=items_dict['Spicy Bun', 3], quantity=30),
        ItemPoolEntry(item=items_dict['Meaty Risotto', 1], quantity=30),
        ItemPoolEntry(item=items_dict['Fruit Salad', 3], quantity=25),
        ItemPoolEntry(item=items_dict['Veggie Wraps', 3], quantity=25),
    ],
    "fillerCommonDrop": [
        ItemPoolEntry(item=items_dict['Autumn Leaves', 4], quantity=15),
        ItemPoolEntry(item=items_dict['Gold Beetle', 4], quantity=15),
        ItemPoolEntry(item=items_dict['Feather Leaf', 5], quantity=17),
        ItemPoolEntry(item=items_dict['Pike Wood', 5], quantity=17),
        ItemPoolEntry(item=items_dict['Bergen Ice', 5], quantity=9),
        ItemPoolEntry(item=items_dict['Bug Shell', 5], quantity=13),
        ItemPoolEntry(item=items_dict['Tough Sand', 4], quantity=13),
        ItemPoolEntry(item=items_dict['Vivid Water', 5], quantity=20),
        ItemPoolEntry(item=items_dict['Crystal Leek', 4], quantity=15),
        ItemPoolEntry(item=items_dict['Old Bones', 4], quantity=12),
        ItemPoolEntry(item=items_dict['Parched Leaves', 4], quantity=13),
        ItemPoolEntry(item=items_dict['White Grain', 4], quantity=13),
        ItemPoolEntry(item=items_dict['Curly Fern', 4], quantity=11),
        ItemPoolEntry(item=items_dict['Common Planter', 4], quantity=11),
        ItemPoolEntry(item=items_dict['Blue Mango', 4], quantity=11),
        ItemPoolEntry(item=items_dict['Venom Shroom', 4], quantity=11),
        ItemPoolEntry(item=items_dict['Green Arbor', 4], quantity=9),
        ItemPoolEntry(item=items_dict['Blue Grass', 4], quantity=9),
        ItemPoolEntry(item=items_dict['Dirty Rubble', 4], quantity=9),
    ],
    "fillerRareCons": [
        ItemPoolEntry(item=items_dict['Chef Sandwich', 3], quantity=40),
        ItemPoolEntry(item=items_dict['Mega-Sandwich', 2], quantity=30),
        ItemPoolEntry(item=items_dict['Sweet Berry Tea', 2], quantity=40),
        ItemPoolEntry(item=items_dict['Flaming Bun', 3], quantity=35),
        ItemPoolEntry(item=items_dict['Steak, rare', 3], quantity=30),
        ItemPoolEntry(item=items_dict['Chili Con Carne', 2], quantity=30),
        ItemPoolEntry(item=items_dict['Shrimp Risotto', 1], quantity=20),
        ItemPoolEntry(item=items_dict['Fruit Pie', 3], quantity=15),
        ItemPoolEntry(item=items_dict['Ginger Tom. Salad', 3], quantity=10),
    ],
    "fillerRareDrop": [
        ItemPoolEntry(item=items_dict['Season Apples', 5], quantity=18),
        ItemPoolEntry(item=items_dict['Twilight Dew', 5], quantity=18),
        ItemPoolEntry(item=items_dict['Rusty Bits', 5], quantity=18),
        ItemPoolEntry(item=items_dict['Metal Gears', 3], quantity=15),
        ItemPoolEntry(item=items_dict['Purple Ore Lump', 6], quantity=21),
        ItemPoolEntry(item=items_dict['Arid Lumber', 4], quantity=17),
        ItemPoolEntry(item=items_dict['Cactone Fruit', 4], quantity=15),
        ItemPoolEntry(item=items_dict['Palmapple Seed', 3], quantity=16),
        ItemPoolEntry(item=items_dict['Glaring Rock', 4], quantity=16),
        ItemPoolEntry(item=items_dict['Helix Relic', 5], quantity=14),
        ItemPoolEntry(item=items_dict['Ripe Apples', 5], quantity=17),
        ItemPoolEntry(item=items_dict['Sunset Dew', 5], quantity=17),
        ItemPoolEntry(item=items_dict['Steel Comb', 4], quantity=16),
        ItemPoolEntry(item=items_dict['Spiky Nut', 4], quantity=18),
        ItemPoolEntry(item=items_dict['Exotic Resin', 3], quantity=15),
        ItemPoolEntry(item=items_dict['Glowing Sphere', 4], quantity=17),
        ItemPoolEntry(item=items_dict['Catalop Pellet', 4], quantity=13),
        ItemPoolEntry(item=items_dict['Pink Petal', 3], quantity=13),
        ItemPoolEntry(item=items_dict['Spark Tin', 3], quantity=11),
    ],
    "fillerEpicCons": [
        ItemPoolEntry(item=items_dict['Cross Sandwich', 2], quantity=50),
        ItemPoolEntry(item=items_dict['Pepper Night Tea', 1], quantity=40),
        ItemPoolEntry(item=items_dict['Blazing Bun', 1], quantity=35),
        ItemPoolEntry(item=items_dict['Chili Dog', 1], quantity=30),
        ItemPoolEntry(item=items_dict['Gourmet Steak', 2], quantity=30),
        ItemPoolEntry(item=items_dict['Cold Platter', 2], quantity=25),
        ItemPoolEntry(item=items_dict['Green Risotto', 2], quantity=20),
        ItemPoolEntry(item=items_dict['Bear Beer', 3], quantity=20),
        ItemPoolEntry(item=items_dict['Crab Mead', 3], quantity=15),
        ItemPoolEntry(item=items_dict['Whale Wine', 3], quantity=15),
    ],
    "fillerEpicDrop": [
        ItemPoolEntry(item=items_dict['Bear Cicada', 3], quantity=14),
        ItemPoolEntry(item=items_dict['Azure Dragonfly', 3], quantity=18),
        ItemPoolEntry(item=items_dict['Frozen Tear', 3], quantity=18),
        ItemPoolEntry(item=items_dict['Winter Thorn', 2], quantity=16),
        ItemPoolEntry(item=items_dict['Blue Orb', 2], quantity=14),
        ItemPoolEntry(item=items_dict['Rainbow Gem', 3], quantity=12),
        ItemPoolEntry(item=items_dict['Maroon Chestnut', 4], quantity=15),
        ItemPoolEntry(item=items_dict['Ancient Earth', 3], quantity=14),
        ItemPoolEntry(item=items_dict['Lucid Shard', 3], quantity=16),
        ItemPoolEntry(item=items_dict['Wolf Cicada', 4], quantity=15),
        ItemPoolEntry(item=items_dict['Crimson Dragonfly', 3], quantity=14),
        ItemPoolEntry(item=items_dict['Elder Wood', 3], quantity=18),
        ItemPoolEntry(item=items_dict['Royal Hive', 2], quantity=13),
        ItemPoolEntry(item=items_dict['Moon Fruit', 3], quantity=16),
        ItemPoolEntry(item=items_dict['Star Fruit', 2], quantity=16),
        ItemPoolEntry(item=items_dict['Virus Root', 2], quantity=16),
        ItemPoolEntry(item=items_dict['Steel Bamboo', 4], quantity=12),
        ItemPoolEntry(item=items_dict['Mystery Grape', 3], quantity=12),
        ItemPoolEntry(item=items_dict['Cobalt Crystal', 4], quantity=12),
    ],
    "fillerLegendary": [
        ItemPoolEntry(item=items_dict['Final Dinner', 1], quantity=30),
        ItemPoolEntry(item=items_dict['Full Course', 1], quantity=30),
        ItemPoolEntry(item=items_dict['One Up', 1], quantity=30),
        ItemPoolEntry(item=items_dict['Rising Super Star', 1], quantity=25),
        ItemPoolEntry(item=items_dict['Guacamole Toast', 1], quantity=25),
        ItemPoolEntry(item=items_dict['Cheese Spaetzle', 1], quantity=20),
        ItemPoolEntry(item=items_dict['Spicy Beat-0-Type', 1], quantity=20),
        ItemPoolEntry(item=items_dict['Durian', 1], quantity=20),
        ItemPoolEntry(item=items_dict['Dk Pepper', 1], quantity=15),
        ItemPoolEntry(item=items_dict['Mooncake', 1], quantity=12),
    ],
    "pets": [
        ItemPoolEntry(item=items_dict['Orange Twister', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Baby Peng', 1], quantity=1),
        ItemPoolEntry(item=items_dict['FDNI Fox', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Good Boy', 1], quantity=1),
        ItemPoolEntry(item=items_dict['S-Rex', 1], quantity=1),
        ItemPoolEntry(item=items_dict["Lil' Reap", 1], quantity=1),
        ItemPoolEntry(item=items_dict['Red Liz', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Shy Fly', 1], quantity=1),
        ItemPoolEntry(item=items_dict['T.A.N.K.', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Micro Crawler', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Cool Bar', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Batboy', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Butterfliege', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Piggybank', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Seedling', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Turbo', 1], quantity=1),
        ItemPoolEntry(item=items_dict['I Rob-0T', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Baby of the East', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Goose', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Nuclear Roach', 1], quantity=1),
        ItemPoolEntry(item=items_dict['Chunky', 1], quantity=1),
    ],
    
}