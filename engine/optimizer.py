from engine.logger import log
from engine.dps import calculate_score
from engine.materia import apply_materia

MAX_PER_SLOT = 6
VALID_SLOTS = [
    "weapon", "head", "body", "hands",
    "legs", "feet", "earrings",
    "necklace", "bracelet", "ring"
]

def normalize_slot(slot):
    if slot is None:
        return None
    try:
        slot_id = int(slot)
        SLOT_MAP = {
            1: "weapon", 2: "weapon", 3: "head", 4: "body",
            5: "hands", 6: "hands", 7: "legs", 8: "feet",
            9: "earrings", 10: "necklace", 11: "bracelet", 12: "ring",
            13: "head"
        }
        return SLOT_MAP.get(slot_id)
    except:
        s = str(slot).lower()
        for key, val in [("weapon","weapon"),("head","head"),("body","body"),
                         ("hand","hands"),("leg","legs"),("foot","feet"),
                         ("ear","earrings"),("neck","necklace"),
                         ("brace","bracelet"),("ring","ring")]:
            if key in s:
                return val
    return None


def group_slots(items):
    slots = {k: [] for k in VALID_SLOTS}
    for item in items:
        slot = normalize_slot(item.get("slot"))
        if slot:
            slots[slot].append(item)
    for s in VALID_SLOTS:
        log(f"{s}: {len(slots[s])} items")
    return slots


def trim_slots(slots):
    """Keep top N per slot by sum of stats to prevent explosion"""
    for slot in slots:
        slots[slot].sort(key=lambda x: sum(x.get(s,0) for s in ["crit","dh","det","sps"]), reverse=True)
        slots[slot] = slots[slot][:MAX_PER_SLOT]


def solve(items, gcd_target, top_n=3):
    """
    Returns top_n builds [(score, build_list), ...]
    Each build has materia applied
    """
    log("Starting solver")
    slots = group_slots(items)
    trim_slots(slots)

    slot_order = [
        "weapon", "head", "body", "hands",
        "legs", "feet", "earrings",
        "necklace", "bracelet", "ring", "ring"
    ]
    slot_items = []
    for s in slot_order:
        if not slots[s]:
            log(f"Missing slot: {s}")
            return []
        slot_items.append(slots[s])

    total_combinations = 1
    for s in slot_items:
        total_combinations *= len(s)
    log(f"Total combinations: {total_combinations}")

    top_builds = []
    checked = 0

    def dfs(i, stats, build):
        nonlocal top_builds, checked
        if i == len(slot_items):
            checked += 1
            score = calculate_score(stats, gcd_target)
            build_copy = [apply_materia(item.copy()) for item in build]
            top_builds.append((score, build_copy))
            top_builds.sort(key=lambda x: x[0], reverse=True)
            if len(top_builds) > top_n:
                top_builds = top_builds[:top_n]
            if checked % 1000 == 0:
                percent = int((checked / total_combinations) * 100)
                log(f"Progress {checked}/{total_combinations} ({percent}%)")
            return

        for base_item in slot_items[i]:
            new_stats = stats.copy()
            item_copy = base_item.copy()
            for s in ["crit","dh","det","sps"]:
                new_stats[s] = new_stats.get(s,0) + item_copy.get(s,0)
            build.append(item_copy)
            dfs(i+1, new_stats, build)
            build.pop()

    dfs(0, {}, [])
    log(f"Finished. Checked {checked} combinations")
    return top_builds
