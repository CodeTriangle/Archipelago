{{generated_comment | indent("# ", True)}}

from .types.condition import *

variable_definitions: dict[str, dict[str, list[Condition]]] = {
    {%- for name, values in code_var_defs.items() %}
    "{{name}}": {
        {% for val, conds in values.items() -%}
        "{{val}}": {{ conds | indent(8) }},
        {%- endfor %}
    },
    {%- endfor %}
}
