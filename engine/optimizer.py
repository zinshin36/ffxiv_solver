from itertools import product
from engine.simulator import simulate_dps
from engine.logger import log


# ------------------------------------------------
# FILTER BY ILVL
# ------------------------------------------------

def filter_ilvl(items, delta=25):

    max_ilvl = max(i["LevelItem"] for i in items)

    cutoff = max_ilvl - delta

    filtered = [i for i in items if i["LevelItem"] >= cutoff]

    log(f"Max ilvl: {max_ilvl}")
    log(f"ILVL cutoff: {cutoff}")
    log(f"Items after ilvl filter: {len(filtered)}")

    return filtered


# ------------------------------------------------
# BLACKLIST
# ------------------------------------------------

def filter_blacklist(items, blacklist):

    if not blacklist:
        return items

    filtered = [i for i in items if i["Name"] not in blacklist]

    log(f"Blacklist removed {len(items) - len(filtered)} items")

    return filtered


# ------------------------------------------------
# GROUP ITEMS BY SLOT
# ------------------------------------------------

def split_by_slot(items):

    slots = {}

    for item in items:

        slot = str(item["Slot"])

        slots.setdefault(slot, []).append(item)

    log(f"Slots detected: {len(slots)}")

    return slots


# ------------------------------------------------
# APPLY MATERIA
# ------------------------------------------------

def apply_best_materia(item, materia):

    stats = item["stats"].copy()

    slots = item["MateriaSlots"]

    if slots <= 0:
        return stats

    # pick highest value materia for each stat
    best = {}

    for m in materia:

        stat = m["stat"]
        val = m["value"]

        if stat not in best or val > best[stat]:
            best[stat] = val

    # apply best materia to slots
    for stat in list(best.keys())[:slots]:

        stats[stat] = stats.get(stat, 0) + best[stat]

    return stats


# ------------------------------------------------
# BUILD GEAR SET
# ------------------------------------------------

def build_gear_set(combo, slot_keys, materia):

    gear = {}

    for i, item in enumerate(combo):

        stats = apply_best_materia(item, materia)

        gear[slot_keys[i]] = {
            "Name": item["Name"],
            "stats": stats
        }

    return gear


# ------------------------------------------------
# MAIN OPTIMIZER
# ------------------------------------------------

def top_sets(items, materia, blacklist=None, top_n=10):

    if blacklist is None:
        blacklist = []

    # filters
    items = filter_ilvl(items)
    items = filter_blacklist(items, blacklist)

    slots = split_by_slot(items)

    slot_keys = list(slots.keys())

    combinations = product(*(slots[s] for s in slot_keys))

    scored = []

    count = 0

    for combo in combinations:

        gear = build_gear_set(combo, slot_keys, materia)

        dps = simulate_dps(gear)

        scored.append({
            "gear": gear,
            "dps": dps
        })

        count += 1

        if count % 10000 == 0:
            log(f"Checked {count} sets")

    scored.sort(key=lambda x: x["dps"], reverse=True)

    log(f"Total sets evaluated: {count}")

    return scored[:top_n]
