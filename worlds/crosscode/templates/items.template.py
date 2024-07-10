{{generated_comment | indent("# ", True)}}

from collections import defaultdict
from BaseClasses import ItemClassification
from worlds.crosscode.types.items import get_info_from_full_name
from .util import KeyDefaultDict
from .types.items import ItemData, SingleItemData

num_items = {{num_items}}

single_items_dict: dict[str, SingleItemData] = {{ single_items_dict | emit_dict("constant", "single_item") }}
"""Dict associating item name with single item data.
SingleItemData represents properties inherent to the item itself, regardless of
the amount of the item.
"""

def __item_data_from_tuple(key: tuple[str, int]) -> ItemData:
    name, amount = key
    return ItemData(item=single_items_dict[name], amount=amount)

items_dict: dict[tuple[str, int], ItemData] = KeyDefaultDict(__item_data_from_tuple, {{ items_dict | emit_dict("tuple", "item") }})
"""Dict which can calculate the ItemData for any item name and amount.
Includes a large cached list of all those items found in code generation.
However, can also be used to generate an arbitrary amount of items.
This feature is useful for custom item placement.
"""

items_by_full_name: dict[str, ItemData] = KeyDefaultDict(
    lambda name: items_dict[get_info_from_full_name(name)],
    { name if amount == 1 else f"{name} x{amount}": value for (name, amount), value in items_dict.items() }
)
"""Dict associating full item name with item data.
Uses cache in items_dict for speedy access.
Computes using the key if cache miss.
"""

keyring_items = {{keyring_items | emit_set("constant") }}
