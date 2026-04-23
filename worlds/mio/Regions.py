from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from . import MIOWorld


def create_and_connect_regions(world: MIOWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: MIOWorld) -> None:
    # The Severed Spine
    ST_security_fall_P1 = Region("ST_security_fall_P1", world.player, world.multiworld)
    ST_security_fall_F1 = Region("ST_security_fall_F1", world.player, world.multiworld)
    ST_security_fall_S1 = Region("ST_security_fall_S1", world.player, world.multiworld)

    severed_spine_regions: list[Region] = [
        ST_security_fall_P1,
        ST_security_fall_F1,
        ST_security_fall_S1,
    ]

    # any conditional regions

    regions: list[Region] = [
        *severed_spine_regions,
    ]

    world.multiworld.regions += regions


def connect_regions(world: MIOWorld) -> None:
    # The Severed Spine
    ST_security_fall_P1 = world.get_region("ST_security_fall_P1")
    ST_security_fall_F1 = world.get_region("ST_security_fall_F1")
    ST_security_fall_S1 = world.get_region("ST_security_fall_S1")

    ST_security_fall_P1.connect(ST_security_fall_F1, "ST_security_fall_P1 to ST_security_fall_F1")
    ST_security_fall_F1.connect(ST_security_fall_S1, "ST_security_fall_F1 to ST_security_fall_S1")
