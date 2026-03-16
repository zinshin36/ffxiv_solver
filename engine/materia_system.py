from engine.csv_loader import load_csv, to_int


def load_materia():

    rows = load_csv("Materia.csv")

    header = rows[1]

    name_col = header.index("Name")

    stat_col = None
    val_col = None

    for i, h in enumerate(header):

        if "BaseParam" in h:
            stat_col = i

        if "Value" in h:
            val_col = i

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


def optimize_materia(item, materia):

    stats = dict(item["stats"])

    melds = []

    for _ in range(item["materia_slots"]):

        best = None
        best_gain = 0

        for m in materia:

            val = m["value"]

            if val > best_gain:
                best = m
                best_gain = val

        if best:

            stats[best["stat"]] = stats.get(best["stat"], 0) + best["value"]

            melds.append(best)

    return stats, melds
