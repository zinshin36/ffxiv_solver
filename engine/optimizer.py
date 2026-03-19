import itertools
import time
import json
import os

from engine.logger import log
from engine.materia_system import load_materia, optimize_materia
from engine.dps_model import compute_dps
from engine.tier_solver import calculate_gcd
from engine.blacklist import load_blacklist


def load_food():

    path = os.path.join(os.getcwd(), "foods.json")

    log(f"[FOOD] Looking for foods.json at: {path}")

    if not os.path.exists(path):
        log("[FOOD] ERROR: foods.json NOT FOUND")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # SUPPORT BOTH FORMATS
        if isinstance(data, dict):
            foods = []
            for k, v in data.items():
                entry = {"name": k}
                entry.update(v)
                foods.append(entry)
        else:
            foods = data

        log(f"[FOOD] Loaded {len(foods)} foods")
        return foods

    except Exception as e:
        log(f"[FOOD] ERROR parsing foods.json: {e}")
        return []


def apply_food(stats, food):

    result = stats.copy()

    for k, v in food.items():
        if k != "name":
            result[k] = result.get(k, 0) + v

    return result


def solve(items, target_gcd, min_ilvl, selected_food):

    log("=== SOLVER START ===")

    blacklist = load_blacklist()
    materia_list = load_materia()
    foods = load_food()

    log(f"[INIT] Blacklist entries: {len(blacklist)}")
    log(f"[INIT] Materia loaded: {len(materia_list)}")

    # SELECT FOOD
    food = next((f for f in foods if f["name"] == selected_food), {})

    if not food:
        log("[FOOD] WARNING: Selected food not found, using NONE")

    # FILTER
    filtered = []

    for i in items:

        if i["ilvl"] < min_ilvl:
            continue

        if any(b in i["name"].lower() for b in blacklist):
            continue

        filtered.append(i)

    log(f"[FILTER] Items after filter: {len(filtered)}")

    # GROUP
    gear = {}
    for item in filtered:
        gear.setdefault(item["slot"], []).append(item)

    for k in gear:
        log(f"[GEAR] {k}: {len(gear[k])}")

    lists = list(gear.values())

    total = 1
    for l in lists:
        total *= len(l)

    log(f"[SOLVER] TOTAL COMBINATIONS: {total}")

    best = []
    start = time.time()

    for idx, combo in enumerate(itertools.product(*lists)):

        if idx % 1000 == 0:
            pct = (idx / total) * 100 if total else 0
            log(f"[PROGRESS] {pct:.6f}% ({idx}/{total})")

        stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

        for item in combo:
            for k in stats:
                stats[k] += item["stats"].get(k, 0)

        _, stats = optimize_materia(
            {"stats": stats, "materia_slots": 10},
            materia_list
        )

        stats = apply_food(stats, food)

        gcd = calculate_gcd(stats["sps"])
        dps = compute_dps(stats)

        penalty = abs(gcd - target_gcd) * 2000
        score = dps - penalty

        best.append(score)

    best.sort(reverse=True)

    log("=== SOLVER COMPLETE ===")

    if len(best) >= 2:
        diff = best[0] - best[1]
        log(f"[RESULT] DPS diff: {diff:.2f}")

    return best[:3]
