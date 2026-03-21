import csv
import os
from engine.runtime_paths import GAME_DATA_DIR

SLOTS = ["weapon","head","body","hands","legs","feet","earrings","necklace","bracelet","ring1","ring2"]

def parse_stats(row):
    stats = {}
    for stat in ["int","crit","dh","det","sps"]:
        if stat in row and row[stat]:
            stats[stat] = int(row[stat])
    return stats

def parse_melds(row):
    melds = {}
    for stat in ["crit","dh","det","sps"]:
        if stat in row and row[stat + "_meld"]:
            melds[stat] = int(row[stat + "_meld"])
    return melds

def load_items():
    items_by_slot = {slot: [] for slot in SLOTS}
    for filename in os.listdir(GAME_DATA_DIR):
        if filename.endswith(".csv"):
            filepath = os.path.join(GAME_DATA_DIR, filename)
            with open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    slot = row.get("slot", "").lower()
                    if slot not in SLOTS:
                        continue
                    item = {
                        "name": row.get("name", "Unknown"),
                        "ilvl": int(row.get("ilvl", 0)),
                        "stats": parse_stats(row),
                        "melds": parse_melds(row)
                    }
                    items_by_slot[slot].append(item)
    # Detect highest iLvl per slot
    for slot in SLOTS:
        if items_by_slot[slot]:
            items_by_slot[slot].sort(key=lambda x: x["ilvl"], reverse=True)
    return items_by_slot
