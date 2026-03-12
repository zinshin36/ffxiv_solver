import csv
import os
from config import GAME_DATA_FOLDER


def load_csv(name):

    path = os.path.join(GAME_DATA_FOLDER, f"{name}.csv")

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


def load_item_params():

    rows = load_csv("ItemBaseParam")

    data = {}

    for r in rows:

        item = r.get("Item")

        stat = r.get("BaseParam")

        try:
            val = int(r.get("Value", 0))
        except:
            val = 0

        if item not in data:
            data[item] = {}

        data[item][stat] = val

    return data


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
