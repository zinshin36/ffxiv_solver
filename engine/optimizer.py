import itertools
import time

from engine.materia_optimizer import optimize_materia_for_set
from engine.tier_solver import calculate_gcd
from engine.dps_model import compute_dps
from engine.logger import log


SLOTS = [
    "weapon", "head", "body", "hands",
    "legs", "feet", "earrings",
    "necklace", "bracelet", "ring"
]


def build_gear_table(items):
    gear = {s: [] for s in SLOTS}

    for item in items:
        slot = item.get("slot")
        if slot in gear:
            gear[slot].append(item)

    for s in SLOTS:
        log(f"[GEAR] {s}: {len(gear[s])}")

    return gear


def estimate_total_combinations(gear):
    total = 1

    for s in SLOTS:
        total *= max(1, len(gear[s]))

    # rings are double
    total *= max(1, len(gear["ring"]))

    return total


def solve(items, target_gcd=2.38, top_n=3):

    log("=== SOLVER START ===")

    gear = build_gear_table(items)

    total = estimate_total_combinations(gear)
    log(f"[SOLVER] Estimated combinations: {total}")

    combos = itertools.product(
        gear["weapon"], gear["head"], gear["body"], gear["hands"],
        gear["legs"], gear["feet"], gear["earrings"],
        gear["necklace"], gear["bracelet"],
        gear["ring"], gear["ring"]
    )

    best = []
    checked = 0
    start = time.time()

    for combo in combos:
        checked += 1

        if checked % 1000 == 0:
            elapsed = time.time() - start
            log(f"[PROGRESS] {checked} checked | {elapsed:.2f}s")

        try:
            materia_stats, melds = optimize_materia_for_set(combo)
        except Exception as e:
            log(f"[ERROR] Materia failure: {e}")
            continue

        try:
            gcd = calculate_gcd(materia_stats["sps"])
            dps = compute_dps(materia_stats)

            penalty = abs(gcd - target_gcd) * 2000
            score = dps - penalty
        except Exception as e:
            log(f"[ERROR] DPS failure: {e}")
            continue

        best.append({
            "score": score,
            "build": combo,
            "stats": materia_stats,
            "melds": melds
        })

    best.sort(key=lambda x: x["score"], reverse=True)

    log("=== SOLVER COMPLETE ===")

    return best[:top_n]


def run_solver(items, target_gcd=2.38):
    log("Running solver wrapper...")

    if not items:
        log("[FATAL] No items loaded")
        return []

    try:
        results = solve(items, target_gcd)

        for i, r in enumerate(results, 1):
            log(f"\n=== BUILD #{i} ===")
            log(f"Score: {r['score']:.2f}")
            log(f"Stats: {r['stats']}")

            for item in r["build"]:
                log(f" - {item['slot']}: {item['name']}")

        return results

    except Exception as e:
        log(f"[FATAL] Solver crashed: {e}")
        raise
