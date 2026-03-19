import itertools
from engine.logger import log
from engine.materia_system import load_materia
from engine.blacklist import load_blacklist
from engine.tier_solver import calculate_gcd
from engine.dps_model import compute_dps


def solve(items, target_gcd, food=None):

    log("=== SOLVER START ===")

    materia = load_materia()
    log(f"[SOLVER] Materia count: {len(materia)}")

    blacklist = load_blacklist()
    log(f"[SOLVER] Blacklist loaded: {len(blacklist)}")

    items = [i for i in items if not any(b in i["name"].lower() for b in blacklist)]
    log(f"[SOLVER] Items after blacklist: {len(items)}")

    # =========================
    # GROUP BY SLOT
    # =========================
    gear = {
        "weapon": [],
        "head": [],
        "body": [],
        "hands": [],
        "legs": [],
        "feet": [],
        "earrings": [],
        "necklace": [],
        "bracelet": [],
        "ring": [],
        "unknown": []
    }

    for item in items:
        slot = item.get("slot", "unknown")
        if slot not in gear:
            slot = "unknown"
        gear[slot].append(item)

    for s in gear:
        log(f"[GEAR] {s}: {len(gear[s])}")

    if gear["unknown"]:
        log(f"[WARNING] Unknown slot items: {len(gear['unknown'])}")

    # =========================
    # TOTAL COMBINATIONS
    # =========================
    total = (
        max(1, len(gear["weapon"])) *
        max(1, len(gear["head"])) *
        max(1, len(gear["body"])) *
        max(1, len(gear["hands"])) *
        max(1, len(gear["legs"])) *
        max(1, len(gear["feet"])) *
        max(1, len(gear["earrings"])) *
        max(1, len(gear["necklace"])) *
        max(1, len(gear["bracelet"])) *
        max(1, len(gear["ring"])) *
        max(1, len(gear["ring"]))
    )

    log(f"[SOLVER] TOTAL COMBINATIONS: {total}")

    # =========================
    # COMBO LOOP (WITH PROGRESS)
    # =========================
    combos = itertools.product(
        gear["weapon"], gear["head"], gear["body"], gear["hands"],
        gear["legs"], gear["feet"], gear["earrings"],
        gear["necklace"], gear["bracelet"],
        gear["ring"], gear["ring"]
    )

    best = []
    checked = 0

    for combo in combos:
        checked += 1

        if checked % 1000 == 0:
            pct = (checked / total) * 100
            log(f"[PROGRESS] {pct:.6f}% ({checked}/{total})")

        total_stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

        for item in combo:
            for k in total_stats:
                total_stats[k] += item["stats"].get(k, 0)

        if food:
            for k in food:
                if k != "name":
                    total_stats[k] += food[k]

        gcd = calculate_gcd(total_stats["sps"])
        dps = compute_dps(total_stats)

        score = dps - abs(gcd - target_gcd) * 2000

        best.append((score, combo, total_stats))

    best.sort(key=lambda x: x[0], reverse=True)

    log("=== SOLVER COMPLETE ===")

    return best[:3]
