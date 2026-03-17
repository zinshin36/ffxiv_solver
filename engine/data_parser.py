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

        # 🔥 detect stat columns ONCE
        crit_cols = find_all_columns(headers, "criticalhit")
        dh_cols = find_all_columns(headers, "directhit")
        det_cols = find_all_columns(headers, "determination")
        sps_cols = find_all_columns(headers, "spellspeed")

        log(f"Using columns -> name:{name_col} ilvl:{ilvl_col} slot:{slot_col}")
        log(f"Stat columns -> crit:{len(crit_cols)} dh:{len(dh_cols)} det:{len(det_cols)} sps:{len(sps_cols)}")

        for i, row in enumerate(reader):

            if i % 5000 == 0 and i > 0:
                log(f"Parsing items... {i}")

            name = row.get(name_col)
            ilvl = safe_int(row.get(ilvl_col))

            if ilvl <= 0 or ilvl > 1000:
                continue

            slot = row.get(slot_col)

            # --- casting filter (FAST) ---
            is_casting = False
            for col in classjob_cols:
                val = row.get(col)
                if val and ("Black Mage" in val or "Thaumaturge" in val or "Caster" in val):
                    is_casting = True
                    break

            if not is_casting:
                continue

            # --- weapon filter ---
            if str(slot) == "1":
                if not is_blm_weapon(name):
                    continue

            # --- stats (FAST: no header scan) ---
            crit = sum(safe_int(row.get(c)) for c in crit_cols)
            dh = sum(safe_int(row.get(c)) for c in dh_cols)
            det = sum(safe_int(row.get(c)) for c in det_cols)
            sps = sum(safe_int(row.get(c)) for c in sps_cols)

            item = {
                "name": name,
                "ilvl": ilvl,
                "slot": slot,
                "crit": crit,
                "dh": dh,
                "det": det,
                "sps": sps,
                "materia_slots": 2
            }

            items.append(item)

    log(f"Items parsed ({len(items)})")

    max_ilvl = max([i["ilvl"] for i in items], default=0)
    log(f"Highest item level detected: {max_ilvl}")

    return items


def load_all_items(path):
    return parse_items(path)
