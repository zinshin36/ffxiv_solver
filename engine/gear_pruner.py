def dominates(a, b):

    better_or_equal = (
        a["ilvl"] >= b["ilvl"]
        and a.get("crit", 0) >= b.get("crit", 0)
        and a.get("dh", 0) >= b.get("dh", 0)
        and a.get("det", 0) >= b.get("det", 0)
        and a.get("sps", 0) >= b.get("sps", 0)
    )

    strictly_better = (
        a["ilvl"] > b["ilvl"]
        or a.get("crit", 0) > b.get("crit", 0)
        or a.get("dh", 0) > b.get("dh", 0)
        or a.get("det", 0) > b.get("det", 0)
        or a.get("sps", 0) > b.get("sps", 0)
    )

    return better_or_equal and strictly_better


def prune_slot(items):

    pruned = []

    for item in items:

        dominated = False

        for other in items:

            if other is item:
                continue

            if dominates(other, item):
                dominated = True
                break

        if not dominated:
            pruned.append(item)

    return pruned
