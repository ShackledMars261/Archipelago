import typing
if typing.TYPE_CHECKING:
    from random import Random
else:
    Random = typing.Any

from random import Random
r = Random(15)
def get_trinket_costs(r: Random, mix: bool, pos: int, neg: int, neg_count: int) -> dict[str, int]:
    if mix and pos > -2 and neg > -2:
        if pos < 0 or neg < 0:
            neg_indices = r.sample(range(len(trinkets)), 7)
        else:
            neg_indices = r.sample(range(len(trinkets)), neg_count)
        neg_indices.sort(reverse = True)
        pos_trinkets = list(trinkets)
        neg_trinkets = []
        for n in neg_indices:
            neg_trinkets.append(pos_trinkets.pop(n))
    else:
        pos_trinkets = get_pos_trinkets()
        neg_trinkets = get_neg_trinkets()
    ps = distribute_costs(r, len(pos_trinkets), pos)
    ns = distribute_costs(r, len(neg_trinkets), neg)
    out = {}
    for k,v in zip(pos_trinkets, ps):
        out[k] = v
    for k,v in zip(neg_trinkets, ns):
        out[k] = -v
    return out

def distribute_costs(r: Random, n : int, total : int) -> list[int]:
    if n == 0: return []
    if total == -2:
        if n == len(get_neg_trinkets()): 
            return [-x for x in get_neg_costs()]
        return get_pos_costs()
    if total == -1:
        if n == len(get_neg_trinkets()):
            out = [-x for x in get_neg_costs()]
        else:
            out = get_pos_costs()
        r.shuffle(out)
        return out
    out = [0] * n
    for i in range(total):
        out[r.randint(0, n - 1)] += 1
    return out

def get_pos_trinkets() -> list[str]:
    return list(filter(lambda key: trinkets[key] > 0, trinkets.keys()))
def get_pos_costs() -> list[int]:
    return [trinkets[key] for key in get_pos_trinkets()]
def get_neg_trinkets() -> list[str]:
    return list(filter(lambda key: trinkets[key] < 0, trinkets.keys()))
def get_neg_costs() -> list[int]:
    return [trinkets[key] for key in get_neg_trinkets()]

def default_trinket_costs():
    return trinkets.copy()

trinkets = {
    "TRINKET:ANALYZER":             5,
    "TRINKET:FAST_RECOVERY":        5,
    "TRINKET:HUD":                  5,
    "TRINKET:KINETIC_CONVERSION":   5,
    "TRINKET:MAINTENANCE_EXPERT":   10,
    "TRINKET:MORE_SCRAPS":          10,
    "TRINKET:LOOT_SUPER_SCRAPS":    10,
    "TRINKET:ORB_RECOVERY":         10,
    "TRINKET:QUICK_RECHARGE":       10,
    "TRINKET:SHIELD_INC":           20,
    "TRINKET:COUNTER_ATTACK":       20,
    "TRINKET:STAGGER_ATTACK":       20,
    "TRINKET:BETTER_DODGE":         20,
    "TRINKET:FOUNTAIN_OVERLOAD":    20,
    "TRINKET:BIG_ENERGY_DRAIN":     20,
    "TRINKET:HEAVY_ATTACK":         20,
    "TRINKET:BERSERKER":            20,
    "TRINKET:HOOK_BERSERKER":       20,
    "TRINKET:DOUBLE_DAMAGES":       20,
    "TRINKET:ENERGY_EMPTY_ATTACK":  20,
    "TRINKET:GOO_REVENGE":          20,
    "TRINKET:LAST_CHANCE":          20,
    "TRINKET:SPIDER_BERSERKER":     20,
    "TRINKET:GLIDE_BERSERKER":      20,
    "TRINKET:DECOY":                30,
    "TRINKET:ORB_BLOCK":            30,
    "TRINKET:ALEXANDERS_FATE":      30,
    "TRINKET:SCRAP_ATTACK":         30,
    "TRINKET:TURBO_GLIDE":          30,
    "TRINKET:CARLO_HOOK":           30,
    "TRINKET:VAMPIRE":              30,
    "TRINKET:PACIFIC":              30,
    "TRINKET:GLIDE_STATIC":         40,
    "TRINKET:HOOK_SLASH":           40,
    "TRINKET:HEAL_GROUND":          40,
    "TRINKET:KURO_CHARM":          -5,
    "TRINKET:LESS_SCRAPS":         -5,
    "TRINKET:DRY_FOUNTAINS":       -15,
    "TRINKET:SHIELD_DEC":          -15,
    "TRINKET:SLOW_ENERGY":         -15,
    "TRINKET:DAREDEVIL":           -25,
    "TRINKET:GLASS_CANNON":        -35,
}

