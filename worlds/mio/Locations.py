from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location, Region

from .Items import MIOItem

if TYPE_CHECKING:
    from . import MIOWorld


LOCATION_NAME_TO_ID: dict[str, int] = {
    "Samsk: Hairpin": 0,
    "Samsk: Harvester": 1,
    "Samsk: Dodge": 2,
    "Samsk: Sail": 3,
    "Samsk: Striders": 4,
    "Samsk: Slingshot": 5,
    "Samsk: Flowing Steps": 6,
}


class MIOLocation(Location):
    game = "Memories in Orbit"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: MIOWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def add_locations_to_region(
    world: MIOWorld, region_name: str, location_names: list[str], location_type: type[Location] = MIOLocation
) -> None:
    region: Region = world.get_region(region_name)
    return region.add_locations(get_location_names_with_ids(location_names), location_type)


def create_regular_locations(world: MIOWorld) -> None:
    # The Severed Spine
    add_locations_to_region(
        world,
        "ST_security_fall_P1",
        [
            "Samsk: Hairpin",
            "Samsk: Harvester",
            "Samsk: Dodge",
            "Samsk: Sail",
        ],
    )
    add_locations_to_region(
        world,
        "ST_security_fall_F1",
        [
            "Samsk: Striders",
            "Samsk: Slingshot",
        ],
    )
    add_locations_to_region(
        world,
        "ST_security_fall_S1",
        [
            "Samsk: Flowing Steps",
        ],
    )


def create_events(world: MIOWorld) -> None:
    ST_security_fall_S1 = world.get_region("ST_security_fall_S1")

    ST_security_fall_S1.add_event("Ati Defeated", "Victory", location_type=MIOLocation, item_type=MIOItem)
