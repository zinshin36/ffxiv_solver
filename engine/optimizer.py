from itertools import product
from engine.simulator import simulate_dps
from engine.logger import log
from engine.materia_solver import optimize_item_materia

# BLM ClassJobCategory key (Black Mage / Thaumaturge)
BLM_JOB_IDS = {"35", "36"}  # depends on export, both included


# --------------------------------------------------
# JOB FILTER
# --------------------------------------------------

def filter_job(items):

    filtered = []

    for item in items:

        job = str(item.get("JobCategory"))

        if job in BLM_JOB_IDS:
            filtered.append(item)

    log(f"BLM items: {len(filtered)}")

    return filtered


# --------------------------------------------------
# ILVL FILTER
# --------------------------------------------------

def filter_ilvl(items, delta=25):

    max_ilvl = max(i["LevelItem"] for i in items)

    cutoff = max_ilvl - delta

    filtered = [i for i in items if i["LevelItem"] >= cutoff]

    log(f"Max ilvl: {max_ilvl}")
    log(f"ILVL cutoff: {cutoff}")
    log(f"Items after ilvl filter: {len(filtered)}")

    return filtered


# --------------------------------------------------
# BLACKLIST
# --------------------------------------------------

def filter_blacklist(items, blacklist):

    if not blacklist:
        return items

    filtered = [i for i in items if i["Name"] not in blacklist]

    log(f"Blacklist removed {len(items) - len(filtered)} items")

    return filtered


# --------------------------------------------------
# HARD SLOT VALIDATION
# --------------------------------------------------

VALID_SLOTS = {
    "MainHand",
    "OffHand",
    "Head",
    "Body",
    "Hands",
    "Legs",
    "Feet",
    "Ears",
    "Neck",
    "Wrists",
    "FingerL",
    "FingerR"
}


def split_by_slot(items):

    slots = {}

    for item in items:

        slot = str(item.get("Slot"))

        if slot not in VALID_SLOTS:
            continue

        slots.setdefault(slot, []).append(item)

    for slot in VALID_SLOTS:

        if slot not in slots:
            log(f"WARNING: No items for slot {slot}")

    log(f"Slots prepared: {len(slots)}")

    return slots


# --------------------------------------------------
# BUILD GEAR SET
# --------------------------------------------------

def build_gear_set(combo, slot_keys, materia):

    gear = {}

    for i, item in enumerate(combo):

        optimized_stats = optimize_item_materia(item, materia)

        gear[slot_keys[i]] = {
            "Name": item["Name"],
            "stats": optimized_stats
        }

    return gear


# --------------------------------------------------
# SOLVER
# --------------------------------------------------

def top_sets(items, materia, blacklist=None, top_n=10):

    if blacklist is None:
        blacklist = []

    # Step 1: job filter
    items = filter_job(items)

    # Step 2: ilvl filter
    items = filter_ilvl(items)

    # Step 3: blacklist
    items = filter_blacklist(items, blacklist)

    # Step 4: slot grouping
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

        if checked % 5000 == 0:
            log(f"Checked {checked} gear sets")

    scored.sort(key=lambda x: x["dps"], reverse=True)

    log(f"Total sets evaluated: {checked}")

    return scored[:top_n]
