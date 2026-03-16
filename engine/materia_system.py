from engine.csv_loader import load_csv, to_int


def normalize(t):
    return t.lower().replace(" ", "").replace("_", "")


def detect_column(header, keywords):

    header_norm = [normalize(h) for h in header]

    for i, col in enumerate(header_norm):

        for k in keywords:

            if k in col:
                return i

    return None


def load_materia():

    rows = load_csv("Materia.csv")

    header = rows[1]

    name_col = detect_column(header, ["name", "singular"])

    stat_col = detect_column(header, ["baseparam"])

    val_col = detect_column(header, ["value"])

    materia = []

    for r in rows[3:]:

        name = r[name_col] if name_col < len(r) else ""

        if not name:
            continue

        materia.append({
            "name": name,
            "stat": r[stat_col],
            "value": to_int(r[val_col])
        })

    return materia
