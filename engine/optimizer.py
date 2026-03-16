from engine.logger import log
import itertools


def score_build(build):

    stats = {}

    for item in build:

        for k, v in item["stats"].items():

            stats[k] = stats.get(k, 0) + v

    crit = stats.get("CriticalHit", 0)
    dh = stats.get("DirectHitRate", 0)
    det = stats.get("Determination", 0)
    sps = stats.get("SpellSpeed", 0)

    # simple damage model
    dps = crit * 1.2 + dh * 1.1 + det * 1.0 + sps * 0.8

    return dps, stats


def group_by_slot(items):

    slots = {}

    for i in items:

        s = i["slot"]

        if s not in slots:
            slots[s] = []

        slots[s].append(i)

    return slots


def optimize(items):

    log("Starting solver")

    slots = group_by_slot(items)

    slot_items = list(slots.values())

    best = []

    count = 0

    for combo in itertools.product(*slot_items):

        count += 1

        dps, stats = score_build(combo)

        best.append((dps, combo))

        best = sorted(best, key=lambda x: x[0], reverse=True)[:5]

        if count % 5000 == 0:
            log(f"Checked {count} builds")

    log(f"Total builds checked: {count}")

    return best
