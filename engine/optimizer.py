import itertools
import math
import time

# Level constants (Lv100 - adjust if needed)
LEVEL_SUB = 400
LEVEL_DIV = 1900
LEVEL_MAIN = 390

MATERIA_VALUES = {
    "crit": 36,
    "dh": 36,
    "det": 36,
    "sps": 36
}

OVERMELD_VALUE = 12  # reduced strength

SLOTS = [
    "weapon","head","body","hands","legs","feet",
    "earrings","necklace","bracelet","ring1","ring2"
]

# ----------------------------
# STAT FORMULAS (AKHMORNING)
# ----------------------------
def calc_crit(crit):
    rate = math.floor(200 * (crit - LEVEL_SUB) / LEVEL_DIV + 50) / 1000
    bonus = (1400 + math.floor(200 * (crit - LEVEL_SUB) / LEVEL_DIV)) / 1000
    return rate, bonus

def calc_dh(dh):
    return math.floor(550 * (dh - LEVEL_SUB) / LEVEL_DIV) / 1000

def calc_det(det):
    return (1000 + math.floor(140 * (det - LEVEL_MAIN) / LEVEL_DIV)) / 1000

def calc_sps(sps):
    return (1000 + math.floor(130 * (sps - LEVEL_SUB) / LEVEL_DIV)) / 1000

def calc_gcd(speed):
    gcd = math.floor((2500 * (1000 + math.ceil(130 * (LEVEL_SUB - speed) / LEVEL_DIV)) / 10000)) / 100
    return gcd

# ----------------------------
# MATERIA SYSTEM
# ----------------------------
def apply_melds(item):
    stats = item["stats"].copy()
    melds = []

    cap = max(stats.values())  # stat cap

    slots = item.get("slots", 2)
    overmeld = item.get("overmeld", 0)

    # priority order (dynamic later)
    priority = item.get("priority", ["crit","det","dh","sps"])

    # normal slots
    for _ in range(slots):
        for stat in priority:
            if stats[stat] + MATERIA_VALUES[stat] <= cap:
                stats[stat] += MATERIA_VALUES[stat]
                melds.append(f"{stat}+36")
                break

    # overmeld slots
    for _ in range(overmeld):
        for stat in priority:
            if stats[stat] + OVERMELD_VALUE <= cap:
                stats[stat] += OVERMELD_VALUE
                melds.append(f"{stat}+12")
                break

    return stats, melds

# ----------------------------
# BUILD EVALUATION
# ----------------------------
def evaluate_build(build, food, target_gcd, build_mode):
    total = {"crit":0,"dh":0,"det":0,"sps":0}

    meld_info = {}

    for slot, item in build.items():
        stats, melds = apply_melds(item)
        meld_info[slot] = melds

        for k in total:
            total[k] += stats.get(k,0)

    # apply food
    if food:
        for k,v in food.items():
            total[k] += v

    # formulas
    crit_rate, crit_bonus = calc_crit(total["crit"])
    dh_rate = calc_dh(total["dh"])
    det_multi = calc_det(total["det"])
    sps_multi = calc_sps(total["sps"])
    gcd = calc_gcd(total["sps"])

    expected_crit = 1 + crit_rate * (crit_bonus - 1)
    expected_dh = 1 + dh_rate * 0.25

    dps = 1000 * det_multi * sps_multi * expected_crit * expected_dh

    # GCD enforcement ONLY if user sets it
    if target_gcd:
        if abs(gcd - target_gcd) > 0.01:
            return None

    return {
        "dps": dps,
        "gcd": gcd,
        "stats": total,
        "melds": meld_info
    }

# ----------------------------
# SOLVER
# ----------------------------
def run_solver(items_by_slot, food, target_gcd, logger, build_mode):
    start = time.time()
    logger.info("=== SOLVER START ===")

    # set priority based on mode
    if build_mode == "SPS":
        priority = ["sps","crit","det","dh"]
    else:
        priority = ["crit","det","dh","sps"]

    for slot in items_by_slot:
        for item in items_by_slot[slot]:
            item["priority"] = priority

    combinations = list(itertools.product(*items_by_slot.values()))
    logger.info(f"[SOLVER] TOTAL COMBINATIONS: {len(combinations)}")

    best = []

    for combo in combinations:
        build = dict(zip(items_by_slot.keys(), combo))

        result = evaluate_build(build, food, target_gcd, build_mode)
        if not result:
            continue

        best.append((result["dps"], build, result))

    best.sort(key=lambda x: x[0], reverse=True)

    logger.info(f"=== DONE ({round(time.time()-start,2)}s) ===")

    return best[:3]
