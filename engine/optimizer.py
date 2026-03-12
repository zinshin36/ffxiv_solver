from itertools import product
from engine.simulator import score
from engine.materia import apply_materia
from engine.logger import logging

def filter_blacklist(items, blacklist):
    if not blacklist:
        return items
    filtered = [i for i in items if i["name"] not in blacklist]
    logging.info(f"Removed {len(items) - len(filtered)} items due to blacklist")
    return filtered

def top_sets(items, materia_list, blacklist=None, ilvl_window=25, top_n=10):
    """Return top N DPS gear sets."""

    if blacklist is None:
        blacklist = []

    items = filter_blacklist(items, blacklist)

    # remove anything more than ilvl_window below max
    max_ilvl = max(i["ilvl"] for i in items)
    items = [i for i in items if i["ilvl"] >= max_ilvl - ilvl_window]

    # group by slot
    slots = {}
    for i in items:
        slots.setdefault(i["slot"], []).append(i)

    all_combos = list(product(*(slots[k] for k in slots)))
    results = []

    for combo in all_combos:
        gear_set = {}
        for i in combo:
            item_copy = i.copy()
            gear_set[i["slot"]] = apply_materia(item_copy, materia_list)
        dps = score(gear_set)
        results.append({"gear": gear_set, "dps": dps})

    # sort top N
    results.sort(key=lambda x: x["dps"], reverse=True)
    return results[:top_n]
