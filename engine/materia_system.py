from engine.csv_loader import load_csv, to_int


def load_materia():

    rows = load_csv("Materia.csv")

    header = rows[1]

    name_col = header.index("Name")
    stat_col = header.index("BaseParam")
    val_col = header.index("Value")

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


def apply_materia(item, materia_list):

    stats = dict(item["stats"])

    melds = []

    for m in materia_list[:item["materia_slots"]]:

        stat = m["stat"]

        val = m["value"]

        cap = item["stats"].get(stat, 0) + 200

        new_val = stats.get(stat, 0) + val

        if new_val > cap:
            continue

        stats[stat] = new_val
        melds.append(m)

    return stats, melds
