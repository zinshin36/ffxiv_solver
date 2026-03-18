import itertools
from engine.logger import log
from engine.dps_model import compute_dps
from engine.food import apply_food


# REAL SLOT LIST (forces full builds)
SLOTS = [
    "weapon", "head", "body", "hands", "legs", "feet",
    "earrings", "necklace", "bracelet", "ring"
]


def detect_slot(item_name):
    name = item_name.lower()

    if "sword" in name or "staff" in name or "rod" in name:
        return "weapon"
    if "helm" in name or "hat" in name:
        return "head"
    if "coat" in name or "robe" in name:
        return "body"
    if "gloves" in name:
        return "hands"
    if "pants" in name or "trousers" in name:
        return "legs"
    if "boots" in name:
        return "feet"
    if "earring" in name:
        return "earrings"
    if "necklace" in name:
        return "necklace"
    if "bracelet" in name:
        return "bracelet"
    if "ring" in name:
        return "ring"

    return None


def is_caster(item):
    name = item["name"].lower()
    return any(x in name for x in ["caster", "mage", "sorcerer", "black", "thaum"])


def group_items(items):
    slots = {s: [] for s in SLOTS}

    for item in items:
        if not is_caster(item):
            continue

        slot = detect_slot(item["name"])

        if slot:
            slots[slot].append(item)

    # remove empty slots (prevents crash)
    slots = {k: v for k, v in slots.items() if v}

    return slots


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

    # simple priority: crit > dh > det > sps
    for _ in range(item.get("materia_slots", 2)):
        item["crit"] += 36
        melds.append({"stat": "crit", "value": 36})

    item["materia_applied"] = melds
    return item


def solve(items, target_gcd, progress=None, top_n=3, foods=None):
    log("Starting REAL solver...")

    slot_groups = group_items(items)

    for slot in slot_groups:
        # keep more items since you want full brute force
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

        if checked % 2000 == 0:
            log(f"{checked}/{total} ({round((checked/total)*100,2)}%)")

        build = [apply_materia(dict(item)) for item in combo]

        base_stats = sum_stats(build)

        best = None

        for food in foods:
            boosted = apply_food(base_stats, food)
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
