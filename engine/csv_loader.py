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


def get(row, column):

    return row.get(column) or row.get(str(column))


def get_id(row):

    return get(row, "key")


# --------------------------------------------------
# BASE PARAM
# --------------------------------------------------

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


# --------------------------------------------------
# ITEM PARSER
# --------------------------------------------------

def load_items():

    items = load_csv("Item")

    base_params = load_base_params()

    parsed = []

    for item in items:

        name = get(item, 9)

        if not name:
            continue

        ilvl = get(item, 24)

        try:
            ilvl = int(ilvl)
        except:
            ilvl = 0

        stats = {}

        # BaseParam indexes (Godbert export)
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

            stat_name = base_params.get(str(param))

            if not stat_name:
                continue

            try:
                stats[stat_name] = int(value)
            except:
                continue

        if not stats:
            continue

        parsed.append({
            "Name": name,
            "LevelItem": ilvl,
            "stats": stats,
        })

    log(f"Items parsed ({len(parsed)})")

    return parsed


# --------------------------------------------------
# MATERIA
# --------------------------------------------------

def load_materia():

    materia_rows = load_csv("Materia")
    param_rows = load_csv("MateriaParam")

    param_map = {}

    for p in param_rows:

        key = get_id(p)
        stat = get(p, 0)

        if key and stat:
            param_map[str(key)] = stat

    materia = []

    for m in materia_rows:

        stat_key = get(m, 2)
        value = get(m, 3)

        stat = param_map.get(str(stat_key))

        try:
            value = int(value)
        except:
            value = 0

        if not stat:
            continue

        materia.append({
            "stat": stat,
            "value": value
        })

    log(f"Materia loaded ({len(materia)})")

    return materia
