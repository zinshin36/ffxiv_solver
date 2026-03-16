from itertools import product
from engine.dps_model import compute_dps
from engine.materia_system import apply_materia
from engine.spell_speed import matches_target


def group_by_slot(items):

    slots = {}

    for i in items:

        s = i["slot"]

        if s not in slots:
            slots[s] = []

        slots[s].append(i)

    return slots


def combine_stats(gear):

    stats = {}

    for g in gear:

        for k, v in g["stats"].items():

            stats[k] = stats.get(k, 0) + v

    return stats


def solve(items, materia, target_gcd):

    slots = group_by_slot(items)

    slot_lists = list(slots.values())

    best = []

    for combo in product(*slot_lists):

        stats = combine_stats(combo)

        if not matches_target(stats.get("sps", 0), target_gcd):
            continue

        melded = []
        meld_names = []

        for g in combo:

            s, meld = apply_materia(g, materia)

            melded.append(s)
            meld_names.append((g["name"], meld))

        final = {}

        for s in melded:

            for k, v in s.items():

                final[k] = final.get(k, 0) + v

        dps = compute_dps(final)

        best.append((dps, meld_names, final))

        best = sorted(best, reverse=True)[:5]

    return best
