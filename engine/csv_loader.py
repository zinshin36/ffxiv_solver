import csv
import os

from engine.logger import log, csv_log

DATA_DIR = "game_data"


def read_csv(name):

    path = os.path.join(DATA_DIR, name)

    if not os.path.exists(path):
        log(f"Missing CSV: {path}")
        return []

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return []

    csv_log(f"{name} columns:")
    csv_log(", ".join(rows[0]))

    return rows


def safe_int(value):

    try:
        return int(value)
    except:
        return 0


def load_items():

    rows = read_csv("Item.csv")

    if not rows:
        log("Item.csv failed to load")
        return []

    items = []

    for r in rows[1:]:

        try:

            name = r[1]
            slot = r[4]
            ilvl = safe_int(r[10])

            # ignore junk rows
            if not name or ilvl <= 0:
                continue

            stats = {
                "Intelligence": safe_int(r[40]),
                "CriticalHit": safe_int(r[50]),
                "Determination": safe_int(r[51]),
                "DirectHitRate": safe_int(r[52]),
                "SpellSpeed": safe_int(r[53]),
            }

            item = {
                "Name": name,
                "slot": slot,
                "ilvl": ilvl,
                "MateriaSlots": safe_int(r[30]),
                "stat_cap": safe_int(r[60]) or 9999,
                "stats": stats
            }

            items.append(item)

        except Exception as e:
            continue

    log(f"Items parsed ({len(items)})")

    return items


def load_materia():

    rows = read_csv("Materia.csv")

    if not rows:
        log("Materia.csv failed to load")
        return []

    materia = []

    for r in rows[1:]:

        try:

            name = r[1]
            stat = r[4]
            value = safe_int(r[5])

            if not name or value == 0:
                continue

            materia.append({
                "name": name,
                "stat": stat,
                "value": value
            })

        except:
            continue

    log(f"Materia loaded ({len(materia)})")

    return materia
