PREFERRED_STATS = [
    "CriticalHit",
    "Determination",
    "SpellSpeed",
    "DirectHitRate"
]


MAX_OVERMELD = 5


def meld_item(item, materia):

    guaranteed = item.get("MateriaSlots", 0)

    # crafted gear can go to 5
    total_slots = max(guaranteed, MAX_OVERMELD)

    stats = item["stats"].copy()

    melds = []

    materia_sorted = sorted(
        materia,
        key=lambda x: x["value"],
        reverse=True
    )

    for m in materia_sorted:

        if len(melds) >= total_slots:
            break

        if m["stat"] not in PREFERRED_STATS:
            continue

        stats[m["stat"]] = stats.get(m["stat"], 0) + m["value"]

        melds.append(m)

    return stats, melds
