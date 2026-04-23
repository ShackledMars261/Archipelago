from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Toggle


class BossKillChecks(Toggle):
    """
    Bosses send a check when killed.
    """

    display_name = "Enable Boss Kill Checks"


class LogicDifficulty(Choice):
    """
    The difficulty you want to set the logic to.
    """

    display_name = "Logic Difficulty"

    option_intended = 0
    option_skips = 1
    option_glitches = 2

    default = option_intended


@dataclass
class MIOOptions(PerGameCommonOptions):
    logic_difficulty: LogicDifficulty
    boss_kill_checks: BossKillChecks


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [LogicDifficulty, BossKillChecks],
    ),
]

option_presets = {}
