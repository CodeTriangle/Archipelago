{{generated_comment | indent("# ", True)}}

from worlds.crosscode import prog_items
from .items import single_items_dict, items_dict
from .types.items import ItemData, ProgressiveItemChain, ProgressiveItemChainSingle, ProgressiveItemChainMulti, ProgressiveChainEntry, ProgressiveItemSubchain

progressive_chains: dict[str, ProgressiveItemChain] = {
    {%- for name, display_name in prog_chain_names.items() %}
    {%- if name in prog_chain_lists_single %}
    "{{name}}": ProgressiveItemChainSingle(
        display_name="{{display_name}}",
        items={{prog_chain_lists_single[name] | indent(8)}},
    ),
    {%- elif name in prog_chain_lists_multi %}
    "{{name}}": ProgressiveItemChainMulti(
        display_name="{{display_name}}",
        subchains=[
            {%- for metadata, subchain in prog_chain_lists_multi[name] %}
            ProgressiveItemSubchain(
                metadata={{ metadata | indent(16) }},
                chain={{ subchain | indent(16) }}
            ),
            {%- endfor %}
        ],
    ),
    {%- endif %}
    {%- endfor %}
}

progressive_items: dict[str, ItemData] = {{prog_items}}
