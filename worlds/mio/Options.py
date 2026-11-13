from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Toggle, Range


class BossKillChecks(Toggle):
    """
    Bosses send a check when killed. CURRENTLY UNIMPLEMENTED!!!
    """

    display_name = "Enable Boss Kill Checks (CURRENTLY UNIMPLEMENTED)"


class LogicDifficulty(Choice):
    """
    The difficulty of the logic for traversing the world.
    - intended: Logic assumes primarily techniques used in
        the base game.
    - simple skips: Logic assumes everything intended as
        well as many skips considered to be straightforward
        to learn and execute.
    - advanced skips: Logic assumes nearly any known technique,
        or skip, with the exception of most flower warps.
    NOTE: simple skips and advanced skips logic levels should
        be considered experimental (moreso than the rest of
        the randomizer)
    """

    display_name = "Logic Difficulty"

    option_intended = 0
    option_simple_skips = 1
    option_advanced_skips = 2

    default = option_intended

class BossDifficulty(Choice):
    """
    The difficulty of logic for bosses. The exact requirements vary for each
    difficulty and boss.
    - intended: Logic assumes primarily what would be available and used
        commonly.
    - difficult: Logic assumes fewer useful items for bosses.
    - possible: Logic assumes only the theoretical minimum loadout for bosses to
        be defeated hitless.

    NOTE: randomizing Slash and enabling "Slashless Combat" will make even
        intended logic more difficult.

    NOTE: difficult and possible boss difficulty levels should be considered
        experimental (moreso than the rest of the randomizer)
    """

    display_name = "Boss Difficulty"

    option_intended = 0
    option_difficult = 1
    option_possible = 2

    default = option_intended

class RandomizeStartingItems(Toggle):
    """
    When disabled, Slash and Self-Awareness are always found at their vanilla
    starting locations instead of being randomized like other items.
    """

    display_name = "Randomize Starting Items"

class SlashlessCombat(Toggle):
    """
    Does nothing when "Randomize Starting Items" is disabled.

    When enabled, logic will not require Slash except where a combat scenario is
    not completable otherwise.  When disabled, logic will not assume anything to
    be killable without Slash.
    """

    display_name = "Allow Slashless Combat"

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

class AirstallLevel(Choice):
    """
    Applies to simple skips
    - none: airstalling is logically disabled
    - airstalling: attacking mid-air to reset vertical momentum
        - may require other items such as dodge situationally
    - crystal stall: in addition to airstalling for distance require airstalling
        in place long enough to hit a single crystal/flower/ bomb multiple times
        to gain additional height
    - wall climb: in addition to crystal stalling, airstalling against a steeply
        sloped surface may be required to gain additional height

    NOTE: Some skips may not have been properly categorized in the logic writing
        process. If you have disabled a skip and it appears to be logically
        required, please report this as a bug!
    """
    display_name = "Airstalling"
    option_none = 0
    option_airstalling = 1
    option_crystal_stall = 2
    option_wall_climb = 3
    default = option_crystal_stall

class EnemyPogoLevel(Choice):
    """
    Applies to simple and advanced skips
    - none: enemy pogo's are not logically required
    - pogo: slashing enemies to reset jumps and gain height may be logically
        required
    - lure: luring enemys far away from their starting location to pogo them
        where there would otherwise be no enemies may be required (advanced
        skips only)

    NOTE: Some skips may not have been properly categorized in the logic writing
        process. If you have disabled a skip and it appears to be logically
        required, please report this as a bug!
    """
    display_name = "Enemy Pogos"
    option_none = 0
    option_pogo = 1
    option_lure = 2
    default = option_pogo

class MovementLevel(Choice):
    """
    Applies to simple skips and advanced skips
    - none: little to no movement tech required logically
    - general: movement tech which is easy to learn and useful practically
        anywhere may be logically required
        - ground pogos: striking the ground immediately prior to a jump slightly
            increases jump height
        - super spring: jumping upon walking into a bumper increases the bounce
            height without consuming your double jump
        - stroost: using dodge while stridering gives the player a boost in
            speed allowing you to move further before running out of energy
        - strider triple: holding up, then holding striders and jumping at the
            right time greatly increases jump height without consuming energy
    - situational: general movement as well as tech which is more difficult to
        learn/master and is less prevelant in logic requirements
        - slope boost: downward diving into a sloped surface can give Mio a lot
            of horizontal momentum such as in the bunker door skip with only
            striders (and no slash)
        - hairpin launch: releasing hairpin at the right moment can give Mio an
            extra powerful boost in the direction of the hairpin
    - tedious: situational movement which may be difficult to replicate and come
        at high risk
        - laser_skip: in certain situations Mio can pass through lasers by
            timing a chained attack properly

    NOTE: Some skips may not have been properly categorized in the logic writing
        process. If you have disabled a skip and it appears to be logically
        required, please report this as a bug!
    """
    display_name = "Movement Tech"
    option_none = 0
    option_general = 1
    option_situational = 2
    option_tedious = 3
    default = option_general

