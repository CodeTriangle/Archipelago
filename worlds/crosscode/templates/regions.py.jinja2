{{generated_comment | indent("# ", True)}}

import typing

from .types.regions import Goal, RegionConnection, RegionsData
from .types.condition import *

modes = {{ modes | emit_list("constant") }}

default_mode = "{{ default_mode }}"

region_packs: typing.Dict[str, RegionsData] = {
    {% for mode, r in region_packs.items() -%}
    "{{mode}}": RegionsData(
        starting_region = "{{r.starting_region}}",
        excluded_regions = {{r.excluded_regions}},
        region_connections = {{r.region_connections | emit_list("region_connection") | indent(8)}},
        goals = {{r.goals.items() | emit_dict("constant", "goal") | indent(8) }}
    ),
    {% endfor %}
}

region_botanics_amounts: dict[str, dict[str, int]] = {
    {% for mode, amounts in region_botanics_amounts.items() -%}
    "{{mode}}": {{ amounts | emit_dict("constant", "constant") | indent(4) }}
    {% endfor %}
}
