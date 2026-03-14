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

    score = (
        main * 1.0 +
        crit * 0.45 +
        det * 0.35 +
        dh * 0.30 +
        sps * 0.25
    )

    score += gcd_bonus(sps, target_gcd)

    return score


def build_slot_map(items):

    slots = {}

    for i in items:
        slots.setdefault(i["slot"], []).append(i)

    if "Ring" in slots:
        slots["Ring1"] = slots["Ring"]
        slots["Ring2"] = slots["Ring"]

    return slots


def prune_candidates(slots, target_gcd, limit=6):

    for s in slots:

        slots[s] = sorted(
            slots[s],
            key=lambda x: stat_score(x["stats"], target_gcd),
            reverse=True
        )[:limit]

    return slots


def solve(items, materia, target_gcd, food):

    slots = build_slot_map(items)

    slots = prune_candidates(slots, target_gcd)

    slot_lists = list(slots.values())

    best_score = 0
    best = None

    tested = 0

    for combo in product(*slot_lists):

        tested += 1

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

    solver_log(f"Combinations tested: {tested}")

    combo, melds, stats = best

    solver_log("BEST SET")

    for item in combo:
        solver_log(f"{item['slot']} : {item['name']}")

    solver_log("MELDS")

    for name, m in melds:

        meld_names = [x["name"] for x in m]

        solver_log(f"{name}: {', '.join(meld_names)}")

    solver_log("FINAL STATS")

    for k, v in stats.items():
        solver_log(f"{k}: {v}")
