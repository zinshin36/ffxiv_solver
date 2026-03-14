from engine.csv_loader import load_csv, i

MAX_OVERMELD = 5


def load_materia():

    rows = load_csv("Materia.csv")

    materia = []

    for r in rows[1:]:

        name = r[1]
        stat = r[10]
        value = i(r[11])

        if not name:
            continue

        materia.append({
            "name": name,
            "stat": stat,
            "value": value
        })

    return materia


def meld_item(item, materia):

    slots = item["materia_slots"]
    max_slots = max(slots, MAX_OVERMELD)

    stats = item["stats"].copy()

    melds = []

    sorted_materia = sorted(materia, key=lambda x: x["value"], reverse=True)

    for m in sorted_materia:

        if len(melds) >= max_slots:
            break

        stat = m["stat"]

        stats[stat] = stats.get(stat, 0) + m["value"]

        melds.append(m)

    return stats, melds
