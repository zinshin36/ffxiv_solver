from config import ILVL_WINDOW
from engine.blacklist import is_blacklisted


def filter_items(items, blacklist):

    max_ilvl = max(x["ilvl"] for x in items)

    cutoff = max_ilvl - ILVL_WINDOW

    filtered = []

    for item in items:

        if item["ilvl"] < cutoff:
            continue

        if is_blacklisted(item, blacklist):
            continue

        filtered.append(item)

    return filtered


def group_by_slot(items):

    slots = {}

    for item in items:

        slot = item["slot"]

        if slot not in slots:
            slots[slot] = []

        slots[slot].append(item)

    return slots
