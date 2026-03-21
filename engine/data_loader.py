import csv
import os
import json

class DataLoader:
    def __init__(self, game_data_path="game_data"):
        self.game_data_path = game_data_path
        self.items = {}
        self.materia = {}
        self.foods = []

    def load_items(self):
        path = os.path.join(self.game_data_path, "Item.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Item.csv not found at {path}")
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item_id = row["ID"]
                self.items[item_id] = row
        print(f"[INFO] Loaded {len(self.items)} items")

    def load_materia(self):
        path = os.path.join(self.game_data_path, "Materia.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Materia.csv not found at {path}")
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mat_id = row["ID"]
                self.materia[mat_id] = row
        print(f"[INFO] Loaded {len(self.materia)} materia")

    def load_foods(self):
        path = os.path.join(self.game_data_path, "foods.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"foods.json not found at {path}")
        with open(path, encoding="utf-8") as f:
            self.foods = json.load(f)
        print(f"[INFO] Loaded {len(self.foods)} foods")

    def load_all(self):
        self.load_items()
        self.load_materia()
        self.load_foods()
