from itertools import product

from engine.logger import log
from engine.materia_solver import meld_item
from engine.blm_math import gcd_score


def score(stats, target_gcd):
    """
    Weighted stat scoring for BLM
    """

    crit = stats.get("CriticalHit", 0)
    det = stats.get("Determination", 0)
    dh = stats.get("DirectHitRate", 0)
    sps = stats.get("SpellSpeed", 0)
    main = stats.get("Intelligence", 0)

    value = (
        main * 1.0
        + crit * 0.45
        + det * 0.35
        + dh * 0.30
        + sps * 0.25
    )

    value += gcd_score(sps, target_gcd)

    return value


def build_slot_map(items):
    """
    Groups items by equipment slot
    """

    slots = {}

    for item in items:
        slot = item.get("slot")

        if not slot:
            continue

        slots.setdefault(slot, []).append(item)

    return slots


def prune_candidates(slots, target_gcd):
    """
    Keeps only the top scoring candidates per slot
    to keep the solver fast.
    """

    pruned = {}

    for slot, items in slots.items():

        items_sorted = sorted(
            items,
            key=lambda x: score(x["stats"], target_gcd),
            reverse=True
        )

        # keep top 6 per slot
        pruned[slot] = items_sorted[:6]

    return pruned


def merge_stats(base, add):

    for k, v in add.items():
        base[k] = base.get(k, 0) + v


def top_sets(items, materia, target_gcd=None):
    """
    Main solver entry point
    """

    if not items:
        log("No items provided to solver")
        return None

    if not materia:
        log("No materia available")
        return None

    slots = build_slot_map(items)

    if not slots:
        log("No slot data found")
        return None

    slots = prune_candidates(slots, target_gcd)

    slot_lists = list(slots.values())

    best_score = -1
    best_combo = None
    best_melds = None
    best_stats = None

    tested = 0

    for combo in product(*slot_lists):

        merged_stats = {}
        meld_info = []

        for item in combo:

            melded_stats, melds = meld_item(item, materia)

            meld_info.append((item["Name"], melds))

            merge_stats(merged_stats, melded_stats)

        s = score(merged_stats, target_gcd)

        tested += 1

        if s > best_score:

            best_score = s
            best_combo = combo
            best_melds = meld_info
            best_stats = merged_stats

    log(f"Solver tested {tested} combinations")

    if not best_combo:
        log("Solver found no valid gear set")
        return None

    log("")
    log("====== BEST BLM SET ======")
    log("")

    for item in best_combo:

        log(f"{item['slot']} : {item['Name']}")

        melds = next(m for n, m in best_melds if n == item["Name"])

        for m in melds:
            log(f"   + {m['name']} ({m['stat']} +{m['value']})")

        if not melds:
            log("   (no materia)")

    log("")
    log("------ TOTAL STATS ------")

    for stat, value in best_stats.items():
        log(f"{stat}: {value}")

    log("")
    log(f"FINAL SCORE: {best_score}")
    log("")

    return best_combo
