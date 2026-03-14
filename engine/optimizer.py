from itertools import product

from engine.logger import log
from engine.materia_solver import meld_item
from engine.blm_math import gcd_score


def score(stats, target_gcd):

    crit = stats.get("CriticalHit", 0)
    det = stats.get("Determination", 0)
    dh = stats.get("DirectHitRate", 0)
    sps = stats.get("SpellSpeed", 0)
    main = stats.get("Intelligence", 0)

    value = (
        main * 1.0
        + crit * 0.45
        + det * 0.35
        + dh * 0.30
        + sps * 0.25
    )

    value += gcd_score(sps, target_gcd)

    return value


def top_sets(items, materia, target_gcd):

    slots = {}

    for item in items:
        slots.setdefault(item["slot"], []).append(item)

    for s in slots:

        slots[s] = sorted(
            slots[s],
            key=lambda x: score(x["stats"], target_gcd),
            reverse=True
        )[:6]

    slot_lists = list(slots.values())

    best_score = 0
    best_set = None
    best_melds = None
    best_stats = None

    for combo in product(*slot_lists):

        merged = {}
        melds = []

        for item in combo:

            stats, m = meld_item(item, materia)

            melds.append((item["Name"], m))

            for k, v in stats.items():
                merged[k] = merged.get(k, 0) + v

        s = score(merged, target_gcd)

        if s > best_score:

            best_score = s
            best_set = combo
            best_melds = melds
            best_stats = merged

    log("====== BEST BLM SET ======")

    for item in best_set:

        log(f"{item['slot']} : {item['Name']}")

        meld = next(m for n, m in best_melds if n == item["Name"])

        for m in meld:
            log(f"   + {m['name']} {m['stat']} +{m['value']}")

    log("---- TOTAL STATS ----")

    for k, v in best_stats.items():
        log(f"{k}: {v}")
