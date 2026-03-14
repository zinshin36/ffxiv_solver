from itertools import product

from engine.logger import log
from engine.blm_math import gcd_score
from engine.materia_solver import meld_item


def score(stats, target_gcd):

    crit = stats.get("CriticalHit", 0)
    det = stats.get("Determination", 0)
    sps = stats.get("SpellSpeed", 0)
    dh = stats.get("DirectHitRate", 0)
    main = stats.get("Intelligence", 0)

    value = (
        main * 1.0 +
        crit * 0.45 +
        det * 0.35 +
        dh * 0.30 +
        sps * 0.25
    )

    value += gcd_score(sps, target_gcd)

    return value


def top_sets(items, materia, target_gcd):

    slots = {}

    for item in items:
        slots.setdefault(item["slot"], []).append(item)

    # prune slot candidates
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

        merged_stats = {}
        meld_data = []

        for item in combo:

            stats, melds = meld_item(item, materia)

            meld_data.append((item["Name"], melds))

            for k, v in stats.items():
                merged_stats[k] = merged_stats.get(k, 0) + v

        s = score(merged_stats, target_gcd)

        if s > best_score:

            best_score = s
            best_set = combo
            best_melds = meld_data
            best_stats = merged_stats

    log("====== BEST BLM SET ======")

    for item in best_set:

        log(f"{item['slot']} : {item['Name']}")

        melds = next(m for n, m in best_melds if n == item["Name"])

        for m in melds:
            log(f"   + {m['name']} ({m['stat']} +{m['value']})")

    log("------ TOTAL STATS ------")

    for k, v in best_stats.items():
        log(f"{k}: {v}")

    log(f"Score: {best_score}")

    return best_set
