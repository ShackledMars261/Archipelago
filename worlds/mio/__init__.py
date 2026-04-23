from worlds.AutoWorld import WebWorld, World

from .Items import ITEM_NAME_TO_ID
from .Locations import LOCATION_NAME_TO_ID, create_all_locations
from .Options import MIOOptions
from .Regions import create_and_connect_regions


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

    origin_region_name = "ST_security_fall_P1"

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    def create_regions(self) -> None:
        create_and_connect_regions(self)
        create_all_locations(self)

    def set_rules(self) -> None:
        pass
