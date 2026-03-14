import csv
import os

from engine.logger import log, csv_log

DATA = "game_data"


def read_csv(name):

    path = os.path.join(DATA, name)

    if not os.path.exists(path):

        log(f"Missing CSV: {path}")
        return []

    with open(path, encoding="utf-8-sig") as f:

        reader = csv.reader(f)
        rows = list(reader)

    csv_log(f"{name} columns:")
    csv_log(", ".join(rows[0]))

    return rows


def safe_int(v):

    try:
        return int(v)
    except:
        return 0


def load_baseparams():

    rows = read_csv("BaseParam.csv")

    params = {}

    for r in rows[1:]:

        param_id = r[0]
        name = r[1]

        params[param_id] = name

    return params


def load_materia():

    materia_rows = read_csv("Materia.csv")
    param_rows = read_csv("MateriaParam.csv")

    param_map = {}

    for r in param_rows[1:]:

        materia_id = r[0]
        stat = r[1]
        value = safe_int(r[2])

        param_map[materia_id] = (stat, value)

    materia = []

    for r in materia_rows[1:]:

        materia_id = r[0]
        name = r[1]

        if materia_id not in param_map:
            continue

        stat, value = param_map[materia_id]

        materia.append({
            "name": name,
            "stat": stat,
            "value": value
        })

    log(f"Materia loaded ({len(materia)})")

    return materia


def load_items():

    rows = read_csv("Item.csv")

    items = []

    for r in rows[1:]:

        name = r[1]

        if not name:
            continue

        ilvl = safe_int(r[10])

        stats = {
            "Intelligence": safe_int(r[40]),
            "CriticalHit": safe_int(r[50]),
            "Determination": safe_int(r[51]),
            "DirectHitRate": safe_int(r[52]),
            "SpellSpeed": safe_int(r[53]),
        }

        item = {
            "Name": name,
            "slot": r[4],
            "ilvl": ilvl,
            "MateriaSlots": safe_int(r[30]),
            "stats": stats
        }

        items.append(item)

    log(f"Items parsed ({len(items)})")

    return items
