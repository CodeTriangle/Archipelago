from .types.world import WorldData
from .regions import region_packs
from .items import single_items_dict, items_dict, items_by_full_name, keyring_items
from .locations import locations_data, locations_dict, events_dict
from .item_pools import item_pools_template
from .vars import variable_definitions

static_world_data = WorldData(
    region_packs=region_packs,
    locations_dict=locations_dict,
    events_dict=events_dict,
    single_items_dict=single_items_dict,
    items_dict=items_dict,
    items_by_full_name=items_by_full_name,
    keyring_items=keyring_items,
    item_pools_template=item_pools_template,
    variable_definitions=variable_definitions
)
