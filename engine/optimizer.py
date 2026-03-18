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


def combine_builds(slot_groups):
    """
    Generate all combinations (1 item per slot)
    WARNING: can explode if too many items per slot
    """
    keys = list(slot_groups.keys())
    values = [slot_groups[k] for k in keys]

    for combo in itertools.product(*values):
        yield list(combo)


def sum_stats(build):
    total = {"crit": 0, "dh": 0, "det": 0, "sps": 0}

    for item in build:
        total["crit"] += item.get("crit", 0)
        total["dh"] += item.get("dh", 0)
        total["det"] += item.get("det", 0)
        total["sps"] += item.get("sps", 0)

    return total


def attach_fake_materia(build):
    """
    Simple placeholder: adds dummy materia so UI doesn't break
    """
    for item in build:
        item["materia_applied"] = [
            {"stat": "crit", "value": 36},
            {"stat": "crit", "value": 36},
        ]
    return build


def solve(items, target_gcd, progress=None, top_n=3, foods=None):
    """
    MAIN SOLVER FUNCTION (what main.py expects)
    """
    log("Starting solver...")

    if not items:
        return []

    slot_groups = group_by_slot(items)

    # Reduce explosion: keep top 8 ilvl per slot
    for slot in slot_groups:
        slot_groups[slot] = sorted(
            slot_groups[slot],
            key=lambda x: x["ilvl"],
            reverse=True
        )[:8]

    builds = []
    total_checked = 0

    for idx, build in enumerate(combine_builds(slot_groups)):
        total_checked += 1

        if idx % 500 == 0 and progress:
            progress(min(100, idx // 50))

        stats = sum_stats(build)

        # Apply foods
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

    log(f"Total builds checked: {total_checked}")

    # Sort + return top N
    builds.sort(key=lambda x: x["score"], reverse=True)

    return builds[:top_n]
