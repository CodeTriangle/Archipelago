import typing
from BaseClasses import Item, ItemClassification

class ItemData(typing.NamedTuple):
    name: str
    item_id: int
    amount: int
    combo_id: int
    classification: ItemClassification

    def __hash__(self):
        return hash((self.item_id, self.amount))

    def __eq__(self, other):
        return self.item_id == other.item_id and self.amount == other.amount

class CrossCodeItem(Item):
    game: str = "CrossCode"
    data: ItemData

    def __init__(self, player: int, data: ItemData):
        super(CrossCodeItem, self).__init__(
            data.name,
            data.classification,
            data.combo_id,
            player,
        )

        self.data = data
