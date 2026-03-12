def dominates(a, b):

    if a["ilvl"] < b["ilvl"]:
        return False

    better = False

    for stat, val in a["stats"].items():

        if val < b["stats"].get(stat, 0):
            return False

        if val > b["stats"].get(stat, 0):
            better = True

    return better


def prune(items):

    result = []

    for a in items:

        dominated = False

        for b in items:

            if a == b:
                continue

            if dominates(b, a):
                dominated = True
                break

        if not dominated:
            result.append(a)

    return result
