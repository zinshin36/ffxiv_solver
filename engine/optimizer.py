from itertools import product

from engine.materia_system import optimize_item_melds
from engine.food_system import FOODS, apply_food
from engine.dps_model import expected_dps
from engine.blm_math import tier_bonus


def solve(items, materia, target_gcd):

    slots = {}

    for item in items:

        slot = item["slot"]

        if slot == "Ring":
            slots.setdefault("Ring1", []).append(item)
            slots.setdefault("Ring2", []).append(item)
        else:
            slots.setdefault(slot, []).append(item)

    slot_lists = list(slots.values())

    best = None
    best_dps = 0

    for combo in product(*slot_lists):

        merged = {}
        build = []

        for item in combo:

            def eval_stats(stats):

                score = expected_dps(stats)

                sps = stats.get("SpellSpeed", 400)

                score += tier_bonus(sps, target_gcd)

                return score

            stats, melds = optimize_item_melds(
                item,
                materia,
                eval_stats
            )

            build.append((item["name"], melds))

            for k, v in stats.items():
                merged[k] = merged.get(k, 0) + v

        for food in FOODS:

            final = apply_food(merged, food)

            dps = expected_dps(final)

            if dps > best_dps:

                best_dps = dps
                best = (build, final, food)

    return best, best_dps
