{{generated_comment | indent("# ", True)}}

from worlds.crosscode import prog_items
from .items import single_items_dict, items_dict
from .types.items import ItemData, ProgressiveItemChain, ProgressiveChainEntry

progressive_chains: dict[str, ProgressiveItemChain] = {
    {%- for name, chain in prog_chains.items() %}
    "{{ name }}": ProgressiveItemChain(
        display_name="{{ chain.display_name }}",
        items={{ chain.items | emit_list("progressive_chain_entry") | indent(8) }},
    ),
    {%- endfor %}
}

progressive_items: dict[str, ItemData] = {{ prog_items.items() | emit_dict("constant", "item_ref") }}
