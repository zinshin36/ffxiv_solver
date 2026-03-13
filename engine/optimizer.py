# engine/optimizer.py
from itertools import product
from engine.simulator import simulate_dps
from engine.logger import log

def filter_blacklist(items, blacklist):
    if not blacklist:
        return items
    filtered = [i for i in items if i["Name"] not in blacklist]
    log(f"Blacklist removed {len(items) - len(filtered)} items")
    return filtered

def split_by_slot(items):
    slots = {}
    for item in items:
        slot = str(item.get("EquipSlotCategory", "Unknown"))
        slots.setdefault(slot, []).append(item)
    return slots

def pick_highest_ilvl_per_slot(slots):
    best = []
    for slot, items in slots.items():
        sorted_items = sorted(items, key=lambda x: int(x.get("LevelItem", 0)), reverse=True)
        best.append(sorted_items[0])
    return best

def build_best_set(items, blacklist=None):
    if blacklist is None:
        blacklist = []
    items = filter_blacklist(items, blacklist)
    slots = split_by_slot(items)
    best = pick_highest_ilvl_per_slot(slots)
    log(f"Built best set with {len(best)} pieces")
    return best

def top_sets(items, top_n=10, blacklist=None):
    if blacklist is None:
        blacklist = []
    items = filter_blacklist(items, blacklist)
    slots = split_by_slot(items)
    slot_keys = list(slots.keys())
    all_combos = product(*(slots[k] for k in slot_keys))
    scored_sets = []
    for combo in all_combos:
        gear_set = {slot_keys[i]: dict(item) for i, item in enumerate(combo)}
        dps = simulate_dps(gear_set)
        scored_sets.append({"gear": gear_set, "dps": dps})
    scored_sets.sort(key=lambda x: x["dps"], reverse=True)
    return scored_sets[:top_n]
