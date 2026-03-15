from itertools import product

from engine.materia_system import optimize_item_melds
from engine.dps_model import expected_dps
from engine.food_system import apply_food


def solve(items, materia, foods):

    slots = {}

    for item in items:

        slot = item["slot"]

        if slot == "Ring":
            slots.setdefault("Ring1", []).append(item)
            slots.setdefault("Ring2", []).append(item)
        else:
            slots.setdefault(slot, []).append(item)

    slot_lists = list(slots.values())

    best_build = None
    best_stats = None
    best_food = None
    best_dps = 0

    for combo in product(*slot_lists):

        merged_stats = {}
        build = []

        for item in combo:

            def stat_eval(stats):
                return expected_dps(stats)

            stats, melds = optimize_item_melds(
                item,
                materia,
                stat_eval
            )

            build.append((item["name"], melds))

            for k, v in stats.items():
                merged_stats[k] = merged_stats.get(k, 0) + v

        for food in foods:

            final_stats = apply_food(merged_stats, food)

            dps = expected_dps(final_stats)

            if dps > best_dps:

                best_dps = dps
                best_build = build
                best_stats = final_stats
                best_food = food

    return (best_build, best_stats, best_food), best_dps
