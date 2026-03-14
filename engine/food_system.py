FOODS = {

    "None": {},

    "Crit Food": {
        "CriticalHit": 100,
        "Determination": 60
    },

    "SpS Food": {
        "SpellSpeed": 100,
        "CriticalHit": 60
    }

}


def apply_food(stats, food):

    if food not in FOODS:
        return stats

    s = stats.copy()

    for k, v in FOODS[food].items():
        s[k] = s.get(k, 0) + v

    return s
