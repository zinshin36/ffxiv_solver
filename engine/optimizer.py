import itertools
import time

from engine.logger import log
from engine.materia_system import load_materia
from engine.blacklist import load_blacklist
from engine.tier_solver import calculate_gcd
from engine.dps_model import compute_dps


def run_solver(items, target_gcd=2.38, food=None):
    return solve(items, target_gcd, food)


def solve(items, target_gcd, food=None):

    log("=== SOLVER START ===")

    start_time = time.time()
    last_update = start_time

    materia = load_materia()
    blacklist = load_blacklist()

    items = [i for i in items if not any(b in i["name"].lower() for b in blacklist)]

    # -------------------------
    # GROUP BY SLOT
    # -------------------------
    gear = {}

    for item in items:
        gear.setdefault(item["slot"], []).append(item)

    required_slots = [
        "weapon", "head", "body", "hands",
        "legs", "feet", "earrings",
        "necklace", "bracelet", "ring"
    ]

    for s in required_slots:
        if s not in gear or not gear[s]:
            log(f"[ERROR] Missing slot: {s}")
            return []

    # -------------------------
    # TOTAL COMBINATIONS
    # -------------------------
    total = (
        len(gear["weapon"]) *
        len(gear["head"]) *
        len(gear["body"]) *
        len(gear["hands"]) *
        len(gear["legs"]) *
        len(gear["feet"]) *
        len(gear["earrings"]) *
        len(gear["necklace"]) *
        len(gear["bracelet"]) *
        len(gear["ring"]) *
        len(gear["ring"])
    )

    log(f"[SOLVER] TOTAL COMBINATIONS: {total:,}")

    combos = itertools.product(
        gear["weapon"], gear["head"], gear["body"], gear["hands"],
        gear["legs"], gear["feet"], gear["earrings"],
        gear["necklace"], gear["bracelet"],
        gear["ring"], gear["ring"]
    )

    best = []
    checked = 0

    for combo in combos:
        checked += 1

        # -------------------------
        # PREVENT DUPLICATE RINGS
        # -------------------------
        if combo[-1]["name"] == combo[-2]["name"]:
            continue

        # -------------------------
        # PROGRESS UPDATE (TIME-BASED)
        # -------------------------
        now = time.time()

        if now - last_update >= 0.5:  # update every 0.5s
            elapsed = now - start_time
            speed = checked / elapsed if elapsed > 0 else 0

            pct = (checked / total) * 100 if total else 0
            remaining = (total - checked) / speed if speed > 0 else 0

            log(
                f"[PROGRESS] {pct:.4f}% | "
                f"{checked:,}/{total:,} | "
                f"{speed:,.0f}/s | "
                f"ETA: {remaining:,.1f}s"
            )

            last_update = now

        # -------------------------
        # STAT SUM
        # -------------------------
        total_stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

        for item in combo:
            for k in total_stats:
                total_stats[k] += item["stats"].get(k, 0)

        # -------------------------
        # APPLY FOOD
        # -------------------------
        if food:
            for k in food:
                if k != "name":
                    total_stats[k] += food[k]

        # -------------------------
        # SCORE
        # -------------------------
        gcd = calculate_gcd(total_stats["sps"])
        dps = compute_dps(total_stats)

        score = dps - abs(gcd - target_gcd) * 1500

        best.append({
            "score": score,
            "stats": total_stats,
            "build": combo,
            "gcd": gcd,
            "dps": dps
        })

    best.sort(key=lambda x: x["score"], reverse=True)

    total_time = time.time() - start_time

    log(f"=== SOLVER COMPLETE ({total_time:.2f}s) ===")

    return best[:10]
