import itertools
import time
from engine.dps_model import compute_dps
from engine.spell_speed import gcd_from_sps


MATERIA_VALUE = 36
MATERIA_TYPES = ["crit", "dh", "det", "sps"]


# -------------------------
# APPLY MATERIA TO ITEM
# -------------------------
def apply_best_materia(item, target_gcd):

    base_stats = item["stats"]
    slots = item.get("materia_slots", 0)

    if slots <= 0:
        return base_stats.copy(), []

    best_stats = None
    best_score = -1
    best_melds = None

    for combo in itertools.product(MATERIA_TYPES, repeat=slots):

        stats = base_stats.copy()
        melds = []

        for m in combo:
            stats[m] += MATERIA_VALUE
            melds.append(f"{m}+{MATERIA_VALUE}")

        gcd = gcd_from_sps(stats["sps"])

        # prioritize matching GCD first
        gcd_diff = abs(gcd - target_gcd)

        score = (
            stats["crit"] * 1.0 +
            stats["dh"] * 0.9 +
            stats["det"] * 0.8 +
            stats["sps"] * 0.7
        )

        final_score = score - (gcd_diff * 1000)

        if final_score > best_score:
            best_score = final_score
            best_stats = stats
            best_melds = melds

    return best_stats, best_melds


# -------------------------
# APPLY FOOD
# -------------------------
def apply_food(stats, food_bonus):

    if not food_bonus:
        return stats

    result = stats.copy()

    for stat, (pct, cap) in food_bonus.items():
        base = result.get(stat, 0)
        bonus = min(int(base * pct), cap)
        result[stat] += bonus

    return result


# -------------------------
# BUILD EVALUATION
# -------------------------
def evaluate_build(build, target_gcd, food_bonus):

    total_stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}
    meld_summary = {}

    # -------------------------
    # APPLY MATERIA PER ITEM
    # -------------------------
    for slot, item in build.items():

        stats, melds = apply_best_materia(item, target_gcd)

        meld_summary[slot] = {
            "item": item["name"],
            "melds": melds
        }

        for k in total_stats:
            total_stats[k] += stats.get(k, 0)

    # -------------------------
    # APPLY FOOD
    # -------------------------
    total_stats = apply_food(total_stats, food_bonus)

    # -------------------------
    # FINAL CALC
    # -------------------------
    gcd = gcd_from_sps(total_stats["sps"])
    dps = compute_dps(total_stats)

    # soft GCD targeting
    penalty = abs(gcd - target_gcd) * 1000
    score = dps - penalty

    return {
        "dps": dps,
        "gcd": gcd,
        "score": score,
        "stats": total_stats,
        "melds": meld_summary
    }


# -------------------------
# SOLVER
# -------------------------
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
