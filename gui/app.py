# gui/app.py

import os
import csv
from engine.food_system import FoodSystem

class BISApp:
    def __init__(self, game_data_path="game_data"):
        self.game_data_path = game_data_path
        self.food_system = FoodSystem(os.path.join(game_data_path, "foods.json"))
        self.items_by_slot = {}
        self.materia_list = []
        self.highest_ilvl = 0
        self.load_game_data()

    def load_game_data(self):
        self.load_items()
        self.load_materia()
        self.detect_highest_ilvl()

    def load_items(self):
        item_csv_path = os.path.join(self.game_data_path, "Item.csv")
        if not os.path.exists(item_csv_path):
            print(f"[ERROR] Item.csv not found at {item_csv_path}")
            return

        with open(item_csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                slot = row.get("Slot")
                ilvl = int(row.get("ItemLevel", 0))
                name = row.get("Name")
                stats = {
                    "crit": int(row.get("Crit", 0)),
                    "dh": int(row.get("DirectHit", 0)),
                    "det": int(row.get("Determination", 0)),
                    "sps": int(row.get("SpellSpeed", 0))
                }
                if slot not in self.items_by_slot:
                    self.items_by_slot[slot] = []
                self.items_by_slot[slot].append({"name": name, "ilvl": ilvl, "stats": stats})

    def load_materia(self):
        materia_csv_path = os.path.join(self.game_data_path, "Materia.csv")
        if not os.path.exists(materia_csv_path):
            print(f"[WARNING] Materia.csv not found at {materia_csv_path}")
            return

        with open(materia_csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.materia_list.append({
                    "name": row.get("Name"),
                    "stat": row.get("Stat"),
                    "value": int(row.get("Value", 0))
                })

    def detect_highest_ilvl(self):
        max_ilvl = 0
        for slot_items in self.items_by_slot.values():
            for item in slot_items:
                if item["ilvl"] > max_ilvl:
                    max_ilvl = item["ilvl"]
        self.highest_ilvl = max_ilvl

    def apply_food_to_stats(self, base_stats, food_name):
        food_bonus = self.food_system.get_food_bonus(food_name)
        return {
            stat: base_stats.get(stat, 0) + food_bonus.get(stat, 0)
            for stat in ["crit", "dh", "det", "sps"]
        }

    def filter_items(self, min_ilvl=780):
        filtered = {}
        for slot, items in self.items_by_slot.items():
            filtered[slot] = [item for item in items if item["ilvl"] >= min_ilvl]
        return filtered

    def solve(self, min_ilvl=780, gcd=2.5, food="Popoto Potage", build_type="Crit"):
        filtered_items = self.filter_items(min_ilvl)
        print(f"[RUN] Min iLvl={min_ilvl} | GCD={gcd} | Food={food} | Build Type={build_type}")
        # Example: sum base stats + food (real solver would apply materia combos)
        for slot, items in filtered_items.items():
            for item in items:
                total_stats = self.apply_food_to_stats(item["stats"], food)
                print(f"Slot: {slot}, Item: {item['name']}, Stats w/ Food: {total_stats}")
        print(f"Highest iLvl detected: {self.highest_ilvl}")
