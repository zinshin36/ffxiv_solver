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
    return any(x in n for x in ["rod", "staff", "scepter", "longpole"])


def find_col_index(headers, keywords):
    for i, h in enumerate(headers):
        hl = h.lower()
        if any(k in hl for k in keywords):
            return i
    return None


def find_all_indices(headers, keyword):
    return [i for i, h in enumerate(headers) if keyword in h.lower()]


def parse_items(path):

    items = []

    # 🔥 IMPORTANT: newline="" fixes csv stalls on Windows
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        headers = next(reader)

        log(f"Item headers detected ({len(headers)} columns)")

        # --- detect column indices ONCE ---
        name_i = find_col_index(headers, ["name"])
        ilvl_i = find_col_index(headers, ["levelitem", "itemlevel"])
        slot_i = find_col_index(headers, ["equipslotcategory"])

        classjob_idx = find_all_indices(headers, "classjobcategory")

        crit_idx = find_all_indices(headers, "criticalhit")
        dh_idx = find_all_indices(headers, "directhit")
        det_idx = find_all_indices(headers, "determination")
        sps_idx = find_all_indices(headers, "spellspeed")

        log(f"name:{name_i} ilvl:{ilvl_i} slot:{slot_i}")
        log(f"stat idx -> crit:{len(crit_idx)} dh:{len(dh_idx)} det:{len(det_idx)} sps:{len(sps_idx)}")

        for i, row in enumerate(reader):

            # 🔥 progress so you KNOW it's moving
            if i % 5000 == 0 and i > 0:
                log(f"Parsing items... {i}")

            try:
                name = row[name_i]
                ilvl = safe_int(row[ilvl_i])
                slot = row[slot_i]
            except:
                continue

            if ilvl <= 0 or ilvl > 1000:
                continue

            # --- casting filter ---
            is_casting = False
            for idx in classjob_idx:
                try:
                    val = row[idx]
                    if val and ("Black Mage" in val or "Thaumaturge" in val or "Caster" in val):
                        is_casting = True
                        break
                except:
                    continue

            if not is_casting:
                continue

            # --- weapon filter ---
            if slot == "1":
                if not is_blm_weapon(name):
                    continue

            # --- stats (FAST) ---
            crit = sum(safe_int(row[i]) for i in crit_idx if i < len(row))
            dh = sum(safe_int(row[i]) for i in dh_idx if i < len(row))
            det = sum(safe_int(row[i]) for i in det_idx if i < len(row))
            sps = sum(safe_int(row[i]) for i in sps_idx if i < len(row))

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
