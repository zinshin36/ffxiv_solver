MATERIA_VALUE = 36

def generate_melded_stats(item, build_type="Crit"):

    slots = item.get("materia_slots", 0)

    melds = {}

    if slots <= 0:
        return melds

    if build_type == "Crit":
        priority = ["crit", "det", "dh"]
    else:
        priority = ["sps", "crit", "det"]

    for i in range(slots):
        stat = priority[i % len(priority)]
        melds[stat] = melds.get(stat, 0) + MATERIA_VALUE

    return melds
