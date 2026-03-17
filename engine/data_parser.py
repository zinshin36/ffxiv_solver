import csv
from engine.logger import log


def safe_int(val):
    try:
        return int(val)
    except:
        return 0


def is_blm_weapon(name):
    if not name:
        return False

    n = name.lower()

    return any(x in n for x in [
        "rod", "staff", "scepter", "longpole"
    ])


def is_casting_gear(row, headers):
    """
    Detect casting gear using ClassJobCategory
    """

    for key in headers:
        if "classjobcategory" in key.lower():
            val = str(row.get(key, "")).lower()
            if any(x in val for x in [
                "thaumaturge", "black mage", "caster"
            ]):
                return True

    return False


def find_column(headers, keywords):
    for h in headers:
        hl = h.lower()
        if any(k in hl for k in keywords):
            return h
    return None


def parse_items(path):

    items = []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        log(f"Item headers detected ({len(headers)} columns)")

        # --- detect columns dynamically ---
        name_col = find_column(headers, ["name"])
        ilvl_col = find_column(headers, ["levelitem", "itemlevel"])
        slot_col = find_column(headers, ["equipslotcategory"])

        log(f"Using columns -> name:{name_col} ilvl:{ilvl_col} slot:{slot_col}")

        for row in reader:

            name = row.get(name_col)
            ilvl = safe_int(row.get(ilvl_col))

            # sanity filter (fix broken ilvl issue)
            if ilvl <= 0 or ilvl > 1000:
                continue

            slot = row.get(slot_col)

            # --- ONLY casting gear ---
            if not is_casting_gear(row, headers):
                continue

            # --- ONLY BLM weapons ---
            if str(slot) == "1":
                if not is_blm_weapon(name):
                    continue

            item = {
                "name": name,
                "ilvl": ilvl,
                "slot": slot,
                "crit": 0,
                "dh": 0,
                "det": 0,
                "sps": 0,
                "materia_slots": 2
            }

            # --- stat parsing ---
            for h in headers:
                hl = h.lower()
                val = safe_int(row.get(h))

                if "criticalhit" in hl:
                    item["crit"] += val
                elif "directhit" in hl:
                    item["dh"] += val
                elif "determination" in hl:
                    item["det"] += val
                elif "spellspeed" in hl:
                    item["sps"] += val

            items.append(item)

    log(f"Items parsed ({len(items)})")

    max_ilvl = max([i["ilvl"] for i in items], default=0)
    log(f"Highest item level detected: {max_ilvl}")

    return items


# ✅ THIS FIXES YOUR ERROR
def load_all_items(path):
    return parse_items(path)
