import csv
from engine.logger import log, csv_log

DATA = "data/"


def read_csv(name):

    path = DATA + name

    with open(path, encoding="utf8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    csv_log(f"{name} columns:")
    csv_log(", ".join(rows[0]))

    return rows


def load_items():

    rows = read_csv("Item.csv")

    items = []

    for r in rows[1:]:

        try:

            ilvl = int(r[10])

            if ilvl < 600:
                continue

            slot = r[4]

            stats = {
                "CriticalHit": int(r[50] or 0),
                "Determination": int(r[51] or 0),
                "DirectHitRate": int(r[52] or 0),
                "SpellSpeed": int(r[53] or 0),
                "Intelligence": int(r[40] or 0),
            }

            item = {
                "Name": r[1],
                "slot": slot,
                "ilvl": ilvl,
                "MateriaSlots": int(r[30] or 0),
                "stat_cap": int(r[60] or 9999),
                "stats": stats
            }

            items.append(item)

        except:
            continue

    log(f"Items parsed ({len(items)})")

    return items


def load_materia():

    rows = read_csv("Materia.csv")

    materia = []

    for r in rows[1:]:

        try:

            stat = r[4]

            value = int(r[5])

            materia.append({
                "name": r[1],
                "stat": stat,
                "value": value
            })

        except:
            continue

    log(f"Materia loaded ({len(materia)})")

    return materia
