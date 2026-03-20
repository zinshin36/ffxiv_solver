import itertools
import time
from engine.dps_model import compute_dps
from engine.gcd import compute_gcd


# =========================
# SIMPLE MATERIA (TEMP SAFE)
# =========================
def apply_materia(stats, slots):
    result = stats.copy()

    for _ in range(slots):
        result["crit"] += 36  # basic default

    return result


# =========================
# BUILD EVALUATION
# =========================
def evaluate_build(build, target_gcd, food_bonus):
    total = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

    for item in build.values():
        stats = item["stats"]

        # apply materia
        stats = apply_materia(stats, item.get("materia_slots", 0))

        for k in total:
            total[k] += stats.get(k, 0)

    # apply food
    for stat, (pct, cap) in food_bonus.items():
        base = total.get(stat, 0)
        bonus = min(int(base * pct), cap)
        total[stat] += bonus

    gcd = compute_gcd(total["sps"])
    dps = compute_dps(total)

    # GCD penalty (important for BLM)
    penalty = abs(gcd - target_gcd) * 2000

    score = dps - penalty

    return {
        "stats": total,
        "gcd": gcd,
        "dps": dps,
        "score": score
    }


# =========================
# SOLVER
# =========================
def run_solver(items_by_slot, target_gcd, food_bonus, logger):

    logger("=== SOLVER START ===")

    start = time.time()

    slots = list(items_by_slot.keys())

    # ensure weapon exists
    if "weapon" not in slots:
        logger("[ERROR] Missing weapon slot")
        return []

    all_combos = list(itertools.product(*items_by_slot.values()))

    logger(f"[SOLVER] TOTAL COMBINATIONS: {len(all_combos):,}")

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

    logger(f"=== SOLVER DONE ({time.time() - start:.2f}s) ===")

    return results[:3]  # TOP 3
