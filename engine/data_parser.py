import os
from engine.csv_loader import load_csv, to_int
from engine.logger import log


def is_caster_item(name):
    n = name.lower()

    # allow caster gear only
    if any(x in n for x in [
        "casting",
        "caster",
        "black mage",
        "thaum",
        "rod",
        "staff",
        "grimoire"
    ]):
        return True

    return False


def load_all_items():
    log("Loading Item.csv...")

    rows = load_csv("Item.csv")

    header = rows[0]

    def find_col(keys):
        for i, h in enumerate(header):
            if any(k in h.lower() for k in keys):
                return i
        return None

    name_i = find_col(["name"])
    ilvl_i = find_col(["levelitem", "itemlevel"])
    slot_i = find_col(["equipslotcategory"])
    crit_i = find_col(["criticalhit"])
    det_i = find_col(["determination"])
    dh_i = find_col(["directhit"])
    sps_i = find_col(["spellspeed"])

    items = []
    max_ilvl = 0

    for r in rows[1:]:

        name = r[name_i]

        # 🔥 FILTER HERE
        if not is_caster_item(name):
            continue

        ilvl = to_int(r[ilvl_i])

        item = {
            "name": name,
            "ilvl": ilvl,
            "slot": r[slot_i],
            "crit": to_int(r[crit_i]) if crit_i else 0,
            "det": to_int(r[det_i]) if det_i else 0,
            "dh": to_int(r[dh_i]) if dh_i else 0,
            "sps": to_int(r[sps_i]) if sps_i else 0,
            "materia_slots": 2
        }

        items.append(item)

        if ilvl > max_ilvl:
            max_ilvl = ilvl

    log(f"Caster items loaded: {len(items)}")
    log(f"Max ilvl: {max_ilvl}")

    return items, max_ilvl
