from engine.logger import log
from itertools import product


def score(stats):

    crit = stats.get("CriticalHit", 0)
    det = stats.get("Determination", 0)
    sps = stats.get("SpellSpeed", 0)
    dh = stats.get("DirectHitRate", 0)
    main = stats.get("Intelligence", 0)

    return main*1.0 + crit*0.45 + det*0.35 + dh*0.30 + sps*0.25


def merge_stats(items):

    total = {}

    for item in items:

        for k,v in item["stats"].items():

            total[k] = total.get(k,0) + v

    return total


def top_sets(items):

    slots = {}

    for item in items:

        slots.setdefault(item["slot"], []).append(item)

    for s in slots:
        slots[s] = sorted(
            slots[s],
            key=lambda x: score(x["stats"]),
            reverse=True
        )[:5]

    slot_lists = list(slots.values())

    best_score = 0
    best_set = None

    for combo in product(*slot_lists):

        stats = merge_stats(combo)

        s = score(stats)

        if s > best_score:
            best_score = s
            best_set = combo

    log("====== BEST GEAR SET ======")

    for item in best_set:
        log(f"{item['slot']} : {item['Name']}")

    log(f"Score: {best_score}")

    return best_set
