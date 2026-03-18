def apply_materia(item):

    slots = item.get("materia_slots", 2)

    melds = []

    for _ in range(slots):
        item["crit"] += 36
        melds.append("Crit +36")

    item["melds"] = melds

    return item
