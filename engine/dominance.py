def dominates(a, b):

    better_or_equal = True
    strictly_better = False

    for stat in ["crit", "det", "dh", "sps", "int"]:

        av = a["stats"].get(stat, 0)
        bv = b["stats"].get(stat, 0)

        if av < bv:
            better_or_equal = False

        if av > bv:
            strictly_better = True

    return better_or_equal and strictly_better


def prune(items):

    result = []

    for item in items:

        dominated = False

        for other in items:

            if other == item:
                continue

            if dominates(other, item):

                dominated = True
                break

        if not dominated:
            result.append(item)

    return result
