from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import WebWorld, World

from .Items import (
    ITEM_NAME_TO_ID,
    MIOItem,
    create_all_items,
    create_item_with_correct_classification,
    get_random_filler_item_name,
)
from .Locations import LOCATION_NAME_TO_ID, create_all_locations
from .Options import MIOOptions
from .Regions import create_and_connect_regions
from .Rules import set_all_rules


class MIOWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = []


class MIOWorld(World):
    """
    MIO: Memories in Orbit is a Metroidvania released in 2026 by Douze Dixiemes.
    """

    game = "Memories in Orbit"
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
        set_all_rules(self)

    def create_items(self) -> None:
        create_all_items(self)

    def create_item(self, name: str) -> MIOItem:
        return create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "logic_difficulty",
            "boss_kill_checks",
        )
