class FoodSystem:
    def __init__(self, foods):
        self.foods = foods

    def get_food_stat(self, food_name, stat_type):
        for food in self.foods:
            if food["name"] == food_name:
                return food.get(stat_type, 0)
        return 0
