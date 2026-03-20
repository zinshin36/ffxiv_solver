import itertools
import time
from engine.dps_model import compute_dps, compute_gcd_from_sps


MATERIA_VALUE = 36


def apply_materia(stats, slots):
    result = stats.copy()
    melds = []

    for _ in range(slots):

        # choose stat with lowest current value (better balance)
        stat = min(["crit", "dh", "det", "sps"], key=lambda s: result[s])

        result[stat] += MATERIA_VALUE
        melds.append(f"{stat}+36")

    return result, melds


def apply_food(stats, food_bonus):
    result = stats.copy()

    for stat, (pct, cap) in food_bonus.items():
        base = result.get(stat, 0)
        bonus = min(int(base * pct), cap)
        result[stat] += bonus

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
    all_melds = []

    for item in build.values():
        stats, melds = apply_materia(item["stats"], item.get("materia_slots", 0))

        all_melds.append({
            "item": item["name"],
            "melds": melds
        })

        for k in total:
            total[k] += stats.get(k, 0)

    total = apply_food(total, food_bonus)

    gcd = compute_gcd_from_sps(total["sps"])
    dps = compute_dps(total)

    # soft target
    penalty = abs(gcd - target_gcd) * 2000
    score = dps - penalty

    return {
        "stats": total,
        "gcd": gcd,
        "dps": dps,
        "score": score,
        "melds": all_melds
    }


def run_solver(items_by_slot, target_gcd, food_bonus, logger):

    logger("=== SOLVER START ===")

    start = time.time()

    slots = list(items_by_slot.keys())
    combos = itertools.product(*items_by_slot.values())

    results = []

    for i, combo in enumerate(combos):

        build = dict(zip(slots, combo))

        if is_unique_conflict(build):
            continue

        result = evaluate_build(build, target_gcd, food_bonus)

        results.append({
            "build": build,
            "result": result
        })

        if i % 500 == 0:
            logger(f"[SOLVER] {i}")

    results.sort(key=lambda x: x["result"]["score"], reverse=True)

    logger(f"=== DONE ({time.time() - start:.2f}s) ===")

    return results[:3]
