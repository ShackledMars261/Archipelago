from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from Options import Choice, OptionGroup, Range, StartInventoryPool
from worlds.AutoWorld import PerGameCommonOptions

if TYPE_CHECKING:
    from . import ArchipelaCodeWorld


def create_options_groups() -> list[OptionGroup]:
    option_group_list: list[OptionGroup] = []
    for name, options in apcode_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list


def adjust_options(world: "ArchipelaCodeWorld"):
    pass


class EndGoal(Range):
    """The percentage of problems needed to be completed in order to \"win\" the game."""

    display_name = "End Goal"
    range_start = 1
    range_end = 100
    default = 60


class TotalProblemCount(Range):
    """How many total problems to include."""

    display_name = "Total Problems"
    range_start = 10
    range_end = 200
    default = 50


# class FreebieCheckCount(Range):
#     """How many free checks to give out. Highly recommended to have at least a few."""

#     display_name = "Freebie Check Count"
#     range_start = 0
#     range_end = 10
#     default = 3


class LanguageChoice(Choice):
    """Which programming language you want to use. Multi-language support will be added in the future.
    CURRENTLY ONLY PYTHON IS SUPPORTED!!! (JS will be added in v0.0.2, more to follow in later versions)"""

    display_name = "Language Choice"
    option_python = 0
    option_javascript = 1
    option_typescript = 2
    option_golang = 3
    default = 0


# PLANNED OPTIONS:
# class EnablePython(DefaultOnToggle):
# """Whether or not to include the Python language."""
# display_name = "Enable Python"
#
# class EnableJavascript(Toggle):
# """Whether or not to include the Javascript language."""
# display_name = "Enable Javascript"
#
# class EnableTypescript(Toggle):
# """Whether or not to include the Typescript language."""
# display_name = "Enable Typescript"
#
# class EnableGolang(Toggle):
# """Whether or not to include the Golang language."""
# display_name = "Enable Golang"
#
# class EnableUniversalLanguageFeatures(Toggle):
# """Whether or not to unlock features for all languages, rather than specific ones. Example: \"Universal if statements\" vs. \"Python if statements\""""
# display_name = "Enable Universal Language Features"
#
# class EnableRestrictiveProblems(Toggle):
# """Whether or not to force you into a specific random language for every problem."""
# display_name = "Enable Restrictive Problems"


@dataclass
class APCodeOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool

    EndGoal: EndGoal

    TotalProblemCount: TotalProblemCount
    # FreebieCheckCount: FreebieCheckCount

    LanguageChoice: LanguageChoice

    # PLANNED OPTIONS:
    # EnableUniversalLanguageFeatures: EnableUniversalLanguageFeatures
    # EnableRestrictiveProblems: EnableRestrictiveProblems
    # EnablePython: EnablePython
    # EnableJavascript: EnableJavascript
    # EnableTypescript: EnableTypescript
    # EnableGolang: EnableGolang


apcode_option_groups: dict[str, list[Any]] = {}
