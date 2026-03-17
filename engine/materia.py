def apply_materia(item):

    slots = item.get("materia_slots", 2)

    # simple priority: crit > dh > det > sps
    for _ in range(slots):

        item["crit"] += 36  # simulate high-grade materia

    return item
