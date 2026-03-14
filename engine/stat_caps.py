STAT_COLUMNS = [
    "CriticalHit",
    "Determination",
    "DirectHitRate",
    "SpellSpeed"
]


def apply_cap(item, stats):

    capped = stats.copy()

    cap = item.get("stat_cap", 9999)

    for s in STAT_COLUMNS:

        if s in capped:
            capped[s] = min(capped[s], cap)

    return capped
