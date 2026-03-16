from engine.csv_loader import load_csv, find_col, to_int


def load_materia():

    rows = load_csv("Materia.csv")

    header = rows[1]

    name_col = find_col(header, "Name")
    stat_col = find_col(header, "BaseParam")
    val_col = find_col(header, "Value")

    materia = []

    for r in rows[3:]:

        name = r[name_col]

        if not name:
            continue

        materia.append({
            "name": name,
            "stat": r[stat_col],
            "value": to_int(r[val_col])
        })

    return materia


def best_materia(item, materia):

    melds = []
    stats = dict(item["stats"])

    cap = item["ilvl"] * 2

    for _ in range(item["materia_slots"]):

        best = None
        best_gain = 0

        for m in materia:

            stat = m["stat"]
            val = m["value"]

            current = stats.get(stat, 0)

            if current + val > cap:
                continue

            if val > best_gain:

                best = m
                best_gain = val

        if not best:
            break

        stats[best["stat"]] = stats.get(best["stat"], 0) + best["value"]

        melds.append(best)

    return stats, melds
