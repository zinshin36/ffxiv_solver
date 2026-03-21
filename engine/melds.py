def generate_melded_stats(item, build_type="Crit"):
    melds = {}
    slots = item.get("materia_slots", 0)
    if slots <= 0:
        return melds

    stat_priority = []
    if build_type == "Crit":
        stat_priority = ["crit", "dh", "det", "sps"]
    else:
        stat_priority = ["sps", "crit", "det", "dh"]

    for i in range(slots):
        stat = stat_priority[i % len(stat_priority)]
        melds[stat] = melds.get(stat, 0) + 36  # standard materia value

    return melds
