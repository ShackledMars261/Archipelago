from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

from BaseClasses import Entrance, Location
from rule_builder.rules import Has, Rule
from worlds.mio.DataProvider import RuleNode, WorldDataEvent, WorldDataLocation, WorldDataTransition

if TYPE_CHECKING:
    from . import MIOWorld


def set_all_rules(world: MIOWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def rule_from_node(world: MIOWorld, node: RuleNode) -> Rule:
    return world.rule_from_dict(dataclasses.asdict(node))


def set_all_entrance_rules(world: MIOWorld) -> None:
    transitions: list[WorldDataTransition] = world.data_provider.data.transitions
    for transition in transitions:
        if transition.requirements is None:
            continue
        entrance: Entrance = world.get_entrance(transition.name)
        world.set_rule(entrance, rule_from_node(world, transition.requirements))


def _get_location(world: MIOWorld, name: str) -> Location | None:
    # Not every location in the data is necessarily created this generation
    # (e.g. rooms not yet wired into the region graph), so a miss here isn't
    # an error - just nothing to set a rule on.
    try:
        return world.get_location(name)
    except KeyError:
        return None


def set_all_location_rules(world: MIOWorld) -> None:
    locations: list[WorldDataLocation] = world.data_provider.data.locations
    for location in locations:
        if location.requirements is None:
            continue
        ap_location: Location | None = _get_location(world, location.name)
        if ap_location is not None:
            world.set_rule(ap_location, rule_from_node(world, location.requirements))

    events: list[WorldDataEvent] = world.data_provider.data.events
    for event in events:
        if event.requirements is None:
            continue
        ap_location: Location | None = _get_location(world, event.locationName)
        if ap_location is not None:
            world.set_rule(ap_location, rule_from_node(world, event.requirements))


def set_completion_condition(world: MIOWorld) -> None:
    world.set_completion_rule(Has("Ati Defeated"))
