import csv
import os
from engine.logger import log


def load_csv(path):

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    log(f"{os.path.basename(path)} loaded ({len(rows)} rows)")
    return rows


# -------------------------------------------------
# BASE PARAM MAPPING
# -------------------------------------------------

def build_baseparam_map(baseparam_rows):

    mapping = {}

    for row in baseparam_rows:

        key = row.get("Key")

        name = row.get("Name")

        if not key or not name:
            continue

        mapping[key] = name

    log(f"BaseParam mapping built ({len(mapping)} stats)")

    return mapping


# -------------------------------------------------
# PARSE ITEM STATS
# -------------------------------------------------

def extract_item_stats(row, baseparam_map):

    stats = {}

    for i in range(6):

        stat_key = row.get(f"BaseParam[{i}]")
        stat_val = row.get(f"BaseParamValue[{i}]")

        if not stat_key or not stat_val:
            continue

        stat_name = baseparam_map.get(stat_key)

        if not stat_name:
            continue

        try:
            stats[stat_name] = int(stat_val)
        except:
            continue

    return stats


# -------------------------------------------------
# ITEM PARSER
# -------------------------------------------------

def parse_items(item_rows, baseparam_map):

    items = []

    for row in item_rows:

        name = row.get("Name")

        if not name:
            continue

        stats = extract_item_stats(row, baseparam_map)

        if not stats:
            continue

        item = {
            "Name": name,
            "LevelItem": int(row.get("LevelItem", 0)),
            "Slot": row.get("EquipSlotCategory"),
            "JobCategory": row.get("ClassJobCategory"),
            "MateriaSlots": int(row.get("MateriaSlotCount", 0)),
            "stats": stats
        }

        items.append(item)

    log(f"Items parsed ({len(items)})")

    return items


# -------------------------------------------------
# MATERIA PARSER
# -------------------------------------------------

def parse_materia(materia_rows, param_rows):

    param_map = {}

    for row in param_rows:

        param_map[row["Key"]] = row["BaseParam"]

    materia = []

    for row in materia_rows:

        stat_key = row.get("BaseParam")

        stat_name = param_map.get(stat_key)

        if not stat_name:
            continue

        try:
            val = int(row.get("Value", 0))
        except:
            continue

        materia.append({
            "stat": stat_name,
            "value": val
        })

    log(f"Materia loaded ({len(materia)})")

    return materia
