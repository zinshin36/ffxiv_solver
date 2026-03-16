FOODS = {

    "None": {},

    "Raid Food":

    {
        "crit": (0.10, 120),
        "det": (0.10, 120)
    },

    "Spell Speed Food":

    {
        "sps": (0.10, 120),
        "crit": (0.05, 80)
    }
}


def apply_food(stats, food):

    buff = FOODS.get(food, {})

    result = dict(stats)

    for stat, (pct, cap) in buff.items():

        base = result.get(stat, 0)

        bonus = min(int(base * pct), cap)

        result[stat] = base + bonus

    return result
