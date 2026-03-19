import itertools
import time

from engine.materia_optimizer import optimize_materia_for_set
from engine.tier_solver import calculate_gcd
from engine.dps_model import compute_dps
from engine.logger import log


# =========================
# MAIN SOLVER (CORE)
# =========================
def solve(items, target_gcd=2.38, foods=None, top_n=3):

    slots = [
        "weapon", "head", "body", "hands",
        "legs", "feet", "earrings",
        "necklace", "bracelet", "ring"
    ]

    gear = {s: [] for s in slots}

    for item in items:
        if item["slot"] in gear:
            gear[item["slot"]].append(item)

    for s in slots:
        log(f"{s}: {len(gear[s])}")

    # prevent zero-slot crash
    for s in slots:
        if not gear[s]:
            log(f"WARNING: No items for slot '{s}'")

    total = 1
    for s in slots:
        total *= max(1, len(gear[s]))
    total *= max(1, len(gear["ring"]))

    log(f"Total combinations: {total}")

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
            pct = int((checked / total) * 100)
            log(f"{checked}/{total} ({pct}%) | {elapsed:.1f}s")

        try:
            materia_stats, melds = optimize_materia_for_set(combo)
        except Exception as e:
            log(f"Materia error: {e}")
            continue

        best_score = 0
        best_food = None
        best_stats = None

        for food in foods or [{}]:
            total_stats = materia_stats.copy()

            for k in food:
                if k != "name":
                    total_stats[k] += food[k]

            gcd = calculate_gcd(total_stats["sps"])
            dps = compute_dps(total_stats)

            penalty = abs(gcd - target_gcd) * 2000
            score = dps - penalty

            if score > best_score:
                best_score = score
                best_food = food.get("name", "None")
                best_stats = total_stats

        best.append({
            "score": best_score,
            "build": combo,
            "food": best_food,
            "stats": best_stats,
            "melds": melds
        })

    best.sort(key=lambda x: x["score"], reverse=True)

    log("Finished solver")

    return best[:top_n]


# =========================
# SAFE ENTRY POINT (FIXES YOUR CRASH)
# =========================
def run_solver(items, target_gcd=2.38):
    log("Running solver wrapper...")

    if not items:
        log("ERROR: No items loaded")
        return

    try:
        results = solve(items, target_gcd=target_gcd)

        log("Top Results:")
        for i, r in enumerate(results, 1):
            log(f"#{i} Score={r['score']:.2f} Food={r['food']}")

        return results

    except Exception as e:
        log(f"FATAL SOLVER ERROR: {e}")
        raise
