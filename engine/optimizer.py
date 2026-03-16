from itertools import product

from engine.dominance import prune
from engine.dps_model import compute_dps
from engine.materia_system import optimize_materia
from engine.spell_speed import matches_target
from engine.food_system import apply_food


def group_slots(items):

    slots = {}

    for i in items:

        s = i["slot"]

        if s not in slots:
            slots[s] = []

        slots[s].append(i)

    for k in slots:

        slots[k] = prune(slots[k])

    return slots


def ring_rule(combo):

    rings = [x for x in combo if "Ring" in x["name"]]

    if len(rings) < 2:
        return True

    return rings[0]["name"] != rings[1]["name"]


def combine_stats(stats_list):

    result = {}

    for s in stats_list:

        for k, v in s.items():

            result[k] = result.get(k, 0) + v

    return result


def solve(items, materia, target_gcd, food):

    slots = group_slots(items)

    slot_lists = list(slots.values())

    best = []

    tested = 0

    for combo in product(*slot_lists):

        if not ring_rule(combo):
            continue

        tested += 1

        melded = []
        meld_names = []

        for g in combo:

            s, m = optimize_materia(g, materia)

            melded.append(s)
            meld_names.append((g["name"], m))

        stats = combine_stats(melded)

        stats = apply_food(stats, food)

        if not matches_target(stats.get("sps", 0), target_gcd):
            continue

        dps = compute_dps(stats)

        best.append((dps, meld_names, stats))

        best = sorted(best, reverse=True)[:5]

        if tested % 100000 == 0:
            print("tested builds:", tested)

    return best
