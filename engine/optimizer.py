import itertools
import time
from engine.dps_model import compute_dps
from engine.gcd import compute_gcd


STAT_CAP = 3000  # safe cap


def apply_stat_caps(stats):
    capped = {}
    for k, v in stats.items():
        capped[k] = min(v, STAT_CAP)
    return capped


def apply_food(stats, food_bonus):
    result = stats.copy()

    for stat, (pct, cap) in food_bonus.items():
        base = result.get(stat, 0)
        bonus = min(int(base * pct), cap)
        result[stat] += bonus

    return result


def apply_materia(stats, slots):
    # greedy best stat (crit priority)
    result = stats.copy()

    for _ in range(slots):
        best_stat = max(["crit", "dh", "det", "sps"], key=lambda s: result[s])
        result[best_stat] += 36

    return result


def is_unique_conflict(build):
    seen = set()

    for item in build.values():
        name = item["name"]

        if name in seen:
            return True

        seen.add(name)

    return False


def evaluate_build(build, target_gcd, food_bonus):
    total = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

    for item in build.values():
        stats = apply_materia(item["stats"], item.get("materia_slots", 0))

        for k in total:
            total[k] += stats.get(k, 0)

    total = apply_food(total, food_bonus)
    total = apply_stat_caps(total)

    gcd = compute_gcd(total["sps"])

    # HARD FILTER (this fixes your issue)
    if abs(gcd - target_gcd) > 0.02:
        return None

    dps = compute_dps(total)

    return {
        "stats": total,
        "gcd": gcd,
        "dps": dps,
        "score": dps
    }


def run_solver(items_by_slot, target_gcd, food_bonus, logger):

    logger("=== SOLVER START ===")

    start = time.time()

    slots = list(items_by_slot.keys())

    all_combos = itertools.product(*items_by_slot.values())

    results = []

    for idx, combo in enumerate(all_combos):

        build = dict(zip(slots, combo))

        # ❗ prevent duplicate rings / uniques
        if is_unique_conflict(build):
            continue

        result = evaluate_build(build, target_gcd, food_bonus)

        if result is None:
            continue

        results.append({
            "build": build,
            "result": result
        })

        if idx % 500 == 0:
            logger(f"[SOLVER] checked {idx}")

    results.sort(key=lambda x: x["result"]["score"], reverse=True)

    logger(f"=== SOLVER DONE ({time.time() - start:.2f}s) ===")
    logger(f"[SOLVER] VALID BUILDS: {len(results)}")

    return results[:3]