ap_name_to_save_flag = {
    "Modifier - Analyser":	"TRINKET:ANALYZER",
    "Modifier - Reduced Latency":	"TRINKET:FAST_RECOVERY",
    "Modifier - Self-Awareness":	"TRINKET:HUD",
    "Modifier - Pain Conversion":	"TRINKET:KINETIC_CONVERSION",
    "Modifier - Maintenance Hack":	"TRINKET:MAINTENANCE_EXPERT",
    "Modifier - Effective Dismantlement":	"TRINKET:MORE_SCRAPS",
    "Modifier - Portable Crystalliser":	"TRINKET:LOOT_SUPER_SCRAPS",
    "Modifier - Defragmentation":	"TRINKET:ORB_RECOVERY",
    "Modifier - The Heart's Favourite":	"TRINKET:QUICK_RECHARGE",
    "Modifier - Protective Overlay":	"TRINKET:SHIELD_INC",
    "Modifier - Counter Measures":	"TRINKET:COUNTER_ATTACK",
    "Modifier - High-voltage Discharge":	"TRINKET:STAGGER_ATTACK",
    "Modifier - Enhanced Dodge":	"TRINKET:BETTER_DODGE",
    "Modifier - High-Risk Voucher":	"TRINKET:FOUNTAIN_OVERLOAD",
    "Modifier - Energy Leecher":	"TRINKET:BIG_ENERGY_DRAIN",
    "Modifier - Kinetic Thrust":	"TRINKET:HEAVY_ATTACK",
    "Modifier - The Hand's Greed":	"TRINKET:BERSERKER",
    "Modifier - Wild Cat":	"TRINKET:HOOK_BERSERKER",
    "Modifier - Perfect State":	"TRINKET:DOUBLE_DAMAGES",
    "Modifier - Foolish Ideal":	"TRINKET:ENERGY_EMPTY_ATTACK",
    "Modifier - Defense Mechanism":	"TRINKET:GOO_REVENGE",
    "Modifier - Makeshift Recovery":	"TRINKET:LAST_CHANCE",
    "Modifier - Black Widow":	"TRINKET:SPIDER_BERSERKER",
    "Modifier - Bird of Prey":	"TRINKET:GLIDE_BERSERKER",
    "Modifier - Afterimage":	"TRINKET:DECOY",
    "Modifier - Splintering Dodge":	"TRINKET:ORB_BLOCK",
    "Modifier - Alexander's Fate":	"TRINKET:ALEXANDERS_FATE",
    "Modifier - Nacre Overload":	"TRINKET:SCRAP_ATTACK",
    "Modifier - Sunsail":	"TRINKET:TURBO_GLIDE",
    "Modifier - Glitch Trail":	"TRINKET:CARLO_HOOK",
    "Modifier - Extra-Coating Processor":	"TRINKET:VAMPIRE",
    "Modifier - Asma's Will":	"TRINKET:PACIFIC",
    "Modifier - Firefly":	"TRINKET:GLIDE_STATIC",
    "Modifier - Sharpened Hairpin":	"TRINKET:HOOK_SLASH",
    "Modifier - Gratitude":	"TRINKET:HEAL_GROUND",
    "Modifier - Imperfect Focus":	"TRINKET:KURO_CHARM",
    "Modifier - Resources Shortage":	"TRINKET:LESS_SCRAPS",
    "Modifier - Nacre Drought":	"TRINKET:DRY_FOUNTAINS",
    "Modifier - Thinner Frame":	"TRINKET:SHIELD_DEC",
    "Modifier - Split Process":	"TRINKET:SLOW_ENERGY",
    "Modifier - Oath to Ember":	"TRINKET:DAREDEVIL",
    "Modifier - Defective Core":	"TRINKET:GLASS_CANNON"
}

