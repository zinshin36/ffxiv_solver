import os
import csv
from engine.logger import log

GAME_DATA_DIR = os.path.join(os.getcwd(), "game_data")


# --------------------------------------------------
# GENERIC CSV LOADER
# --------------------------------------------------

def load_csv(name):

    path = os.path.join(GAME_DATA_DIR, f"{name}.csv")

    if not os.path.exists(path):
        raise FileNotFoundError(f"{name}.csv not found in {GAME_DATA_DIR}")

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    log(f"{name}.csv loaded ({len(rows)} rows)")
    return rows


def get_id(row):

    return (
        row.get("#")
        or row.get("RowId")
        or row.get("Key")
        or row.get("ID")
    )


# --------------------------------------------------
# BASE PARAM MAP
# --------------------------------------------------

def load_base_params():

    rows = load_csv("BaseParam")

    mapping = {}

    for r in rows:

        key = get_id(r)

        name = r.get("Name") or r.get("Text")

        if key and name:
            mapping[str(key)] = name

    log(f"BaseParam mapping built ({len(mapping)} stats)")

    return mapping


# --------------------------------------------------
# SLOT MAP
# --------------------------------------------------

def load_slots():

    rows = load_csv("EquipSlotCategory")

    slots = {}

    for r in rows:

        key = get_id(r)

        if key:
            slots[str(key)] = r

    return slots


# --------------------------------------------------
# JOB MAP
# --------------------------------------------------

def load_jobs():

    rows = load_csv("ClassJobCategory")

    jobs = {}

    for r in rows:

        key = get_id(r)

        if key:
            jobs[str(key)] = r

    return jobs


# --------------------------------------------------
# ITEM LEVEL MAP
# --------------------------------------------------

def load_item_levels():

    rows = load_csv("ItemLevel")

    levels = {}

    for r in rows:

        key = get_id(r)

        if key:
            levels[str(key)] = r

    return levels


# --------------------------------------------------
# ITEM STAT EXTRACTION
# --------------------------------------------------

def extract_stats(item, base_params):

    stats = {}

    for i in range(10):

        param = (
            item.get(f"BaseParam[{i}]")
            or item.get(f"BaseParam{i}")
        )

        value = (
            item.get(f"BaseParamValue[{i}]")
            or item.get(f"BaseParamValue{i}")
        )

        if not param or not value:
            continue

        stat_name = base_params.get(str(param))

        if not stat_name:
            continue

        try:
            stats[stat_name] = int(value)
        except:
            continue

    return stats


# --------------------------------------------------
# LOAD ITEMS
# --------------------------------------------------

def load_items():

    items = load_csv("Item")

    base_params = load_base_params()
    load_slots()
    load_jobs()
    load_item_levels()

    parsed = []

    for item in items:

        name = item.get("Name")

        if not name:
            continue

        stats = extract_stats(item, base_params)

        if not stats:
            continue

        ilvl = item.get("LevelItem")

        try:
            ilvl = int(ilvl)
        except:
            ilvl = 0

        parsed.append({
            "Name": name,
            "LevelItem": ilvl,
            "Slot": item.get("EquipSlotCategory"),
            "JobCategory": item.get("ClassJobCategory"),
            "MateriaSlots": int(item.get("MateriaSlotCount", 0)),
            "stats": stats
        })

    log(f"Items parsed ({len(parsed)})")

    return parsed


# --------------------------------------------------
# LOAD MATERIA
# --------------------------------------------------

def load_materia():

    materia_rows = load_csv("Materia")
    param_rows = load_csv("MateriaParam")

    param_map = {}

    for p in param_rows:

        key = get_id(p)

        stat = p.get("BaseParam")

        if key and stat:
            param_map[str(key)] = stat

    materia = []

    for m in materia_rows:

        stat_key = m.get("BaseParam")

        stat = param_map.get(str(stat_key))

        try:
            value = int(m.get("Value", 0))
        except:
            value = 0

        if not stat:
            continue

        materia.append({
            "name": m.get("Name"),
            "stat": stat,
            "value": value
        })

    log(f"Materia loaded ({len(materia)})")

    return materia
