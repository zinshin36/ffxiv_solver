import csv
import os

from engine.runtime_paths import GAME_DATA_DIR


def load_csv(name):

    path = os.path.join(GAME_DATA_DIR, f"{name}.csv")

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{name}.csv not found in {GAME_DATA_DIR}"
        )

    with open(path, encoding="utf8") as f:
        return list(csv.DictReader(f))


def load_items():

    rows = load_csv("Item")

    items = []

    for r in rows:

        try:
            ilvl = int(r.get("LevelItem", 0))
        except:
            continue

        items.append({
            "id": r.get("ID"),
            "name": r.get("Name"),
            "slot": r.get("EquipSlotCategory"),
            "ilvl": ilvl,
            "materia_slots": 2,
            "stats": {}
        })

    return items


def load_materia():

    rows = load_csv("Materia")

    materia = []

    for r in rows:

        stat = r.get("BaseParam")

        try:
            val = int(r.get("Value", 0))
        except:
            continue

        materia.append({
            "stats": {stat: val}
        })

    return materia
