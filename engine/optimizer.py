import itertools
import time

# -------------------------
# CONSTANTS
# -------------------------
LEVEL_MAIN = 390
LEVEL_SUB = 400
LEVEL_DIV = 1900

MATERIA_VALUE = 36

# -------------------------
# GCD
# -------------------------
def compute_gcd(sps):
    base = 2.5
    gcd = base * (1000 - (130 * (sps - LEVEL_SUB) / LEVEL_DIV)) / 1000
    return round(gcd, 3)

# -------------------------
# DAMAGE FORMULAS
# -------------------------
def crit_rate(crit):
    return (200 * (crit - LEVEL_SUB) / LEVEL_DIV + 50) / 1000

def crit_damage(crit):
    return (1400 + (200 * (crit - LEVEL_SUB) / LEVEL_DIV)) / 1000

def dh_rate(dh):
    return (550 * (dh - LEVEL_SUB) / LEVEL_DIV) / 1000

def det_multi(det):
    return (140 * (det - LEVEL_MAIN) / LEVEL_DIV + 1000) / 1000

def speed_multi(sps):
    return (1000 + (130 * (sps - LEVEL_SUB) / LEVEL_DIV)) / 1000

# -------------------------
# DPS (ILVL HEAVILY WEIGHTED)
# -------------------------
def compute_dps(stats, ilvl_total):

    crit = stats["crit"]
    dh = stats["dh"]
    det = stats["det"]
    sps = stats["sps"]
    intel = stats["int"]

    dmg = intel
    dmg *= det_multi(det)
    dmg *= speed_multi(sps)

    dmg *= (1 + crit_rate(crit) * (crit_damage(crit) - 1))
    dmg *= (1 + dh_rate(dh) * 0.25)

    # 🔥 THIS FIXES BASE vs AUGMENTED
    dmg *= (1 + ilvl_total * 0.002)

    return dmg

# -------------------------
# FOOD
# -------------------------
def apply_food(stats, food):
    if not food:
        return stats

    out = stats.copy()

    for stat, (pct, cap) in food.items():
        base = out.get(stat, 0)
        bonus = min(int(base * pct), cap)
        out[stat] += bonus

    return out

# -------------------------
# SAFE STAT CAP
# -------------------------
def apply_cap(base, current):
    # simple but effective cap model
    cap = int(base * 1.3)
    return min(current, cap)

# -------------------------
# VALID MATERIA
# -------------------------
def apply_materia(item):

    base = item["stats"]
    stats = base.copy()

    slots = item.get("materia_slots", 0)

    # ONLY crafted gets overmeld
    name = item["name"].lower()
    is_crafted = "augmented" not in name and "bygone" in name

    if is_crafted:
        slots += 2

    melds = []

    priority = ["crit", "det", "dh", "sps"]

    for _ in range(slots):

        applied = False

        for stat in priority:

            new_val = stats[stat] + MATERIA_VALUE

            # enforce cap
            capped = apply_cap(base[stat], new_val)

            if capped > stats[stat]:
                stats[stat] = capped
                melds.append(f"{stat}+{MATERIA_VALUE}")
                applied = True
                break

        if not applied:
            break

    return stats, melds

# -------------------------
# BUILD EVAL
# -------------------------
def evaluate_build(build, food, target_gcd):

    total = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}
    melds_out = {}
    ilvl_total = 0

    for slot, item in build.items():

        if not item:
            return None

        stats, melds = apply_materia(item)

        melds_out[slot] = melds

        for k in total:
            total[k] += stats.get(k, 0)

        ilvl_total += item["ilvl"]

    total = apply_food(total, food)

    gcd = compute_gcd(total["sps"])
    dps = compute_dps(total, ilvl_total)

    if target_gcd:
        dps -= abs(gcd - target_gcd) * 500

    return {
        "stats": total,
        "gcd": gcd,
        "dps": dps,
        "melds": melds_out
    }

# -------------------------
# SOLVER
# -------------------------
def run_solver(items_by_slot, food, target_gcd, logger):

    logger("=== SOLVER START ===")

    start = time.time()

    clean = {}
    for slot, items in items_by_slot.items():
        valid = [i for i in items if i]
        if not valid:
            return []
        clean[slot] = valid

    slots = list(clean.keys())
    combos = itertools.product(*clean.values())

    results = []

    for combo in combos:

        build = dict(zip(slots, combo))

        result = evaluate_build(build, food, target_gcd)

        if result:
            results.append({
                "build": build,
                "result": result
            })

    results.sort(key=lambda x: x["result"]["dps"], reverse=True)

    logger(f"=== DONE ({time.time() - start:.2f}s) ===")

    return results[:3]
