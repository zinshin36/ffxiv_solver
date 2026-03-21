import itertools
from engine.melds import generate_melded_stats
from engine.stats import calculate_build_stats, cap_stats

SLOTS = [
    "weapon","head","body","hands","legs",
    "feet","earrings","necklace","bracelet","ring1","ring2"
]

def run_solver(items_by_slot, target_gcd=2.5, build_type="Crit", selected_food=None, foods=None):

    slot_items = [items_by_slot.get(slot, []) for slot in SLOTS]

    best = []

    for combo in itertools.product(*slot_items):

        build = {}

        for slot, item in zip(SLOTS, combo):
            new_item = item.copy()
            new_item["melds"] = generate_melded_stats(new_item, build_type)
            build[slot] = new_item

        stats = calculate_build_stats(build, selected_food, foods)
        stats = cap_stats(stats)

        gcd_diff = abs(stats["gcd"] - target_gcd)

        score = stats["dps"] - (gcd_diff * 5000)

        best.append({
            "items": build,
            "dps": stats["dps"],
            "gcd": stats["gcd"],
            "score": score,
            "crit": stats["crit"],
            "dh": stats["dh"],
            "det": stats["det"],
            "sps": stats["sps"]
        })

    best.sort(key=lambda x: x["score"], reverse=True)

    return best[:5]
