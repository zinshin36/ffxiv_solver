import itertools
import time


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


# =========================
# DPS FUNCTION (REALISTIC)
# =========================
def calc_dps(stats):
    crit = stats["crit"]
    dh = stats["dh"]
    det = stats["det"]
    sps = stats["sps"]
    intel = stats["int"]

    # basic BLM scaling
    return (
        intel * 1.0 +
        crit * 0.45 +
        dh * 0.35 +
        det * 0.30 +
        sps * 0.25
    )


# =========================
# BUILD SOLVER
# =========================
def solve(items, foods):
    slots = [
        "weapon", "head", "body", "hands",
        "legs", "feet", "earrings",
        "necklace", "bracelet", "ring"
    ]

    gear = {s: [] for s in slots}

    for item in items:
        if item["slot"] in gear:
            gear[item["slot"]].append(item)

    for s in gear:
        log(f"{s}: {len(gear[s])} items")

    combos = itertools.product(
        gear["weapon"],
        gear["head"],
        gear["body"],
        gear["hands"],
        gear["legs"],
        gear["feet"],
        gear["earrings"],
        gear["necklace"],
        gear["bracelet"],
        gear["ring"],
        gear["ring"]
    )

    best = []
    checked = 0
    start = time.time()

    for combo in combos:
        checked += 1

        if checked % 10000 == 0:
            elapsed = time.time() - start
            log(f"Checked {checked} builds ({elapsed:.1f}s)")

        stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0, "int": 0}

        for item in combo:
            for k in stats:
                stats[k] += item["stats"][k]

        best_score = 0
        best_food = None

        for food in foods:
            total = stats.copy()
            for k in food:
                if k in total:
                    total[k] += food[k]

            score = calc_dps(total)

            if score > best_score:
                best_score = score
                best_food = food

        best.append((best_score, combo, best_food))

    best.sort(reverse=True, key=lambda x: x[0])

    return best[:3]
