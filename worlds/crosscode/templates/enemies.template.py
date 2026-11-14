{{generated_comment | indent("# ", True)}}

from .types.condition import *
from .types.enemies import Enemy

enemies: dict[str, Enemy] = {{ enemies | emit_dict("constant", "dataclass") }}
