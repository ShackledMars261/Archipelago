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
