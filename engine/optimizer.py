from itertools import product

from engine.materia_system import meld_item
from engine.food_system import apply_food
from engine.blm_math import gcd_bonus
from engine.logger import solver_log


def stat_score(stats, target_gcd):

    main = stats.get("Intelligence", 0)
    crit = stats.get("CriticalHit", 0)
    det = stats.get("Determination", 0)
    dh = stats.get("DirectHitRate", 0)
    sps = stats.get("SpellSpeed", 0)

    value = (
        main * 1.0 +
        crit * 0.45 +
        det * 0.35 +
        dh * 0.30 +
        sps * 0.25
    )

    value += gcd_bonus(sps, target_gcd)

    return value


def solve(items, materia, target_gcd, food):

    slots = {}

    for i in items:
        slots.setdefault(i["slot"], []).append(i)

    for s in slots:

        slots[s] = sorted(
            slots[s],
            key=lambda x: stat_score(x["stats"], target_gcd),
            reverse=True
        )[:6]

    best = None
    best_score = 0

    slot_lists = list(slots.values())

    for combo in product(*slot_lists):

        merged = {}
        melds = []

        for item in combo:

            stats, m = meld_item(item, materia)

            melds.append((item["name"], m))

            for k, v in stats.items():
                merged[k] = merged.get(k, 0) + v

        merged = apply_food(merged, food)

        score = stat_score(merged, target_gcd)

        if score > best_score:
            best_score = score
            best = (combo, melds, merged)

    combo, melds, stats = best

    solver_log("BEST SET")

    for item in combo:
        solver_log(f"{item['slot']} : {item['name']}")

    solver_log("STATS")

    for k, v in stats.items():
        solver_log(f"{k}: {v}")
