from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import MIOWorld


LOCATION_NAME_TO_ID: dict[str, int] = {
    "Navigation Circuit": 1,
    "Flowing Steps": 2,
    "Hairpin": 3,
    "Dodge": 4,
    "Harvester": 5,
    "Sail": 6,
    "Striders": 7,
    "Slingshot": 8,
}


class MIOLocation(Location):
    game = "MIO: Memories in Orbit"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: MIOWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: MIOWorld) -> None:
    starting_area = world.get_region("Starting Area")


def create_events(world: MIOWorld) -> None:
    pass
