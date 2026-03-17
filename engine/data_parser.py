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


def find_column(headers, keywords):
    for h in headers:
        hl = h.lower()
        if any(k in hl for k in keywords):
            return h
    return None


def find_all_columns(headers, keyword):
    return [h for h in headers if keyword in h.lower()]


def parse_items(path):

    items = []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        log(f"Item headers detected ({len(headers)} columns)")

        # --- detect columns ONCE ---
        name_col = find_column(headers, ["name"])
        ilvl_col = find_column(headers, ["levelitem", "itemlevel"])
        slot_col = find_column(headers, ["equipslotcategory"])

        classjob_cols = find_all_columns(headers, "classjobcategory")

        log(f"Using columns -> name:{name_col} ilvl:{ilvl_col} slot:{slot_col}")
        log(f"ClassJobCategory columns: {len(classjob_cols)}")

        for i, row in enumerate(reader):

            # optional progress so you SEE it's working
            if i % 5000 == 0 and i > 0:
                log(f"Parsing items... {i}")

            name = row.get(name_col)
            ilvl = safe_int(row.get(ilvl_col))

            # sanity filter
            if ilvl <= 0 or ilvl > 1000:
                continue

            slot = row.get(slot_col)

            # --- FAST casting check ---
            is_casting = False
            for col in classjob_cols:
                val = str(row.get(col, "")).lower()
                if "black mage" in val or "thaumaturge" in val or "caster" in val:
                    is_casting = True
                    break

            if not is_casting:
                continue

            # --- weapon filter ---
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


def load_all_items(path):
    return parse_items(path)
