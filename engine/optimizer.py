import itertools
from engine.stats import calculate_build_stats, cap_stats
from engine.melds import generate_melded_stats

def run_solver(items_by_slot, min_ilvl=0, target_gcd=None, build_type="Crit", selected_food=None, blacklist=None):
    all_slots = ["weapon","head","body","hands","legs","feet","earrings","necklace","bracelet","ring1","ring2"]
    slot_items = [items_by_slot[slot] for slot in all_slots]

    best_builds = []
    total_combinations = 1
    for items in slot_items:
        total_combinations *= len(items)

    if total_combinations > 10**7:  # cap for performance
        slot_items = [items[:10] for items in slot_items]

    for combo in itertools.product(*slot_items):
        build = {slot: item.copy() for slot, item in zip(all_slots, combo)}

        # generate melds per item
        for slot_name, item in build.items():
            item['melds'] = generate_melded_stats(item, build_type)

        stats = calculate_build_stats(build, selected_food)
        stats = cap_stats(stats)

        build_entry = {
            'items': build,
            'dps': stats['dps'],
            'gcd': stats['gcd'],
            'crit': stats['crit'],
            'dh': stats['dh'],
            'det': stats['det'],
            'sps': stats['sps']
        }

        best_builds.append(build_entry)

    best_builds.sort(key=lambda x: x['dps'], reverse=True)
    return best_builds[:3]
