import csv
import os
from config import GAME_DATA_FOLDER


def load_csv(name):

    path = os.path.join(GAME_DATA_FOLDER, f"{name}.csv")

    with open(path, newline='', encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_items():

    items = load_csv("Item")

    parsed = []

    for row in items:

        try:
            ilvl = int(row.get("LevelItem", 0))
        except:
            continue

        name = row.get("Name", "")

        slot = row.get("EquipSlotCategory", "")

        parsed.append({
            "name": name,
            "slot": slot,
            "ilvl": ilvl,
            "materia_slots": 2,
            "stats": {}
        })

    return parsed


def load_item_params():

    rows = load_csv("ItemBaseParam")

    data = {}

    for r in rows:

        item = r.get("Item")

        stat = r.get("BaseParam")

        try:
            value = int(r.get("Value", 0))
        except:
            value = 0

        if item not in data:
            data[item] = {}

        data[item][stat] = value

    return data


def load_materia():

    rows = load_csv("Materia")

    materia = []

    for r in rows:

        stat = r.get("BaseParam")

        try:
            value = int(r.get("Value", 0))
        except:
            continue

        materia.append({
            "stats": {stat: value}
        })

    return materia
