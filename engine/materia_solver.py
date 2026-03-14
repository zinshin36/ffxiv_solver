from engine.logger import log


PREFERRED_STATS = [
    "CriticalHit",
    "Determination",
    "SpellSpeed",
    "DirectHitRate"
]


def meld_item(item, materia):

    slots = item["MateriaSlots"]

    if slots <= 0:
        return item["stats"], []

    stats = item["stats"].copy()

    melds = []

    materia_sorted = sorted(
        materia,
        key=lambda m: m["value"],
        reverse=True
    )

    for m in materia_sorted:

        if len(melds) >= slots:
            break

        if m["stat"] not in PREFERRED_STATS:
            continue

        stats[m["stat"]] = stats.get(m["stat"],0) + m["value"]

        melds.append(m)

    return stats, melds
