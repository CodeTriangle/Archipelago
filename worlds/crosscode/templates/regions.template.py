{{generated_comment | indent("# ", True)}}

import typing

from .types.regions import RegionConnection, RegionsData
from .types.condition import *

modes = {{ modes | emit_list("constant") }}

default_mode = "{{ default_mode }}"

region_packs: typing.Dict[str, RegionsData] = {
    {% for mode, r in region_packs.items() -%}
    "{{mode}}": RegionsData(
        starting_region = "{{r.starting_region}}",
        goal_region = "{{r.goal_region}}",
        excluded_regions = {{r.excluded_regions}},
        region_list = {{r.region_list | emit_list("constant") | indent(8)}},
        region_connections = {{r.region_connections | emit_list("region_connection") | indent(8)}}
    ),
    {% endfor %}
}
