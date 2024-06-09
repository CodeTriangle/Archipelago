{{generated_comment | indent("# ", True)}}

import typing

from .items import items_dict
from .types.items import ItemData, ItemPoolEntry
from .types.condition import *

item_pools_template: dict[str, list[ItemPoolEntry]] = {
    {% for name, pool in item_pools.items() -%}
    "{{name}}": {{pool | emit_list("item_pool_entry") | indent(4)}},
    {% endfor %}
}
