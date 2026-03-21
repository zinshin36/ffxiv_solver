# engine/optimizer.py

from itertools import product
from engine.stats import calc_stats, calc_gcd, calc_dps
from engine.food_system import apply_food

def run_solver(items_by_slot, min_ilvl=0, target_gcd=2.5, build_type="Crit", selected_food=None, blacklist=None):
    """
    Run the BIS optimizer.
    items_by_slot: dict mapping slots -> list of item dicts
    selected_food: dict with food stats
    blacklist: set of item names to exclude
    """

    if blacklist is None:
        blacklist = set()

    # Filter items based on blacklist & min ilvl
    filtered_items = {}
    for slot, items in items_by_slot.items():
        filtered_items[slot] = [
            i for i in items if i['name'] not in blacklist and i['ilvl'] >= min_ilvl
        ]

    # Prepare slot order for combinations
    slots = list(filtered_items.keys())
    all_combinations = product(*(filtered_items[slot] for slot in slots))

    results = []

    base_stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0}  # Can add more base stats if needed

    for combo in all_combinations:
        gear_stats = {}
        combo_dict = {}
        for idx, slot in enumerate(slots):
            item = combo[idx]
            combo_dict[slot] = item
            for stat in ["crit", "dh", "det", "sps"]:
                gear_stats[stat] = gear_stats.get(stat, 0) + item.get(stat, 0)

        # Apply food
        food_stats = {}
        if selected_food:
            for stat in ["crit", "dh", "det", "sps"]:
                if stat in selected_food:
                    food_stats[stat] = selected_food[stat]

        final_stats = calc_stats(base_stats, gear_stats, food_stats)
        gcd = calc_gcd(final_stats["det"], target_gcd)
        dps = calc_dps(final_stats, gcd=gcd, build_type=build_type)

        results.append({
            "dps": dps,
            "gcd": gcd,
            "crit": final_stats["crit"],
            "dh": final_stats["dh"],
            "det": final_stats["det"],
            "sps": final_stats["sps"],
            "items": combo_dict
        })

    # Sort by DPS descending
    results.sort(key=lambda x: x["dps"], reverse=True)
    return results[:5]  # Top 5 builds
