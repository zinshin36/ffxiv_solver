from engine.csv_loader import load_csv, i

MAX_OVERMELD = 5


def load_materia():

    materia_rows = load_csv("Materia.csv")
    param_rows = load_csv("MateriaParam.csv")

    param_map = {}

    for r in param_rows[1:]:
        materia_id = r[1]
        stat = r[2]
        value = i(r[3])

        param_map[materia_id] = (stat, value)

    materia = []

    for r in materia_rows[1:]:

        key = r[0]
        name = r[1]

        if key not in param_map:
            continue

        stat, value = param_map[key]

        materia.append({
            "name": name,
            "stat": stat,
            "value": value
        })

    return materia


def apply_cap(item, stats):

    cap = item.get("stat_cap", {})

    for stat in cap:

        if stat in stats:
            stats[stat] = min(stats[stat], cap[stat])

    return stats


def meld_item(item, materia):

    slots = item["materia_slots"]
    max_slots = max(slots, MAX_OVERMELD)

    stats = item["stats"].copy()
    melds = []

    materia_sorted = sorted(materia, key=lambda x: x["value"], reverse=True)

    for m in materia_sorted:

        if len(melds) >= max_slots:
            break

        stat = m["stat"]

        stats[stat] = stats.get(stat, 0) + m["value"]

        melds.append(m)

    stats = apply_cap(item, stats)

    return stats, melds
