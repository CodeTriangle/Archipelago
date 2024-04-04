{{generated_comment | indent("# ", True)}}

from collections import defaultdict
from BaseClasses import ItemClassification
from .util import keydefaultdict
from .types.items import ItemData, SingleItemData

num_items = {{num_items}}

single_items_dict: dict[str, SingleItemData] = {{single_items_dict}}

items_dict: dict[tuple[str, int], ItemData] = keydefaultdict(
    lambda key: ItemData(item=single_items_dict[key[0]], amount=key[1]),
    {{items_dict | indent(4)}}
)

items_by_full_name: dict[str, ItemData] = { f"{name} x{amount}" if amount > 1 else name: value for (name, amount), value in items_dict.items() }
