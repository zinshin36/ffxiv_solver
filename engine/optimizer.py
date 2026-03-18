import itertools
from collections import defaultdict
from engine.logger import log
from engine.dps_model import compute_dps
from engine.food import apply_food


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

    # remove empty slots
    return {k: v for k, v in slots.items() if v}


def sum_stats(build):
    total = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 1000}

    for item in build:
        total["crit"] += item["crit"]
        total["dh"] += item["dh"]
        total["det"] += item["det"]
        total["sps"] += item["sps"]

    return total


def apply_materia(item):
    melds = []

    for _ in range(item.get("materia_slots", 2)):
        item["crit"] += 36
        melds.append({"stat": "crit", "value": 36})

    item["materia_applied"] = melds
    return item


def solve(items, target_gcd, progress=None, top_n=3, foods=None):
    log("Starting FULL solver...")

    slot_groups = group_items(items)

    # prune slightly (still large)
    for slot in slot_groups:
        slot_groups[slot] = sorted(
            slot_groups[slot],
            key=lambda x: x["ilvl"],
            reverse=True
        )[:15]

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

        if checked % 5000 == 0:
            log(f"{checked}/{total} ({round((checked/total)*100,2)}%)")

        build = []

        for item in combo:
            build.append(apply_materia(dict(item)))

        stats = sum_stats(build)

        best = None

        for food in foods:
            boosted = apply_food(stats, food)
            dps = compute_dps(boosted)

            if not best or dps > best["dps"]:
                best = {
                    "dps": dps,
                    "food": food["name"],
                    "stats": boosted
                }

        results.append({
            "build": build,
            "score": best["dps"],
            "food": best["food"],
            "stats": best["stats"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    log("Solver finished")

    return results[:top_n]
