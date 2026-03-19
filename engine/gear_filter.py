# REPLACE ENTIRE FILE

from config import ILVL_WINDOW
from engine.blacklist import is_blacklisted


def filter_items(items, blacklist):

    max_ilvl = max(x["ilvl"] for x in items)
    cutoff = max_ilvl - ILVL_WINDOW

    out = []

    for item in items:

        if item["ilvl"] < cutoff:
            continue

        if is_blacklisted(item["name"], blacklist):
            continue

        out.append(item)

    return out
