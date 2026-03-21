def generate_melded_stats(item, build_type="Crit"):
    melds = {}
    if not item.get('materia_slots'):
        return melds
    # simple logic: prioritize build_type stat
    stat_priority = [build_type.lower(), "det", "dh" if build_type=="Crit" else "crit"]
    for i, slot in enumerate(item['materia_slots']):
        stat = stat_priority[i % len(stat_priority)]
        melds[stat] = slot
    return melds
