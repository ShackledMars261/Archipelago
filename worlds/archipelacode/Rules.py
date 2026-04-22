import math
from typing import TYPE_CHECKING

from worlds.AutoWorld import CollectionState
from worlds.generic.Rules import add_rule

from .Items import get_item_name_from_id, item_frequencies

if TYPE_CHECKING:
    from . import ArchipelaCodeWorld


def check_if_location_is_available(
    world: "ArchipelaCodeWorld", state: CollectionState, required_features: dict[str, list[int]]
) -> bool:
    # print(required_features)
    # result = any(
    # all(state.has(get_item_name_from_id(item_id), world.player) for item_id in lang_features)
    # for lang_features in required_features.values()
    # )

    results: dict[str, bool] = {}
    missing_items: list[str] = []

    for slug, lang_features in required_features.items():
        for language in world.included_languages:
            for lang_slug in language.langSlugs:
                if slug == lang_slug:
                    results[slug] = True
                    for item_id in lang_features:
                        if not state.has(get_item_name_from_id(item_id), world.player):
                            missing_items.append(get_item_name_from_id(item_id))
                            results[slug] = False

    # print(missing_items)
    # print(results)

    return any(results.values())


def has_reached_goal(world: "ArchipelaCodeWorld", state: CollectionState) -> bool:
    required_problems: int = round(
        float(world.options.EndGoal.value) * float(world.options.TotalProblemCount.value) / 100.0
    )
    return len(state.locations_checked) >= required_problems


def set_custom_rules(world: "ArchipelaCodeWorld") -> None:
    for language in world.included_languages:
        for location in world.included_locations:
            if (
                language.langSlugs[0] in location.required_features.keys()
            ):  # probably need to remove language.langSlugs[0]
                features_count: int = 0
                for feature_id in location.required_features[
                    language.langSlugs[0]
                ]:  # probably need to remove language.langSlugs[0]
                    add_rule(
                        world.multiworld.get_location(location.name, world.player),
                        lambda state, fid=feature_id: state.has(get_item_name_from_id(fid), world.player),
                    )
                    features_count += 1
            # print(f"Problem {location.name} has {features_count} required features")


def set_rules(world: "ArchipelaCodeWorld") -> None:
    add_rule(
        world.multiworld.get_entrance("Starter Problems -> Extra Problem Batch 1", world.player),
        lambda state: state.has("Progressive Problem Unlock", world.player, 1),
    )
    add_rule(
        world.multiworld.get_entrance("Extra Problem Batch 1 -> Extra Problem Batch 2", world.player),
        lambda state: state.has("Progressive Problem Unlock", world.player, 2),
    )
    add_rule(
        world.multiworld.get_entrance("Extra Problem Batch 2 -> Extra Problem Batch 3", world.player),
        lambda state: state.has("Progressive Problem Unlock", world.player, 3),
    )
    add_rule(
        world.multiworld.get_entrance("Extra Problem Batch 3 -> Extra Problem Batch 4", world.player),
        lambda state: state.has("Progressive Problem Unlock", world.player, 4),
    )

    # for location in world.included_locations:
    # add_rule(
    # world.multiworld.get_location(location.name, world.player),
    # lambda state: check_if_location_is_available(world, state, location.required_features),
    # )
    set_custom_rules(world)

    # world.multiworld.completion_condition[world.player] = lambda state: has_reached_goal(world, state)

    # Uncomment the next 2 lines in order to generate a PlantUML file that graphs the regions
    # from Utils import visualize_regions
    # visualize_regions(world.multiworld.get_region("Starter Problems", world.player), "archipelacode.puml")


def calculate_possible_problem_count(state: CollectionState, world: "ArchipelaCodeWorld", player: int) -> int:
    unlock_count: int = state.count("Progressive Problem Unlock", player)
    unlock_percentage: float = float(1 + unlock_count) / float(1 + item_frequencies["Progressive Problem Unlock"])
    unlocked_problem_count: int = round(unlock_percentage * float(world.options.TotalProblemCount))
    return unlocked_problem_count


def set_completion_rules(world: "ArchipelaCodeWorld", player: int) -> None:
    world.multiworld.completion_condition[player] = lambda state: (
        calculate_possible_problem_count(state, world, player)
        >= math.floor(float(world.options.EndGoal) * float(world.options.TotalProblemCount) / 100.0)
    )


"""
required_problem_count: int = math.floor(
    float(world.options.EndGoal) * float(world.options.TotalProblemCount) / 100.0
)
"""
