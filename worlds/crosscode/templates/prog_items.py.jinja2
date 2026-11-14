{{generated_comment | indent("# ", True)}}

from worlds.crosscode import prog_items
from .items import single_items_dict, items_dict
from .types.items import ItemData, ProgressiveItemChain, ProgressiveItemChainSingle, ProgressiveItemChainMulti, ProgressiveChainEntry, ProgressiveItemSubchain

progressive_chains: dict[str, ProgressiveItemChain] = {
    {%- for name, chain in prog_chains.items() %}
    {%- if prog_chain_types[name] == "single" %}
    "{{ name }}": ProgressiveItemChainSingle(
        display_name="{{ chain.display_name }}",
        items={{ chain.items | emit_list("progressive_chain_entry") | indent(8) }},
    ),
    {%- elif prog_chain_types[name] == "multi" %}
    "{{ name }}": ProgressiveItemChainMulti(
        display_name="{{ chain.display_name }}",
        subchains=[
            {%- for subchain in chain.subchains %}
            ProgressiveItemSubchain(
                metadata={{ subchain.metadata.items() | emit_dict("constant", "constant") | indent(16) }},
                chain={{ subchain.chain | emit_list("progressive_chain_entry") | indent(16) }}
            ),
            {%- endfor %}
        ],
    ),
    {%- endif %}
    {%- endfor %}
}

progressive_items: dict[str, ItemData] = {{ prog_items.items() | emit_dict("constant", "item_ref") }}
