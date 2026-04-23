from __future__ import annotations

from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import MIOWorld


def set_all_rules(world: MIOWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: MIOWorld) -> None:
    f1_to_s1 = world.get_entrance("ST_security_fall_F1 to ST_security_fall_S1")

    set_rule(f1_to_s1, lambda state: state.has("Sail"))


def set_all_location_rules(world: MIOWorld) -> None:
    pass


def set_completion_condition(world: MIOWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
