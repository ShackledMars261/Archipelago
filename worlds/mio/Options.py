from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Toggle, Range


class BossKillChecks(Toggle):
    """
    Bosses send a check when killed. CURRENTLY UNIMPLEMENTED!!!
    """

    display_name = "Enable Boss Kill Checks (CURRENTLY UNIMPLEMENTED)"


class LogicDifficulty(Choice):
    """
    The difficulty you want to set the logic to. CURRENTLY UNIMPLEMENTED!!!
    """

    display_name = "Logic Difficulty (CURRENTLY UNIMPLEMENTED)"

    option_intended = 0
    option_skips = 1
    option_glitches = 2

    default = option_intended


class RandomizeStartingItems(Toggle):
    """
    When disabled, Slash and Self-Awareness are always found at their vanilla
    starting locations instead of being randomized like other items.
    """

    display_name = "Randomize Starting Items"


class StartingRoom(Choice):
    """
    Start the game from a different room than usual.
    """

    display_name = "Starting Room"
    option_ST_security_fall_P1 = 0
    option_LQ_city_hall_C2 = 1
    option_GA_vin_terrace_P3 = 2
    option_LQ_vin_intro = 3
    option_GA_root_conex_P2 = 4
    default = 0


class FastTravelUnlock(Toggle):
    """
    If enabled, receiving a torn overseer will also unlock teleporting to it
    through the overseer network even if you haven't sat at the corresponding
    overseer previously.
    If disabled, torn overseers behave as in vanilla.

    NOTE: Logic currently does not consider fast travel unlocked by this
        setting.
    """

    display_name = "Fast Travel Unlock"
    default = True


class DeathLink(Toggle):
    """
    Toggles DeathLink for this player.
    """

    display_name = "DeathLink"
    default = False


class DeathLinkAmnesty(Range):
    """
    The amount of deaths needed to send a DeathLink.
    """

    display_name = "DeathLink Amnesty"
    range_start = 1
    range_end = 20
    default = 1


class DeathLinkGrace(Range):
    """
    The amount of DeathLinks required for mio to die.
    """

    display_name = "DeathLink Grace"
    range_start = 1
    range_end = 20
    default = 1


class KnockbackLink(Toggle):
    """
    Toggles KnockbackLink for the player.
    This implementation currently does not send it, only receives.
    """

    display_name = "KnockbackLink"
    default = False


class DamageLink(Toggle):
    """
    Toggles DamageLink for the player.
    DamageLink will only take away shields, and won't count death as one to send.
    """

    display_name = "DamageLink"
    default = False


@dataclass
class MIOOptions(PerGameCommonOptions):
    logic_difficulty: LogicDifficulty
    boss_kill_checks: BossKillChecks
    randomize_starting_items: RandomizeStartingItems
    starting_room: StartingRoom
    fast_travel_unlock: FastTravelUnlock

    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
    death_link_grace: DeathLinkGrace
    knockback_link: KnockbackLink
    damage_link: DamageLink


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [LogicDifficulty, BossKillChecks, RandomizeStartingItems, StartingRoom, FastTravelUnlock],
    ),
    OptionGroup(
        "Links (Protocols)",
        [DeathLink, DeathLinkAmnesty, DeathLinkGrace, KnockbackLink, DamageLink],
    ),
]

option_presets = {}
