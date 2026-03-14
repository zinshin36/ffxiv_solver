import os
import csv
from engine.logger import log

GAME_DATA_DIR = os.path.join(os.getcwd(), "game_data")


def load_csv(name):
    path = os.path.join(GAME_DATA_DIR, f"{name}.csv")

    if not os.path.exists(path):
        raise FileNotFoundError(f"{name}.csv not found in {GAME_DATA_DIR}")

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]

    log(f"{name}.csv loaded ({len(rows)} rows)")
    return rows


# --------------------------------------------------
# BASE PARAM MAP
# --------------------------------------------------

def load_base_params():
    rows = load_csv("BaseParam")

    mapping = {}

    for r in rows:
        key = r.get("Key") or r.get("#") or r.get("RowId")
        name = r.get("Name")

        if key and name:
            mapping[str(key)] = name

    log(f"BaseParam mapping built ({len(mapping)} stats)")
    return mapping


# --------------------------------------------------
# CLASS JOB CATEGORY
# --------------------------------------------------

def load_class_jobs():
    rows = load_csv("ClassJobCategory")

    mapping = {}

    for r in rows:
        key = r.get("Key") or r.get("#") or r.get("RowId")
        name = r.get("Name")

        mapping[str(key)] = name

    return mapping


# --------------------------------------------------
# EQUIP SLOT CATEGORY
# --------------------------------------------------

def load_slots():
    rows = load_csv("EquipSlotCategory")

    mapping = {}

    for r in rows:
        key = r.get("Key") or r.get("#") or r.get("RowId")

        mapping[str(key)] = r

    return mapping


# --------------------------------------------------
# MATERIA
# --------------------------------------------------

def load_materia():
    materia_rows = load_csv("Materia")
    param_rows = load_csv("MateriaParam")

    param_map = {}

    for p in param_rows:
        key = p.get("Key") or p.get("#") or p.get("RowId")
        param_map[str(key)] = p

    materia = []

    for m in materia_rows:
        param = m.get("BaseParam")

        stat = None

        if param in param_map:
            stat = param_map[param].get("BaseParam")

        materia.append({
            "name": m.get("Name"),
            "stat": stat,
            "value": int(m.get("Value", 0))
        })

    log(f"Materia loaded ({len(materia)})")

    return materia


# --------------------------------------------------
# ITEM STATS RECONSTRUCTION
# --------------------------------------------------

def extract_stats(item, base_params):

    stats = {}

    for i in range(6):

        param = item.get(f"BaseParam{i}")
        value = item.get(f"BaseParamValue{i}")

        if not param or not value:
            continue

        stat_name = base_params.get(str(param))

        if stat_name:
            stats[stat_name] = int(value)

    return stats


# --------------------------------------------------
# LOAD ITEMS
# --------------------------------------------------

def load_items():

    items = load_csv("Item")
    base_params = load_base_params()
    slots = load_slots()
    jobs = load_class_jobs()

    parsed_items = []

    for item in items:

        name = item.get("Name")

        if not name:
            continue

        slot_id = item.get("EquipSlotCategory")
        slot = slots.get(str(slot_id), {})

        stats = extract_stats(item, base_params)

        parsed_items.append({
            "Name": name,
            "LevelItem": int(item.get("LevelItem", 0)),
            "Slot": slot_id,
            "JobCategory": item.get("ClassJobCategory"),
            "MateriaSlots": int(item.get("MateriaSlotCount", 0)),
            "stats": stats
        })

    log(f"Items parsed ({len(parsed_items)})")

    return parsed_items
