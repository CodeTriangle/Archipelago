{{generated_comment | indent("# ", True)}}

from .types.locations import LocationData, AccessInfo
from .types.condition import *

locations_data = {{locations_data | emit_list("location") }}

locations_dict = { location.name: location for location in locations_data }

events_data = {{events_data | emit_list("location") }}

events_dict = { location.name: location for location in events_data }

locked_locations = {{ locked_locations | emit_set("constant") }}

pool_locations = {{ pool_locations | emit_list("location_ref") }}

location_groups = {
    {% for name, group in location_groups.items() -%}
    "{{name}}": {{ group | emit_set("location_ref") | indent(4) }},
    {% endfor %}
}
