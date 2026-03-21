from engine.stats import apply_food_stats, compute_gcd, compute_dps
import itertools

def run_solver(items_by_slot, min_ilvl=0, target_gcd=2.5, build_type="Crit", selected_food=None, blacklist=None):
    """
    Run BIS solver with optional food stats
    items_by_slot: dict of slot -> list of items
    min_ilvl: minimum item level
    target_gcd: desired GCD
    build_type: "Crit" or "Spell Speed"
    selected_food: dict from food_system.get_food_stats()
    blacklist: set of blacklisted item names
    """
    if blacklist is None:
        blacklist = set()
    if selected_food is None:
        selected_food = {}

    # Prepare filtered items per slot
    filtered_items = {}
    for slot, items in items_by_slot.items():
        filtered_items[slot] = [i for i in items if i['ilvl'] >= min_ilvl and i['name'] not in blacklist]
        if not filtered_items[slot]:
            raise ValueError(f"No valid items in slot {slot} after filtering")

    # Generate all possible builds (cartesian product)
    all_slots = sorted(filtered_items.keys())
    all_combinations = itertools.product(*(filtered_items[slot] for slot in all_slots))

    results = []
    for combo in all_combinations:
        build_items = dict(zip(all_slots, combo))

        # Aggregate base stats
        base_stats = {"crit":0,"dh":0,"det":0,"sps":0}
        for item in build_items.values():
            for stat in ["crit","dh","det","sps"]:
                base_stats[stat] += item.get(stat,0)
            # Include melds if present
            if item.get("melds"):
                for stat, val in item["melds"].items():
                    base_stats[stat] = base_stats.get(stat,0) + val

        # Apply food stats
        total_stats = apply_food_stats(base_stats, selected_food)

        # Compute actual GCD
        gcd = compute_gcd(target_gcd, total_stats.get("det",0))

        # Compute DPS
        dps = compute_dps(total_stats, gcd, build_type)

        result = {
            "items": build_items,
            "crit": total_stats.get("crit",0),
            "dh": total_stats.get("dh",0),
            "det": total_stats.get("det",0),
            "sps": total_stats.get("sps",0),
            "gcd": gcd,
            "dps": dps
        }
        results.append(result)

    # Sort results by DPS descending
    results.sort(key=lambda x: x["dps"], reverse=True)
    return results[:10]  # top 10 builds
