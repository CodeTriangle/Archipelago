{{generated_comment | indent("# ", True)}}

from .types.locations import LocationData, AccessInfo
from .types.condition import *

locations_data = {{locations_data}}

locations_dict = { location.name: location for location in locations_data }

events_data = {{events_data}}

events_dict = { location.name: location for location in events_data }