class HazardSkips(Toggle):
    """
    Applies to simple skips
    If enabled logic may require standing or respawning in areas which look
    unsafe, or using striders on solid surfaces which are covered in hazards

    NOTE: Some skips may not have been properly categorized in the logic writing
        process. If you have disabled a skip and it appears to be logically
        required, please report this as a bug!
    """
    display_name = "Hazard Respawn and Stridering"


class FlowerWarps(Toggle):
    """
    Applies to advanced skips
    If enabled logic may require using flower warps
    NOTE: almost none of the known flower warps are implemented logically
    """
    display_name = "Flower Warps"



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



class Modsanity(Toggle):
    """
    Whether costs of specific trinkets should be randomized. If disabled, all
    options in this section are ignored.
    """
    display_name = "Modsanity"
    default = False

class MixPositiveNegative(Toggle):
    """
    If enabled, modifiers which have positive cost in the base game will be
    randomized in the same pool with modifiers which usually have negative cost.
    If disabled, positive cost modifiers and negative cost modifiers will be
    randomized in separate pools. Negative cost modifiers will not be given
    positive costs and vice versa.
    This option is ignored if either of "Total Positive Modifier Cost" and
    "Total Negative Modifier Cost" is set to -2 or unshuffled.
    """

    display_name = "Mix Positive and Negative Modifiers"
    default = False


class NegativeModifierCount(Range):
    """
    The number of modifiers which will be given negative costs. Ignored if
    either of "Total Positive Modifer Cost" and "Total Negative Modifier Cost"
    is set to -1 or -2 (vanilla costs are used).
    """

    display_name = "Negative Modifier Count"
    range_start = 0
    range_end = 42
    default = 7


class TotalPositiveModiferCost(Range):
    """
    The modifier slot cost of all positive modifiers. Vanilla is 730 and without
    negative modifiers you can have up to 95 slots.
    If "Mix Positive and Negative Modifiers" is enabled, this is the sum of
    costs of all modifiers with positive cost.
    Set to -1 or shuffle to shuffle the vanilla costs to different modifiers.
    Set to -2 or unshuffle to assign the original cost to all positive
    modifiers.
    """

    display_name = "Total Positive Modifier Cost"
    special_range_names = {
        "shuffle": -1,
        "unshuffled": -2
    }
    range_start = 0
    range_end = 2000
    default = 730


class TotalNegativeModiferCost(Range):
    """
    The negative of the sum of slot costs of all negative modifiers. Vanilla is
    115.
    If "Mix Positive and Negative Modifiers" is enabled, this is the sum of
    costs of all modifiers with negative cost.
    Set to -1 or shuffle to shuffle the vanilla costs to different modifiers.
    Set to -2 or unshuffle to assign the original cost to all positive
    modifiers.
    """

    display_name = "Total negative Modifier Cost"
    special_range_names = {
        "shuffle": -1,
        "unshuffled": -2
    }
    range_start = 0
    range_end = 2000
    default = 115


@dataclass
class MIOOptions(PerGameCommonOptions):
    logic_difficulty: LogicDifficulty
    boss_difficulty: BossDifficulty
    boss_kill_checks: BossKillChecks
    randomize_starting_items: RandomizeStartingItems
    slashless_combat: SlashlessCombat
    starting_room: StartingRoom
    fast_travel_unlock: FastTravelUnlock

    movement_level: MovementLevel
    airstall_level: AirstallLevel
    enemy_pogo_level: EnemyPogoLevel
    hazard_skips: HazardSkips
    flower_warps: FlowerWarps

    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
    death_link_grace: DeathLinkGrace
    knockback_link: KnockbackLink
    damage_link: DamageLink

    modsanity: Modsanity
    mix_positive_negative: MixPositiveNegative
    negative_modifier_count: NegativeModifierCount
    total_positive_modifier_cost: TotalPositiveModiferCost
    total_negative_modifier_cost: TotalNegativeModiferCost

mio_option_groups = [
    OptionGroup(
        "Game Options",
        [LogicDifficulty, BossDifficulty, BossKillChecks, RandomizeStartingItems, SlashlessCombat, StartingRoom, FastTravelUnlock],
    ),
    OptionGroup(
        "Skip Settings",
        [MovementLevel, AirstallLevel, EnemyPogoLevel, HazardSkips, FlowerWarps]
    ),
    OptionGroup(
        "Links (Protocols)",
        [DeathLink, DeathLinkAmnesty, DeathLinkGrace, KnockbackLink, DamageLink],
    ),
    OptionGroup(
        "Modsanity",
        [Modsanity, MixPositiveNegative, NegativeModifierCount, TotalPositiveModiferCost, TotalNegativeModiferCost,],
    )
]

option_presets = {}
