def apply_materia(item, materia_list):
    """Apply materia to the item stats."""
    slots = item.get("materia_slots", 0)
    sorted_materia = sorted(materia_list, key=lambda x: list(x["stats"].values())[0], reverse=True)

    for i in range(slots):
        if i < len(sorted_materia):
            stat, val = list(sorted_materia[i]["stats"].items())[0]
            item["stats"][stat] = item["stats"].get(stat, 0) + val

    item["MateriaApplied"] = slots
    return item
