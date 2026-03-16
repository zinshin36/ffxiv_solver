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

    # simple temporary DPS formula
    dps = crit * 1.2 + dh * 1.1 + det * 1.0 + sps * 0.8

    return dps, stats


def group_by_slot(items):

    slots = {}

    for i in items:

        slot = i["slot"]

        if slot not in slots:
            slots[slot] = []

        slots[slot].append(i)

    return slots


def optimize(items):

    log("Starting solver")

    slots = group_by_slot(items)

    slot_items = list(slots.values())

    best_builds = []

    checked = 0

    for combo in itertools.product(*slot_items):

        checked += 1

        dps, stats = score_build(combo)

        best_builds.append((dps, combo))

        best_builds = sorted(best_builds, key=lambda x: x[0], reverse=True)[:5]

        if checked % 5000 == 0:
            log(f"Checked {checked} builds")

    log(f"Total builds checked: {checked}")

    return best_builds


# --------------------------------------------------
# This function is what main.py expects to exist
# --------------------------------------------------

def solve(items, config=None):

    log("Solve() called")

    results = optimize(items)

    builds = []

    for rank, (dps, combo) in enumerate(results, start=1):

        build = {
            "rank": rank,
            "dps": dps,
            "items": [i["name"] for i in combo]
        }

        builds.append(build)

    return builds
