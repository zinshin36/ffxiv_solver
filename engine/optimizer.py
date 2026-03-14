from itertools import product

from engine.logger import log
from engine.blm_math import gcd_bonus
from engine.materia_solver import meld_item


def score(stats):

    crit = stats.get("CriticalHit",0)
    det = stats.get("Determination",0)
    sps = stats.get("SpellSpeed",0)
    dh = stats.get("DirectHitRate",0)
    main = stats.get("Intelligence",0)

    value = (
        main*1.0 +
        crit*0.45 +
        det*0.35 +
        dh*0.30 +
        sps*0.25
    )

    value += gcd_bonus(sps)

    return value


def top_sets(items, materia):

    slots = {}

    for item in items:
        slots.setdefault(item["slot"], []).append(item)

    for s in slots:

        slots[s] = sorted(
            slots[s],
            key=lambda x: score(x["stats"]),
            reverse=True
        )[:6]

    slot_lists = list(slots.values())

    best_score = 0
    best_set = None
    best_melds = None

    for combo in product(*slot_lists):

        total = {}
        melds = []

        for item in combo:

            stats, used = meld_item(item, materia)

            melds.append((item["Name"], used))

            for k,v in stats.items():
                total[k] = total.get(k,0) + v

        s = score(total)

        if s > best_score:

            best_score = s
            best_set = combo
            best_melds = melds

    log("====== BEST BLM SET ======")

    for item in best_set:

        log(f"{item['slot']} : {item['Name']}")

        meld = next(m for n,m in best_melds if n == item["Name"])

        for m in meld:
            log(f"   + {m['name']} ({m['stat']} +{m['value']})")

    log(f"Score: {best_score}")

    return best_set
