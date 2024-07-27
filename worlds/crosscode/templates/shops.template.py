{{generated_comment | indent("# ", True)}}

from .items import items_dict
from .types.locations import AccessInfo, LocationData
from .types.shops import ShopData
from .types.condition import *
from .locations import locations_dict

shop_dict: dict[str, ShopData] = {{ shop_data.items() | emit_dict("constant", "shop") }}

per_shop_locations: dict[str, dict[int, LocationData]] = {
    {% for name, data in per_shop_locations.items() -%}
        "{{name}}": {{ data.items() | emit_dict("constant", "location_ref") | indent(4) }},
    {% endfor %}
}

global_shop_locations: dict[int, LocationData] = {{ global_shop_locations.items() | emit_dict("constant", "location_ref") }}

shop_unlock_by_id = {{ shop_unlock_by_id.items() | emit_dict("constant", "item_ref") }}

shop_unlock_by_shop = {{ shop_unlock_by_shop.items() | emit_dict("constant", "item_ref") }}

shop_unlock_by_shop_and_id = {{ shop_unlock_by_shop_and_id.items() | emit_dict("tuple", "item_ref") }}
