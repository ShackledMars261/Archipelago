from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, Location, Region
from worlds.mio.DataProvider import DataProvider, WorldDataEvent, WorldDataLocation, WorldDataRoom

from .Items import MIOItem

if TYPE_CHECKING:
    from . import MIOWorld


# LOCATION_NAME_TO_ID: dict[str, int] = {
# "Samsk: Hairpin": 1,
# "Samsk: Harvester": 2,
# "Samsk: Dodge": 3,
# "Samsk: Sail": 4,
# "Samsk: Striders": 5,
# "Samsk: Slingshot": 6,
# "Samsk: Flowing Steps": 7,
# "Flash Memory - Connection Lost": 8,
# "Silo Access Badge": 9,
# }


class MIOLocation(Location):
    game = "Memories in Orbit"


def location_name_to_id(world: MIOWorld, name: str) -> int | None:
    locations: list[WorldDataLocation] = world.data_provider.data.locations
    for location in locations:
        if location.name == name:
            return location.id
    return None


def build_location_name_to_id_dict(data_provider: DataProvider) -> dict[str, int]:
    return {location.name: location.id for location in data_provider.data.locations}


def get_location_names_with_ids(world: MIOWorld, location_names: list[str]) -> dict[str, int | None]:
    return {location_name: location_name_to_id(world, location_name) for location_name in location_names}


def create_all_locations(world: MIOWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def add_locations_to_region(
    world: MIOWorld, region_name: str, location_names: list[str], location_type: type[Location] = MIOLocation
) -> None:
    if len(location_names) == 0:
        return None
    region: Region = world.get_region(region_name)
    return region.add_locations(get_location_names_with_ids(world, location_names), location_type)


def create_regular_locations(world: MIOWorld) -> None:
    # The Severed Spine
    # add_locations_to_region(
    # world,
    # "ST_security_fall_P1",
    # [],
    # )
    # add_locations_to_region(
    # world,
    # "ST_security_fall_P2",
    # [],
    # )
    # add_locations_to_region(
    # world,
    # "ST_security_fall_F1",
    # [],
    # )
    # add_locations_to_region(
    # world,
    # "ST_security_fall_S1",
    # [
    # "Flash Memory - Connection Lost",
    # ],
    # )

    rooms: list[WorldDataRoom] = world.data_provider.data.rooms

    for room in rooms:
        room_locations: list[WorldDataLocation] = room.locations
        add_locations_to_region(world, room.name, [location.name for location in room_locations])


def create_event(world: MIOWorld, region_name: str, location_name: str, item_name: str) -> Item:
    region = world.get_region(region_name)
    return region.add_event(location_name, item_name, location_type=MIOLocation, item_type=MIOItem)


def create_events(world: MIOWorld) -> None:
    # create_event(world, "ST_security_fall_S1", "Ati Defeated", "Victory")
    # create_event(world, "ST_security_view", "Starting Tremor", "Starting Tremor")
    events: list[WorldDataEvent] = world.data_provider.data.events
    for event in events:
        create_event(world, event.roomName, event.locationName, event.itemName)
