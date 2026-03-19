import itertools
import time

from engine.logger import log
from engine.materia_system import load_materia
from engine.blacklist import load_blacklist


def run_solver(items, target_gcd, selected_food):

    log("=== SOLVER START ===")

    materia = load_materia()
    log(f"[SOLVER] Materia count: {len(materia)}")

    blacklist = load_blacklist()
    log(f"[SOLVER] Blacklist loaded: {len(blacklist)}")

    # Apply blacklist
    if blacklist:
        items = [i for i in items if not any(b in i["name"].lower() for b in blacklist)]

    log(f"[SOLVER] Items after blacklist: {len(items)}")

    # Group by slot
    gear = {}
    for i in items:
        gear.setdefault(i["slot"], []).append(i)

    for k in gear:
        log(f"[GEAR] {k}: {len(gear[k])}")

    # Calculate combinations
    total = 1
    for v in gear.values():
        total *= max(1, len(v))

    log(f"[SOLVER] TOTAL COMBINATIONS: {total}")

    start = time.time()
    checked = 0

    for combo in itertools.product(*gear.values()):
        checked += 1

        if checked % 1000 == 0:
            pct = (checked / total) * 100
            elapsed = time.time() - start
            log(f"[PROGRESS] {checked}/{total} ({pct:.4f}%) | {elapsed:.1f}s")

    log("=== SOLVER COMPLETE ===")
