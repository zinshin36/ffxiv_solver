import itertools
import time

from engine.materia_optimizer import optimize_materia_for_set
from engine.tier_solver import calculate_gcd
from engine.dps_model import compute_dps
from engine.food import foods
from engine.blacklist import load_blacklist, is_blacklisted
from engine.logger import log


def run_solver(items, target_gcd=2.38):

    log("=== SOLVER START ===")

    blacklist = load_blacklist()
    log(f"[SOLVER] Blacklist loaded: {len(blacklist)} entries")

    # Apply blacklist
    items = [i for i in items if not is_blacklisted(i["name"], blacklist)]
    log(f"[SOLVER] After blacklist: {len(items)} items")

    # Group by slot
    gear = {}
    for i in items:
        gear.setdefault(i["slot"], []).append(i)

    for slot in gear:
        log(f"[GEAR] {slot}: {len(gear[slot])}")

    total = 1
    for slot in gear:
        total *= len(gear[slot])

    log(f"[SOLVER] TOTAL COMBINATIONS: {total}")

    combos = itertools.product(*gear.values())

    best = []
    checked = 0
    start = time.time()

    for combo in combos:
        checked += 1

        if checked % 1000 == 0:
            log(f"[PROGRESS] {checked}")

        materia_stats, melds = optimize_materia_for_set(combo)

        for food in foods:

            stats = materia_stats.copy()

            for k, v in food.items():
                if k != "name":
                    stats[k] += v

            gcd = calculate_gcd(stats["sps"])
            dps = compute_dps(stats)

            score = dps - abs(gcd - target_gcd) * 2000

            best.append(score)

    log("=== SOLVER DONE ===")
