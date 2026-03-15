from itertools import product

from engine.materia_system import meld_item
from engine.blm_math import gcd_bonus
from engine.logger import log


def stat_score(stats, target_gcd):

    main = stats.get("Intelligence", 0)
    crit = stats.get("CriticalHit", 0)
    det = stats.get("Determination", 0)
    dh = stats.get("DirectHitRate", 0)
    sps = stats.get("SpellSpeed", 0)

    score = (
        main * 1.0 +
        crit * 0.45 +
        det * 0.35 +
        dh * 0.30 +
        sps * 0.25
    )

    score += gcd_bonus(sps, target_gcd)

    return score


def solve(items, materia, target_gcd):

    slots = {}

    for i in items:
        slots.setdefault(i["slot"], []).append(i)

    for s in slots:
        slots[s] = sorted(
            slots[s],
            key=lambda x: stat_score(x["stats"], target_gcd),
            reverse=True
        )[:5]

    slot_lists = list(slots.values())

    best = None
    best_score = 0

    for combo in product(*slot_lists):

        merged = {}
        melds = []

        for item in combo:

            stats, m = meld_item(item, materia)

            melds.append((item["name"], m))

            for k, v in stats.items():
                merged[k] = merged.get(k, 0) + v

        score = stat_score(merged, target_gcd)

        if score > best_score:
            best_score = score
            best = (combo, melds, merged)

    combo, melds, stats = best

    log("BEST SET")

    for item in combo:
        log(f"{item['slot']} : {item['name']}")

    log("MELDS")

    for name, m in melds:
        log(f"{name}: {', '.join(x['name'] for x in m)}")

    log("STATS")

    for k, v in stats.items():
        log(f"{k}: {v}")
