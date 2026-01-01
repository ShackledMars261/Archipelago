from typing import TYPE_CHECKING

from BaseClasses import Region

from .Helpers import split_array
from .Types import ArchipelaCodeLocation, LocData

if TYPE_CHECKING:
    from . import ArchipelaCodeWorld


def create_regions(world: "ArchipelaCodeWorld"):
    world.origin_region_name = "Starter Problems"
    loc_arrays = split_array(world.included_locations, 5)
    starter_problems = create_region(world, "Starter Problems", locations=loc_arrays[0])
    batch_1 = create_region_and_connect(
        world,
        "Extra Problem Batch 1",
        "Starter Problems -> Extra Problem Batch 1",
        starter_problems,
        locations=loc_arrays[1],
    )
    batch_2 = create_region_and_connect(
        world,
        "Extra Problem Batch 2",
        "Extra Problem Batch 1 -> Extra Problem Batch 2",
        batch_1,
        locations=loc_arrays[2],
    )
    batch_3 = create_region_and_connect(
        world,
        "Extra Problem Batch 3",
        "Extra Problem Batch 2 -> Extra Problem Batch 3",
        batch_2,
        locations=loc_arrays[3],
    )
    batch_4 = create_region_and_connect(
        world,
        "Extra Problem Batch 4",
        "Extra Problem Batch 3 -> Extra Problem Batch 4",
        batch_3,
        locations=loc_arrays[4],
    )


def create_region(world: "ArchipelaCodeWorld", name: str, locations: list[LocData]) -> Region:
    reg = Region(name, world.player, world.multiworld)

    for data in locations:
        loc = ArchipelaCodeLocation(world.player, data[1], int(data[0]), reg)
        reg.locations.append(loc)

    world.multiworld.regions.append(reg)
    return reg


def create_region_and_connect(
    world: "ArchipelaCodeWorld",
    name: str,
    entrancename: str,
    connected_region: Region,
    locations: list[LocData],
    is_exit: bool = True,
) -> Region:
    reg: Region = create_region(world, name, locations)
    entrance_region: Region
    exit_region: Region

    if is_exit:
        entrance_region = connected_region
        exit_region = reg
    else:
        entrance_region = reg
        exit_region = connected_region

    entrance_region.connect(exit_region, entrancename)
    return reg
