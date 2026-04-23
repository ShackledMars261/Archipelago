from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import MIOWorld

ITEM_NAME_TO_ID: dict[str, int] = {
    "Hairpin": 0,
    "Harvester": 1,
    "Dodge": 2,
    "Sail": 3,
    "Striders": 4,
    "Slingshot": 5,
    "Flowing Steps": 6,
    "Random Amount of Liquid Nacre": 7,
}

DEFAULT_ITEM_CLASSIFICATIONS: dict[str, ItemClassification] = {
    "Hairpin": ItemClassification.progression,
    "Harvester": ItemClassification.progression,
    "Dodge": ItemClassification.progression,
    "Sail": ItemClassification.progression,
    "Striders": ItemClassification.progression,
    "Slingshot": ItemClassification.progression,
    "Flowing Steps": ItemClassification.progression,
    "Random Amount of Liquid Nacre": ItemClassification.filler,
}


class MIOItem(Item):
    game = "Memories in Orbit"


def get_random_filler_item_name(world: MIOWorld) -> str:
    return "Random Amount of Liquid Nacre"  # filler item name, change this


def create_item_with_correct_classification(world: MIOWorld, name: str) -> MIOItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return MIOItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: MIOWorld) -> None:
    itempool: list[Item] = [
        world.create_item("Hairpin"),
        world.create_item("Harvester"),
        world.create_item("Dodge"),
        world.create_item("Sail"),
        world.create_item("Striders"),
        world.create_item("Slingshot"),
        world.create_item("Flowing Steps"),
    ]

    # append any conditional items here

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
