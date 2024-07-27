from ..options import CrossCodeOptions, ShopReceiveMode
from typing import TypedDict

class IncludeOptions(TypedDict):
    questRandoOnly: bool
    shops: bool
    shopSendMode: int