save_flag_to_ap_name = {
    "TRINKET:ANALYZER": "Modifier - Analyser",
    "TRINKET:FAST_RECOVERY": "Modifier - Reduced Latency",
    "TRINKET:HUD": "Modifier - Self-Awareness",
    "TRINKET:KINETIC_CONVERSION": "Modifier - Pain Conversion",
    "TRINKET:MAINTENANCE_EXPERT": "Modifier - Maintenance Hack",
    "TRINKET:MORE_SCRAPS": "Modifier - Effective Dismantlement",
    "TRINKET:LOOT_SUPER_SCRAPS": "Modifier - Portable Crystalliser",
    "TRINKET:ORB_RECOVERY": "Modifier - Defragmentation",
    "TRINKET:QUICK_RECHARGE": "Modifier - The Heart's Favourite",
    "TRINKET:SHIELD_INC": "Modifier - Protective Overlay",
    "TRINKET:COUNTER_ATTACK": "Modifier - Counter Measures",
    "TRINKET:STAGGER_ATTACK": "Modifier - High-voltage Discharge",
    "TRINKET:BETTER_DODGE": "Modifier - Enhanced Dodge",
    "TRINKET:FOUNTAIN_OVERLOAD": "Modifier - High-Risk Voucher",
    "TRINKET:BIG_ENERGY_DRAIN": "Modifier - Energy Leecher",
    "TRINKET:HEAVY_ATTACK": "Modifier - Kinetic Thrust",
    "TRINKET:BERSERKER": "Modifier - The Hand's Greed",
    "TRINKET:HOOK_BERSERKER": "Modifier - Wild Cat",
    "TRINKET:DOUBLE_DAMAGES": "Modifier - Perfect State",
    "TRINKET:ENERGY_EMPTY_ATTACK": "Modifier - Foolish Ideal",
    "TRINKET:GOO_REVENGE": "Modifier - Defense Mechanism",
    "TRINKET:LAST_CHANCE": "Modifier - Makeshift Recovery",
    "TRINKET:SPIDER_BERSERKER": "Modifier - Black Widow",
    "TRINKET:GLIDE_BERSERKER": "Modifier - Bird of Prey",
    "TRINKET:DECOY": "Modifier - Afterimage",
    "TRINKET:ORB_BLOCK": "Modifier - Splintering Dodge",
    "TRINKET:ALEXANDERS_FATE": "Modifier - Alexander's Fate",
    "TRINKET:SCRAP_ATTACK": "Modifier - Nacre Overload",
    "TRINKET:TURBO_GLIDE": "Modifier - Sunsail",
    "TRINKET:CARLO_HOOK": "Modifier - Glitch Trail",
    "TRINKET:VAMPIRE": "Modifier - Extra-Coating Processor",
    "TRINKET:PACIFIC": "Modifier - Asma's Will",
    "TRINKET:GLIDE_STATIC": "Modifier - Firefly",
    "TRINKET:HOOK_SLASH": "Modifier - Sharpened Hairpin",
    "TRINKET:HEAL_GROUND": "Modifier - Gratitude",
    "TRINKET:KURO_CHARM": "Modifier - Imperfect Focus",
    "TRINKET:LESS_SCRAPS": "Modifier - Resources Shortage",
    "TRINKET:DRY_FOUNTAINS": "Modifier - Nacre Drought",
    "TRINKET:SHIELD_DEC": "Modifier - Thinner Frame",
    "TRINKET:SLOW_ENERGY": "Modifier - Split Process",
    "TRINKET:DAREDEVIL": "Modifier - Oath to Ember",
    "TRINKET:GLASS_CANNON": "Modifier - Defective Core"
}
