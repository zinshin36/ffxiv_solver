import itertools
from collections import defaultdict
from engine.logger import log
from engine.dps_model import compute_dps
from engine.food import apply_food
from engine.materia_solver import optimize_materia
from engine.gcd import compute_gcd


SLOTS = [
    "weapon", "head", "body", "hands", "legs", "feet",
    "earrings", "necklace", "bracelet", "ring1", "ring2"
]


def group_items(items):
    slots = defaultdict(list)

    for item in items:
        if item["slot"] == "ring":
            slots["ring1"].append(item)
            slots["ring2"].append(item)
        else:
            slots[item["slot"]].append(item)

    return {k: v for k, v in slots.items() if v}


def sum_stats(build):
    total = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 1000}

    for item in build:
        total["crit"] += item["crit"]
        total["dh"] += item["dh"]
        total["det"] += item["det"]
        total["sps"] += item["sps"]

    return total


def solve(items, target_gcd, progress=None, top_n=3, foods=None):
    log("Starting FINAL solver (materia + speed tiers)...")

    slot_groups = group_items(items)

    for slot in slot_groups:
        slot_groups[slot] = sorted(
            slot_groups[slot],
            key=lambda x: x["ilvl"],
            reverse=True
        )[:12]

    keys = list(slot_groups.keys())
    values = [slot_groups[k] for k in keys]

    total = 1
    for v in values:
        total *= len(v)

    log(f"Total combinations: {total}")

    results = []
    checked = 0

    for combo in itertools.product(*values):
        checked += 1

        if progress:
            progress(int((checked / total) * 100))

        if checked % 3000 == 0:
            log(f"{checked}/{total} ({round((checked/total)*100,2)}%)")

        build = [dict(item) for item in combo]

        base_stats = sum_stats(build)

        best = None

        for food in foods:
            boosted = apply_food(base_stats, food)

            # total materia slots across gear
            total_slots = sum(i.get("materia_slots", 2) for i in build)

            materia_result = optimize_materia(
                boosted,
                total_slots,
                compute_dps,
                compute_gcd,
                target_gcd
            )

            if not best or materia_result["score"] > best["score"]:
                best = {
                    "score": materia_result["score"],
                    "dps": materia_result["dps"],
                    "gcd": materia_result["gcd"],
                    "food": food["name"],
                    "melds": materia_result["melds"]
                }

        results.append({
            "build": build,
            "score": best["score"],
            "dps": best["dps"],
            "gcd": best["gcd"],
            "food": best["food"],
            "melds": best["melds"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    log("Solver finished")

    return results[:top_n]
