import itertools
import time


# =========================
# MATERIA LOADING
# =========================

def load_materia(csv_data, logger):
    materia = []

    for row in csv_data:
        try:
            base_param = int(row.get("BaseParam", -1))

            # Find first non-zero value
            value = 0
            for i in range(16):
                v = int(row.get(f"Value[{i}]", 0))
                if v > 0:
                    value = v
                    break

            if base_param >= 0 and value > 0:
                materia.append({
                    "param": base_param,
                    "value": value
                })

        except Exception:
            continue

    logger(f"Materia parsed ({len(materia)})")
    return materia


# =========================
# APPLY MATERIA
# =========================

def apply_materia_to_item(item, materia_list):
    """
    Apply best materia to item based on available slots
    """

    slots = int(item.get("MateriaSlotCount", 0))
    overmeld = item.get("IsAdvancedMeldingPermitted", "False") == "True"

    max_slots = slots + (2 if overmeld else 0)

    applied = []
    stats = item["stats"].copy()

    # Sort materia by value (best first)
    materia_sorted = sorted(materia_list, key=lambda x: x["value"], reverse=True)

    for mat in materia_sorted[:max_slots]:
        param = mat["param"]
        val = mat["value"]

        stats[param] = stats.get(param, 0) + val
        applied.append(mat)

    return stats, applied


# =========================
# BUILD EVALUATION
# =========================

def evaluate_build(build, materia, logger):
    total_stats = {}

    applied_materia = {}

    for slot, item in build.items():
        stats, mats = apply_materia_to_item(item, materia)

        applied_materia[slot] = mats

        for k, v in stats.items():
            total_stats[k] = total_stats.get(k, 0) + v

    # --- SIMPLE DPS MODEL (you can refine later)
    main_stat = total_stats.get(0, 0)
    crit = total_stats.get(1, 0)
    dh = total_stats.get(2, 0)
    det = total_stats.get(3, 0)
    speed = total_stats.get(4, 0)

    dps = (
        main_stat * 1.0 +
        crit * 0.5 +
        dh * 0.4 +
        det * 0.3 +
        speed * 0.2
    )

    gcd = max(2.0, 2.5 - (speed / 10000))

    score = dps - (abs(gcd - 2.2) * 100)

    return {
        "dps": dps,
        "gcd": gcd,
        "score": score,
        "materia": applied_materia
    }


# =========================
# SOLVER
# =========================

def run_solver(items_by_slot, materia_csv, config, logger):
    logger("=== SOLVER START ===")

    start = time.time()

    materia = load_materia(materia_csv, logger)

    slots = list(items_by_slot.keys())

    if "weapon" not in slots:
        logger("[ERROR] Missing slot: weapon")
        return []

    all_combos = list(itertools.product(*items_by_slot.values()))

    logger(f"[SOLVER] TOTAL COMBINATIONS: {len(all_combos):,}")

    results = []

    for idx, combo in enumerate(all_combos):
        build = dict(zip(slots, combo))

        result = evaluate_build(build, materia, logger)

        results.append({
            "build": build,
            "result": result
        })

        # Progress logging every 100
        if idx % 100 == 0:
            logger(f"[SOLVER] Progress: {idx}/{len(all_combos)}")

    results.sort(key=lambda x: x["result"]["score"], reverse=True)

    logger(f"=== SOLVER COMPLETE ({time.time() - start:.2f}s) ===")

    return results[:10]
