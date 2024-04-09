import re
from ..codegen.util import BASE_ID, NUM_ITEMS, RESERVED_ITEM_IDS
from dataclasses import dataclass, field
import typing
from BaseClasses import Item, ItemClassification

@dataclass
class SingleItemData:
    name: str
    item_id: int
    classification: ItemClassification
    unique: bool = False

def get_combo_id(item: SingleItemData, amount: int) -> int:
    return BASE_ID + RESERVED_ITEM_IDS + NUM_ITEMS * (amount - 1) + item.item_id

def get_info_from_full_name(name: str) -> tuple[str, int]:
    m = re.match(r"(.+) x(\d+)", name)
    if m is None:
        return name, 1
    name, id = m.groups()
    id = int(id)
    return name, id

@dataclass
class ItemData:
    item: SingleItemData
    amount: int
    combo_id: int = 0
    name: str = field(init=False)

    def __post_init__(self):
        if self.combo_id == 0:
            self.combo_id = get_combo_id(self.item, self.amount)
        self.name = self.item.name if self.amount == 1 else f"{self.item.name} x{self.amount}"

class CrossCodeItem(Item):
    game: str = "CrossCode"
    data: ItemData

    def __init__(self, player: int, data: ItemData):
        super(CrossCodeItem, self).__init__(
            data.item.name,
            data.item.classification,
            data.combo_id,
            player,
        )

        self.data = data
