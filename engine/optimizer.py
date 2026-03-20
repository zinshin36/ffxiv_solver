import itertools
import time

# -------------------------
# CONSTANTS (Balance-like)
# -------------------------
LEVEL_MAIN = 390
LEVEL_SUB = 400
LEVEL_DIV = 1900

# -------------------------
# SAFE STAT GET
# -------------------------
def get_stat(stats, key):
    if not stats:
        return 0
    return stats.get(key, 0)

# -------------------------
# GCD CALC (REAL FORMULA)
# -------------------------
def compute_gcd(sps):
    base = 2.5
    gcd = base * (1000 - (130 * (sps - LEVEL_SUB) / LEVEL_DIV)) / 1000
    return round(gcd, 3)

# -------------------------
# CRIT
# -------------------------
def crit_rate(crit):
    return (200 * (crit - LEVEL_SUB) / LEVEL_DIV + 50) / 1000

def crit_damage(crit):
    return (1400 + (200 * (crit - LEVEL_SUB) / LEVEL_DIV)) / 1000

# -------------------------
# DH
# -------------------------
def dh_rate(dh):
    return (550 * (dh - LEVEL_SUB) / LEVEL_DIV) / 1000

# -------------------------
# DET
# -------------------------
def det_multi(det):
    return (140 * (det - LEVEL_MAIN) / LEVEL_DIV + 1000) / 1000

# -------------------------
# SPEED MULTI
# -------------------------
def speed_multi(sps):
    return (1000 + (130 * (sps - LEVEL_SUB) / LEVEL_DIV)) / 1000

# -------------------------
# DPS MODEL (Balance-like)
# -------------------------
def compute_dps(stats):

    crit = get_stat(stats, "crit")
    dh = get_stat(stats, "dh")
    det = get_stat(stats, "det")
    sps = get_stat(stats, "sps")
    intel = get_stat(stats, "int")

    cr = crit_rate(crit)
    cd = crit_damage(crit)
    dr = dh_rate(dh)
    dm = det_multi(det)
    sm = speed_multi(sps)

    # Expected damage multiplier
    dmg = intel * dm * sm

    # crit + dh expected value
    dmg *= (1 + cr * (cd - 1))
    dmg *= (1 + dr * 0.25)

    return dmg

# -------------------------
# APPLY FOOD
# -------------------------
def apply_food(stats, food):

    if not food:
        return stats

    result = stats.copy()

    for stat, (pct, cap) in food.items():
        base = result.get(stat, 0)
        bonus = min(int(base * pct), cap)
        result[stat] = base + bonus

    return result

# -------------------------
# APPLY MATERIA (WITH OVERMELD)
# -------------------------
MATERIA_VALUES = {
    "crit": 36,
    "dh": 36,
    "det": 36,
    "sps": 36
}

def apply_materia(item):

    if not item:
        return None, []

    stats = item["stats"].copy()

    base_slots = item.get("materia_slots", 0)

    # assume crafted = can overmeld
    overmeld_slots = 2 if item.get("ilvl", 0) < 790 else 0

    total_slots = base_slots + overmeld_slots

    melds = []

    for _ in range(total_slots):
        # prioritize crit > det > dh > sps
        best = max(stats, key=lambda k: stats[k] if k in MATERIA_VALUES else -1)

        if best in MATERIA_VALUES:
            stats[best] += MATERIA_VALUES[best]
            melds.append(f"{best}+{MATERIA_VALUES[best]}")

    return stats, melds

# -------------------------
# BUILD EVAL
# -------------------------
def evaluate_build(build, food, target_gcd):

    total = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}
    melds_output = {}

    for slot, item in build.items():

        if not item:
            return None

        stats, melds = apply_materia(item)

        melds_output[slot] = melds

        for k in total:
            total[k] += stats.get(k, 0)

    # apply food AFTER full gear
    total = apply_food(total, food)

    gcd = compute_gcd(total["sps"])
    dps = compute_dps(total)

    # OPTIONAL GCD targeting
    if target_gcd:
        penalty = abs(gcd - target_gcd) * 500
        dps -= penalty

    return {
        "stats": total,
        "gcd": gcd,
        "dps": dps,
        "melds": melds_output
    }

# -------------------------
# SOLVER
# -------------------------
def run_solver(items_by_slot, food, target_gcd, logger):

    logger("=== SOLVER START ===")

    start = time.time()

    # 🚫 REMOVE EMPTY OR NONE SLOTS
    clean_slots = {}
    for slot, items in items_by_slot.items():
        valid = [i for i in items if i is not None]
        if not valid:
            logger(f"[ERROR] Slot {slot} has no valid items")
            return []
        clean_slots[slot] = valid

    slots = list(clean_slots.keys())

    combos = itertools.product(*clean_slots.values())

    results = []

    for combo in combos:

        build = dict(zip(slots, combo))

        result = evaluate_build(build, food, target_gcd)

        if result is None:
            continue

        results.append({
            "build": build,
            "result": result
        })

    results.sort(key=lambda x: x["result"]["dps"], reverse=True)

    logger(f"=== DONE ({time.time() - start:.2f}s) ===")

    return results[:3]
