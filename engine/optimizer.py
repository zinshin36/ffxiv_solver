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
    if not os.path.exists("foods.json"):
        log("[FOOD] foods.json not found")
        return []

    with open("foods.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    log(f"[FOOD] Loaded {len(data)} foods")
    return data


def apply_food(stats, food):
    result = stats.copy()

    for k, v in food.items():
        if k != "name":
            result[k] = result.get(k, 0) + v

    return result


def solve(items, target_gcd, min_ilvl=0):

    log("=== SOLVER START ===")

    # --- LOAD SYSTEMS ---
    blacklist = load_blacklist()
    materia_list = load_materia()
    foods = load_food()

    log(f"[SOLVER] Blacklist: {len(blacklist)} entries")
    log(f"[SOLVER] Materia: {len(materia_list)} loaded")

    # --- FILTER ONLY BY ILVL (OPTIONAL) ---
    if min_ilvl > 0:
        items = [i for i in items if i["ilvl"] >= min_ilvl]

    log(f"[SOLVER] Items after ilvl filter: {len(items)}")

    # --- GROUP ---
    gear = {}
    for item in items:
        slot = item["slot"]
        gear.setdefault(slot, []).append(item)

    for k in gear:
        log(f"[GEAR] {k}: {len(gear[k])}")

    # --- COMBINATIONS ---
    slots = list(gear.keys())
    lists = [gear[s] for s in slots]

    total = 1
    for l in lists:
        total *= len(l)

    log(f"[SOLVER] TOTAL COMBINATIONS: {total}")

    best = []

    start = time.time()
    checked = 0

    for combo in itertools.product(*lists):

        checked += 1

        if checked % 1000 == 0:
            pct = (checked / total) * 100
            elapsed = time.time() - start
            log(f"[PROGRESS] {pct:.4f}% | {checked}/{total} | {elapsed:.1f}s")

        # --- BASE STATS ---
        total_stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

        for item in combo:
            for k in total_stats:
                total_stats[k] += item["stats"].get(k, 0)

        # --- MATERIA ---
        melds, total_stats = optimize_materia(
            {"stats": total_stats, "materia_slots": 10},
            materia_list
        )

        # --- FOOD ---
        best_score = 0
        best_food = None

        for food in foods or [{}]:

            stats = apply_food(total_stats, food)

            gcd = calculate_gcd(stats["sps"])
            dps = compute_dps(stats)

            penalty = abs(gcd - target_gcd) * 2000
            score = dps - penalty

            if score > best_score:
                best_score = score
                best_food = food.get("name", "None")

        best.append({
            "score": best_score,
            "food": best_food
        })

    best.sort(key=lambda x: x["score"], reverse=True)

    log("=== SOLVER COMPLETE ===")

    top = best[:3]

    if len(top) >= 2:
        diff = top[0]["score"] - top[1]["score"]
        log(f"[RESULT] DPS diff #1 vs #2: {diff:.2f}")

    return top
