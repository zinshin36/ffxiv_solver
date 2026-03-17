foods = [
    {"name":"Archon Burger","crit":90,"dh":60},
    {"name":"Tacos de Carne Asada","crit":80,"sps":70},
    {"name":"Stuffed Peppers","dh":90,"det":60},
    {"name":"Pumpkin Ratatouille","sps":100},
    {"name":"Scallop Salad","crit":60,"det":90},
]


def apply_food(stats, food):

    result = stats.copy()

    for k,v in food.items():
        if k == "name":
            continue

        result[k] = result.get(k,0) + v

    return result
