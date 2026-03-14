import os
import csv
from engine.logger import log, csv_log

GAME_DATA_DIR = os.path.join(os.getcwd(), "game_data")


def load_csv(name):

    path = os.path.join(GAME_DATA_DIR, f"{name}.csv")

    if not os.path.exists(path):
        raise FileNotFoundError(f"{name}.csv not found in {GAME_DATA_DIR}")

    with open(path, encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames

    log(f"{name}.csv loaded ({len(rows)} rows)")

    if headers:
        csv_log(f"{name}.csv columns:")
        csv_log(", ".join(headers))
        csv_log("")

    return rows


def get(row, col):
    return row.get(str(col))


def get_id(row):
    return row.get("key")


# ---------------------------
# BASE PARAM
# ---------------------------

def load_base_params():

    rows = load_csv("BaseParam")

    mapping = {}

    for r in rows:

        key = get_id(r)
        name = get(r, 0)

        if key and name:
            mapping[str(key)] = name

    log(f"BaseParam mapping built ({len(mapping)} stats)")

    return mapping


# ---------------------------
# SLOT CATEGORY
# ---------------------------

def load_slots():

    rows = load_csv("EquipSlotCategory")

    slots = {}

    for r in rows:

        key = get_id(r)

        name = get(r, 0)

        if key:
            slots[key] = name

    return slots


# ---------------------------
# JOB CATEGORY
# ---------------------------

def load_job_categories():

    rows = load_csv("ClassJobCategory")

    jobs = {}

    for r in rows:

        key = get_id(r)

        # column 33 = Black Mage flag
        if get(r, 33) == "1":
            jobs[key] = True

    return jobs


# ---------------------------
# ITEMS
# ---------------------------

def load_items(min_ilvl=700):

    items = load_csv("Item")

    base_params = load_base_params()
    slots = load_slots()
    blm_jobs = load_job_categories()

    parsed = []

    for item in items:

        name = get(item, 9)

        if not name:
            continue

        job_cat = get(item, 63)

        if job_cat not in blm_jobs:
            continue

        ilvl = get(item, 24)

        try:
            ilvl = int(ilvl)
        except:
            continue

        if ilvl < min_ilvl:
            continue

        slot_id = get(item, 10)
        slot = slots.get(slot_id, "Unknown")

        stats = {}

        stat_pairs = [
            (68, 69),
            (70, 71),
            (72, 73),
            (74, 75),
            (76, 77),
        ]

        for param_col, value_col in stat_pairs:

            param = get(item, param_col)
            value = get(item, value_col)

            if not param or not value:
                continue

            stat_name = base_params.get(param)

            if not stat_name:
                continue

            try:
                value = int(value)
            except:
                continue

            if value > 0:
                stats[stat_name] = value

        if not stats:
            continue

        parsed.append({
            "Name": name,
            "LevelItem": ilvl,
            "slot": slot,
            "stats": stats
        })

    log(f"BLM items after ilvl filter: {len(parsed)}")

    return parsed


# ---------------------------
# MATERIA
# ---------------------------

def load_materia():

    materia_rows = load_csv("Materia")
    base_params = load_base_params()

    materia = []

    for m in materia_rows:

        stat_key = get(m, 2)
        value = get(m, 3)

        stat = base_params.get(stat_key)

        if not stat:
            continue

        try:
            value = int(value)
        except:
            continue

        if value <= 0:
            continue

        materia.append({
            "stat": stat,
            "value": value
        })

    log(f"Materia loaded ({len(materia)})")

    return materia
