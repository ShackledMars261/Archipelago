from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

class BossKillChecks(Toggle):
    """
    Bosses send a check when killed.
    """
    
    display_name = "Enable Boss Kill Checks"
    
@dataclass
class MIOOptions(PerGameCommonOptions):
    boss_kill_checks: BossKillChecks
    
option_groups = [
    OptionGroup(
      "Gameplay Options",
      [BossKillChecks],  
    ),
]

option_presets = {}