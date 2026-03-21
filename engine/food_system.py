# engine/food_system.py

import json
import os

class FoodSystem:
    def __init__(self, game_data_path="game_data/foods.json"):
        self.game_data_path = game_data_path
        self.foods = self.load_foods()

    def load_foods(self):
        if not os.path.exists(self.game_data_path):
            print(f"[ERROR] foods.json not found at {self.game_data_path}")
            return []
        with open(self.game_data_path, "r", encoding="utf-8") as f:
            try:
                foods = json.load(f)
                return foods
            except json.JSONDecodeError as e:
                print(f"[ERROR] Failed to parse foods.json: {e}")
                return []

    def get_food_bonus(self, food_name):
        """Return the stat bonus for a given food name."""
        for food in self.foods:
            if food.get("name") == food_name:
                return {
                    "crit": food.get("crit", 0),
                    "dh": food.get("dh", 0),
                    "det": food.get("det", 0),
                    "sps": food.get("sps", 0)
                }
        # Default to no bonus if food not found
        return {"crit": 0, "dh": 0, "det": 0, "sps": 0}
