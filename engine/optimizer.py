from itertools import product
from engine.simulator import simulate_dps
from engine.logger import log
from engine.materia_solver import optimize_item_materia


def filter_ilvl(items, delta=25):

    max_ilvl = max(i["LevelItem"] for i in items)

    cutoff = max_ilvl - delta

    filtered = [i for i in items if i["LevelItem"] >= cutoff]

    log(f"Max ilvl: {max_ilvl}")
    log(f"ILVL cutoff: {cutoff}")
    log(f"Items after ilvl filter: {len(filtered)}")

    return filtered


def filter_blacklist(items, blacklist):

    if not blacklist:
        return items

    filtered = [i for i in items if i["Name"] not in blacklist]

    log(f"Blacklist removed {len(items) - len(filtered)} items")

    return filtered


def split_by_slot(items):

    slots = {}

    for item in items:

        slot = str(item["Slot"])

        slots.setdefault(slot, []).append(item)

    return slots


def build_gear_set(combo, slot_keys, materia):

    gear = {}

    for i, item in enumerate(combo):

        optimized_stats = optimize_item_materia(item, materia)

        gear[slot_keys[i]] = {
            "Name": item["Name"],
            "stats": optimized_stats
        }

    return gear


def top_sets(items, materia, blacklist=None, top_n=10):

    if blacklist is None:
        blacklist = []

    items = filter_ilvl(items)
    items = filter_blacklist(items, blacklist)

    slots = split_by_slot(items)

    slot_keys = list(slots.keys())

    combinations = product(*(slots[s] for s in slot_keys))

    scored = []

    checked = 0

    for combo in combinations:

        gear = build_gear_set(combo, slot_keys, materia)

        dps = simulate_dps(gear)

        scored.append({
            "gear": gear,
            "dps": dps
        })

        checked += 1

        if checked % 10000 == 0:
            log(f"Checked {checked} sets")

    scored.sort(key=lambda x: x["dps"], reverse=True)

    log(f"Total sets evaluated: {checked}")

    return scored[:top_n]
