{{generated_comment | indent("# ", True)}}

from worlds.crosscode import prog_items
from .items import single_items_dict, items_dict
from .types.items import ItemData, ProgressiveItemChain, ProgressiveChainEntry

progressive_chains: dict[str, ProgressiveItemChain] = {
    {%- for name, display_name in prog_chain_names.items() %}
    "{{name}}": ProgressiveItemChain(
        display_name="{{display_name}}",
        items={{prog_chain_lists[name] | indent(8)}},
    ),
    {%- endfor %}
}

progressive_items: dict[str, ItemData] = {{prog_items}}
