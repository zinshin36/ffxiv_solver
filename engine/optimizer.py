import itertools
import time
from engine.dps_model import compute_dps, gcd_from_sps

MATERIA_VALUE = 36
MATERIA_TYPES = ["crit", "dh", "det", "sps"]

# ----------------------------------------
# STAT CAPS (safe generic caps)
# ----------------------------------------
STAT_CAP = 3000


def apply_caps(stats):
    capped = stats.copy()
    for k in capped:
        capped[k] = min(capped[k], STAT_CAP)
    return capped


# ----------------------------------------
# OVERMELD RULES
# ----------------------------------------
def get_max_melds(item):
    base = item.get("materia_slots", 0)

    # assume crafted gear = can overmeld
    if "augmented" not in item["name"].lower():
        return base + 2

    return base


# ----------------------------------------
# BEST MATERIA PER ITEM
# ----------------------------------------
def optimize_item_materia(item, target_gcd):

    base_stats = item["stats"]
    max_slots = get_max_melds(item)

    if max_slots <= 0:
        return base_stats.copy(), []

    best_stats = None
    best_score = -1
    best_melds = None

    for combo in itertools.product(MATERIA_TYPES, repeat=max_slots):

        stats = base_stats.copy()
        melds = []

        for i, m in enumerate(combo):

            # overmeld penalty (last 2 slots weaker)
            value = MATERIA_VALUE
            if i >= item.get("materia_slots", 0):
                value = int(MATERIA_VALUE * 0.8)

            stats[m] += value
            melds.append(f"{m}+{value}")

        stats = apply_caps(stats)

        gcd = gcd_from_sps(stats["sps"])
        gcd_diff = abs(gcd - target_gcd)

        score = compute_dps(stats) - (gcd_diff * 2000)

        if score > best_score:
            best_score = score
            best_stats = stats
            best_melds = melds

    return best_stats, best_melds


# ----------------------------------------
# APPLY FOOD
# ----------------------------------------
def apply_food(stats, food_bonus):

    if not food_bonus:
        return stats

    result = stats.copy()

    for stat, (pct, cap) in food_bonus.items():
        base = result.get(stat, 0)
        bonus = min(int(base * pct), cap)
        result[stat] += bonus

    return result


# ----------------------------------------
# BUILD EVALUATION
# ----------------------------------------
def evaluate_build(build, target_gcd, food_bonus):

    total_stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}
    meld_summary = {}

    for slot, item in build.items():

        stats, melds = optimize_item_materia(item, target_gcd)

        meld_summary[slot] = {
            "item": item["name"],
            "melds": melds
        }

        for k in total_stats:
            total_stats[k] += stats.get(k, 0)

    total_stats = apply_caps(total_stats)
    total_stats = apply_food(total_stats, food_bonus)

    gcd = gcd_from_sps(total_stats["sps"])
    dps = compute_dps(total_stats)

    penalty = abs(gcd - target_gcd) * 2000
    score = dps - penalty

    return {
        "dps": dps,
        "gcd": gcd,
        "score": score,
        "stats": total_stats,
        "melds": meld_summary
    }


# ----------------------------------------
# SOLVER
# ----------------------------------------
def run_solver(items_by_slot, target_gcd, food_bonus, logger):

    logger("=== SOLVER START ===")

    start = time.time()

    slots = list(items_by_slot.keys())
    all_combos = list(itertools.product(*items_by_slot.values()))

    logger(f"[SOLVER] TOTAL COMBINATIONS: {len(all_combos)}")

    results = []

    for idx, combo in enumerate(all_combos):

        build = dict(zip(slots, combo))
        result = evaluate_build(build, target_gcd, food_bonus)

        results.append({
            "build": build,
            "result": result
        })

        if idx % 100 == 0:
            logger(f"[SOLVER] {idx}/{len(all_combos)}")

    results.sort(key=lambda x: x["result"]["score"], reverse=True)

    logger(f"=== DONE ({time.time() - start:.2f}s) ===")

    return results[:10]
