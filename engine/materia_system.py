class MateriaSystem:
    def __init__(self, items, materia):
        self.items = items
        self.materia = materia

    def meld_item(self, item_id, materia_ids):
        if item_id not in self.items:
            return None
        item = self.items[item_id].copy()
        total_stats = {}
        for mid in materia_ids:
            if mid not in self.materia:
                continue
            mat = self.materia[mid]
            for stat, val in mat.items():
                if stat.startswith("Param"):
                    total_stats[stat] = total_stats.get(stat, 0) + int(val)
        # Apply stats to item
        for stat, val in total_stats.items():
            item[stat] = str(int(item.get(stat, 0)) + val)
        return item
