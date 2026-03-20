import itertools
import time
from engine.dps_model import compute_dps
from engine.gcd import compute_gcd


STAT_CAP = 9000


def apply_stat_caps(stats):
    return {k: min(v, STAT_CAP) for k, v in stats.items()}


def apply_food(stats, food_bonus):
    result = stats.copy()

    for stat, (pct, cap) in food_bonus.items():
        base = result.get(stat, 0)
        bonus = min(int(base * pct), cap)
        result[stat] += bonus

    return result


def apply_materia(stats, slots):
    result = stats.copy()

    for _ in range(slots):
        # prioritize best scaling stat
        best = max(result, key=lambda x: result[x] if x != "int" else -1)
        if best != "int":
            result[best] += 36

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
    dps = compute_dps(total)

    # 🔥 THIS is the correct behavior
    penalty = abs(gcd - target_gcd) * 3000

    score = dps - penalty

    return {
        "stats": total,
        "gcd": gcd,
        "dps": dps,
        "score": score
    }


def run_solver(items_by_slot, target_gcd, food_bonus, logger):

    logger("=== SOLVER START ===")

    start = time.time()

    slots = list(items_by_slot.keys())

    all_combos = itertools.product(*items_by_slot.values())

    results = []

    for idx, combo in enumerate(all_combos):

        build = dict(zip(slots, combo))

        if is_unique_conflict(build):
            continue

        result = evaluate_build(build, target_gcd, food_bonus)

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
