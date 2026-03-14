from engine.stat_caps import apply_cap

MAX_OVERMELD = 5


def meld_item(item, materia):

    slots = item.get("MateriaSlots", 0)
    max_slots = max(slots, MAX_OVERMELD)

    stats = item["stats"].copy()
    melds = []

    materia_sorted = sorted(materia, key=lambda x: x["value"], reverse=True)

    for m in materia_sorted:

        if len(melds) >= max_slots:
            break

        stat = m["stat"]

        stats[stat] = stats.get(stat, 0) + m["value"]

        stats = apply_cap(item, stats)

        melds.append(m)

    return stats, melds
