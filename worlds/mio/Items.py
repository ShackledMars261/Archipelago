from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from worlds.mio.DataProvider import DataProvider, WorldDataItem

if TYPE_CHECKING:
    from . import MIOWorld

# ITEM_NAME_TO_ID: dict[str, int] = {
# "Hairpin": 1,
# "Harvester": 2,
# "Dodge": 3,
# "Sail": 4,
# "Striders": 5,
# "Slingshot": 6,
# "Flowing Steps": 7,
# "Liquid Nacre": 8,
# "Crystal Nacre": 9,
# "Flash Memory - Connection Lost": 10,
# "Silo Access Badge": 11,
# }


def item_name_to_id(world: MIOWorld, name: str) -> int | None:
    items: list[WorldDataItem] = world.data_provider.data.items
    for item in items:
        if item.name == name:
            return item.id
    return None


def build_item_name_to_id_dict(data_provider: DataProvider) -> dict[str, int]:
    return {item.name: item.id for item in data_provider.data.items}


# DEFAULT_ITEM_CLASSIFICATIONS: dict[str, ItemClassification] = {
# "Hairpin": ItemClassification.progression,
# "Harvester": ItemClassification.progression,
# "Dodge": ItemClassification.progression,
# "Sail": ItemClassification.progression,
# "Striders": ItemClassification.progression,
# "Slingshot": ItemClassification.progression,
# "Flowing Steps": ItemClassification.progression,
# "Liquid Nacre": ItemClassification.filler,
# "Crystal Nacre": ItemClassification.filler,
# "Flash Memory - Connection Lost": ItemClassification.useful,
# "Silo Access Badge": ItemClassification.progression,
# }


def int_to_item_classification(value: int) -> ItemClassification:
    match value:
        case 0:
            return ItemClassification.filler
        case 1:
            return ItemClassification.progression
        case 2:
            return ItemClassification.useful
        case 4:
            return ItemClassification.trap
        case 8:
            return ItemClassification.skip_balancing
        case 16:
            return ItemClassification.deprioritized
        case 25:
            return ItemClassification.progression_deprioritized_skip_balancing
        case 9:
            return ItemClassification.progression_skip_balancing
        case 17:
            return ItemClassification.progression_deprioritized
        case _:
            return ItemClassification.progression


def item_name_to_classification(world: MIOWorld, name: str) -> ItemClassification | None:
    items: list[WorldDataItem] = world.data_provider.data.items
    for item in items:
        if item.name == name:
            return int_to_item_classification(item.classification)
    return None


def build_default_item_classifications_dict(data_provider: DataProvider) -> dict[str, ItemClassification]:
    return {item.name: int_to_item_classification(item.classification) for item in data_provider.data.items}


class MIOItem(Item):
    game = "Memories in Orbit"


def get_random_filler_item_name(world: MIOWorld) -> str:
    return ["Liquid Nacre", "Crystallized Nacre"][world.random.randint(0, 1)]


def create_item_with_correct_classification(world: MIOWorld, name: str) -> MIOItem:
    classification = item_name_to_classification(world, name) or ItemClassification.progression

    return MIOItem(name, classification, item_name_to_id(world, name), world.player)


def create_all_items(world: MIOWorld) -> None:
    itempool: list[Item] = [
        # world.create_item("Hairpin"),
        # world.create_item("Harvester"),
        # world.create_item("Dodge"),
        # world.create_item("Sail"),
        # world.create_item("Striders"),
        # world.create_item("Slingshot"),
        # world.create_item("Flowing Steps"),
        # world.create_item("Flash Memory - Connection Lost"),
        # world.create_item("Silo Access Badge"),
    ]

    items: list[WorldDataItem] = world.data_provider.data.items
    itempool.extend([world.create_item(item.name) for item in items])

    # append any conditional items here

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
