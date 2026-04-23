from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has

if TYPE_CHECKING:
    from . import MIOWorld


def set_all_rules(world: MIOWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: MIOWorld) -> None:
    f1_to_s1 = world.get_entrance("ST_security_fall_F1 to ST_security_fall_S1")

    has_sail = Has("Sail")

    world.set_rule(f1_to_s1, has_sail)


def set_all_location_rules(world: MIOWorld) -> None:
    can_defeat_ati = Has("Hairpin")

    ati_defeated = world.get_location("Ati Defeated")

    world.set_rule(ati_defeated, can_defeat_ati)


def set_completion_condition(world: MIOWorld) -> None:
    world.set_completion_rule(Has("Victory"))
