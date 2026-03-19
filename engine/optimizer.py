# REPLACE ENTIRE FILE

import itertools
from engine.logger import log
from engine.materia_system import load_materia
from engine.blacklist import load_blacklist
from engine.tier_solver import calculate_gcd
from engine.dps_model import compute_dps


def run_solver(items, target_gcd=2.38, food=None):
    return solve(items, target_gcd, food)


def solve(items, target_gcd, food=None):

    log("=== SOLVER START ===")

    materia = load_materia()
    blacklist = load_blacklist()

    items = [i for i in items if not any(b in i["name"].lower() for b in blacklist)]

    gear = {}

    for item in items:
        gear.setdefault(item["slot"], []).append(item)

    required_slots = [
        "weapon", "head", "body", "hands",
        "legs", "feet", "earrings",
        "necklace", "bracelet", "ring"
    ]

    for s in required_slots:
        if s not in gear or not gear[s]:
            log(f"[ERROR] Missing slot: {s}")
            return []

    combos = itertools.product(
        gear["weapon"], gear["head"], gear["body"], gear["hands"],
        gear["legs"], gear["feet"], gear["earrings"],
        gear["necklace"], gear["bracelet"],
        gear["ring"], gear["ring"]
    )

    best = []

    for combo in combos:

        # 🚨 prevent duplicate rings
        if combo[-1]["name"] == combo[-2]["name"]:
            continue

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

        score = dps - abs(gcd - target_gcd) * 1500

        best.append({
            "score": score,
            "stats": total_stats,
            "build": combo,
            "gcd": gcd,
            "dps": dps
        })

    best.sort(key=lambda x: x["score"], reverse=True)

    log("=== SOLVER COMPLETE ===")

    return best[:10]
