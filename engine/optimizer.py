import itertools
from collections import defaultdict
from engine.logger import log
from engine.dps import calculate_score
from engine.food import apply_food


def group_by_slot(items):
    slots = defaultdict(list)

    for item in items:
        slots[item["slot"]].append(item)

    return slots


def sum_stats(build):
    total = {"crit": 0, "dh": 0, "det": 0, "sps": 0}

    for item in build:
        total["crit"] += item.get("crit", 0)
        total["dh"] += item.get("dh", 0)
        total["det"] += item.get("det", 0)
        total["sps"] += item.get("sps", 0)

    return total


def attach_fake_materia(build):
    for item in build:
        item["materia_applied"] = [
            {"stat": "crit", "value": 36},
            {"stat": "crit", "value": 36},
        ]
    return build


def solve(items, target_gcd, progress=None, top_n=3, foods=None):
    log("Starting solver...")

    if not items:
        return []

    slot_groups = group_by_slot(items)

    # Light pruning (NOT a cap, just sanity)
    for slot in slot_groups:
        slot_groups[slot] = sorted(
            slot_groups[slot],
            key=lambda x: x["ilvl"],
            reverse=True
        )[:10]

    slots = list(slot_groups.keys())
    values = [slot_groups[s] for s in slots]

    total_combinations = 1
    for v in values:
        total_combinations *= len(v)

    log(f"Total combinations to evaluate: {total_combinations}")

    builds = []
    checked = 0

    for combo in itertools.product(*values):
        checked += 1

        if progress and total_combinations > 0:
            pct = int((checked / total_combinations) * 100)
            progress(pct)

        if checked % 1000 == 0:
            log(f"Progress: {checked}/{total_combinations} ({round((checked/total_combinations)*100,2)}%)")

        build = list(combo)
        stats = sum_stats(build)

        best_food = "None"
        best_score = 0

        if foods:
            for food in foods:
                boosted = apply_food(stats, food)
                score = calculate_score(boosted, target_gcd)

                if score > best_score:
                    best_score = score
                    best_food = food["name"]
        else:
            best_score = calculate_score(stats, target_gcd)

        builds.append({
            "build": attach_fake_materia(build.copy()),
            "score": best_score,
            "food": best_food
        })

    log(f"Finished. Total builds checked: {checked}")

    builds.sort(key=lambda x: x["score"], reverse=True)

    return builds[:top_n]
