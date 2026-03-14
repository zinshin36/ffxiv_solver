from engine.logger import log


PREFERRED_STATS = [
    "CriticalHit",
    "Determination",
    "SpellSpeed",
    "DirectHitRate"
]


def apply_materia(item, materia):

    slots = item.get("MateriaSlots", 2)

    stats = item["stats"].copy()

    sorted_materia = sorted(
        materia,
        key=lambda x: x["value"],
        reverse=True
    )

    used = 0

    for m in sorted_materia:

        if used >= slots:
            break

        if m["stat"] not in PREFERRED_STATS:
            continue

        stats[m["stat"]] = stats.get(m["stat"], 0) + m["value"]

        used += 1

    return stats
