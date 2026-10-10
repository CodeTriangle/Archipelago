{{generated_comment | indent("# ", True)}}

from .types.condition import *

variable_definitions: dict[str, dict[str, list[Condition]]] = {
    {%- for name, values in variable_definitions.items() %}
    "{{name}}": {
        {% for val, conds in values.items() -%}
        "{{val}}": {{ conds | emit_list("condition") | indent(8) }},
        {%- endfor %}
    },
    {%- endfor %}
}
