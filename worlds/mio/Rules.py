from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING
from typing_extensions import override
from collections.abc import Iterable

from BaseClasses import Entrance, Location
from rule_builder.rules import Has, Rule, HasAll
from rule_builder.options import OptionFilter
from worlds.mio.DataProvider import RuleNode, WorldDataEvent, WorldDataLocation, WorldDataTransition

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart

from worlds.mio.Trinkets import save_flag_to_ap_name, ap_name_to_save_flag

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

@dataclasses.dataclass()
class UseMod(Rule["MIOWorld"], game="Memories in Orbit"):
    required_trinkets : tuple[str, ...]

    def __init__(
        self,
        required_trinkets: tuple[str, ...],
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.required_trinkets = tuple(sorted(set(required_trinkets)))

    @override
    def _instantiate(self, world: MIOWorld) -> Rule.Resolved:
        cost = 0
        for t in self.required_trinkets:
            cost += world.trinket_costs[ap_name_to_save_flag[t]]
        negative_items = tuple([(save_flag_to_ap_name[key], value) for key,value in world.trinket_costs.items() if value < 0])
        return self.Resolved(cost, self.required_trinkets, negative_items, player=world.player)

    class Resolved(Rule.Resolved):
        cost: int
        required_trinkets: tuple[str, ...]
        costs: tuple[tuple[str, int], ...]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            for trinket in self.required_trinkets:
                if not state.has(trinket, self.player):
                    return False
            return self.slot_sum(state, True) >= self.cost

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state and not self(state):
                missing = [t for t in self.required_trinkets if not state.has(t, self.player)]
                if len(missing) > 0:
                    return [
                        {"type": "text", "text": f"Missing {missing} with {self.slot_sum(state)}/{self.cost} slots"}
                    ]
                return [
                    {"type": "text", "text": f"Not enough slots: {self.slot_sum(state)}/{self.cost} slots"}
                ]
            elif state:
                return [
                    {"type": "text", "text": f"Have {self.required_trinkets} (which you do) and {self.slot_sum(state)}/{self.cost} slots"}
                ]
            else:
                return [
                    {"type": "text", "text": f"Have {self.required_trinkets} and {self.cost} slots"}
                ]


        def slot_sum(self, state: CollectionState, exit_early=False) -> int:
            best = 25
            for trinket, cost in self.costs:
                if state.has(trinket, self.player):
                    best -= cost
                    if best >= self.cost and exit_early: return best
            for s in [f"Modifier Slot Upgrade (#{i})" for i in range(1,8)]:
                if state.has(s, self.player):
                    best += 10
                    if best >= self.cost and exit_early: return best
            return best
