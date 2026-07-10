from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from worlds.mio.DataProvider import WorldDataRoom, WorldDataTransition

if TYPE_CHECKING:
    from . import MIOWorld


def create_and_connect_regions(world: MIOWorld) -> None:
    create_all_regions(world)
    connect_regions(world)
    # visualize_regions(world.get_region("ST_security_fall_P1"), "mio.puml")


def create_all_regions(world: MIOWorld) -> None:
    # The Severed Spine
    # ST_security_fall_P1 = Region("ST_security_fall_P1", world.player, world.multiworld)
    # ST_security_fall_P2 = Region("ST_security_fall_P2", world.player, world.multiworld)
    # ST_security_fall_F1 = Region("ST_security_fall_F1", world.player, world.multiworld)
    # ST_security_fall_S1 = Region("ST_security_fall_S1", world.player, world.multiworld)
    # ST_security_view = Region("ST_security_view", world.player, world.multiworld)
    # ST_security_transi_P1 = Region("ST_security_transi_P1", world.player, world.multiworld)
    # HUB_hub_central_C1 = Region("HUB_hub_central_C1", world.player, world.multiworld)
    # HUB_hub_central = Region("HUB_hub_central", world.player, world.multiworld)
    # HUB_hub_shop = Region("HUB_hub_shop", world.player, world.multiworld)
    # HUB_hub_shop_S1 = Region("HUB_hub_shop_S1", world.player, world.multiworld)

    # severed_spine_regions: list[Region] = [
    # ST_security_fall_P1,
    # ST_security_fall_P2,
    # ST_security_fall_F1,
    # ST_security_fall_S1,
    # ST_security_view,
    # ST_security_transi_P1,
    # HUB_hub_central_C1,
    # HUB_hub_central,
    # HUB_hub_shop,
    # HUB_hub_shop_S1,
    # ]

    # any conditional regions

    regions: list[Region] = [
        # *severed_spine_regions
    ]

    rooms: list[WorldDataRoom] = world.data_provider.data.rooms

    regions.extend([Region(room.name, world.player, world.multiworld) for room in rooms])

    world.multiworld.regions += regions


def connect_regions(world: MIOWorld) -> None:
    # The Severed Spine
    # ST_security_fall_P1: Region = world.get_region("ST_security_fall_P1")
    # ST_security_fall_P2 = world.get_region("ST_security_fall_P2")
    # ST_security_fall_F1 = world.get_region("ST_security_fall_F1")
    # ST_security_fall_S1 = world.get_region("ST_security_fall_S1")
    # ST_security_view = world.get_region("ST_security_view")
    # ST_security_transi_P1 = world.get_region("ST_security_transi_P1")
    # HUB_hub_central_C1 = world.get_region("HUB_hub_central_C1")
    # HUB_hub_central = world.get_region("HUB_hub_central")
    # HUB_hub_shop = world.get_region("HUB_hub_shop")
    # HUB_hub_shop_S1 = world.get_region("HUB_hub_shop_S1")

    # ST_security_fall_P1.connect(ST_security_fall_F1, "ST_security_fall_P1 to ST_security_fall_F1")
    # ST_security_fall_P1.connect(ST_security_fall_P2, "ST_security_fall_P1 to ST_security_fall_P2")
    # ST_security_fall_F1.connect(ST_security_fall_S1, "ST_security_fall_F1 to ST_security_fall_S1")
    # ST_security_fall_F1.connect(ST_security_view, "ST_security_fall_F1 to ST_security_view")
    # ST_security_view.connect(ST_security_transi_P1, "ST_security_view to ST_security_transi_P1")
    # ST_security_transi_P1.connect(HUB_hub_central_C1, "ST_security_transi_P1 to HUB_hub_central_C1")
    # HUB_hub_central_C1.connect(HUB_hub_central, "HUB_hub_central_C1 to HUB_hub_central")
    # HUB_hub_central.connect(HUB_hub_shop, "HUB_hub_central to HUB_hub_shop")
    # HUB_hub_central.connect(HUB_hub_shop_S1, "HUB_hub_central to HUB_hub_shop_S1")
    # HUB_hub_shop.connect(HUB_hub_shop_S1, "HUB_hub_shop to HUB_hub_shop_S1")

    transitions: list[WorldDataTransition] = world.data_provider.data.transitions

    for transition in transitions:
        from_region: Region = world.get_region(transition.fromName)
        to_region: Region = world.get_region(transition.toName)
        from_region.connect(to_region, transition.name)
