from worlds.AutoWorld import WebWorld, World

from .Items import ITEM_NAME_TO_ID
from .Options import MIOOptions


class MIOWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = []


class MIOWorld(World):
    """
    MIO: Memories in Orbit is a Metroidvania released in 2026 by Douze Dixiemes.
    """

    game = "MIO: Memories in Orbit"
    web = MIOWebWorld()

    options_dataclass = MIOOptions
    options: MIOOptions

    origin_region_name = "Starting Room"

    item_name_to_id = ITEM_NAME_TO_ID
