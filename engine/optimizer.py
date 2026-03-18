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

    try:
        slot = int(slot)
        return {
            1: "weapon", 2: "weapon",
            3: "head", 4: "body",
            5: "hands", 6: "hands",
            7: "legs", 8: "feet",
            9: "earrings", 10: "necklace",
            11: "bracelet", 12: "ring"
        }.get(slot)
    except:
        return None


def group_slots(items):

    slots = {k: [] for k in VALID_SLOTS}

    for item in items:
        s = normalize_slot(item["slot"])
        if s:
            slots[s].append(item)

    # 🔥 DEBUG OUTPUT
    for s in VALID_SLOTS:
        log(f"{s}: {len(slots[s])} items")

    return slots


def trim_slots(slots):
    for s in slots:
        slots[s].sort(
            key=lambda x: x["crit"] + x["dh"] + x["det"] + x["sps"],
            reverse=True
        )
        slots[s] = slots[s][:MAX_PER_SLOT]


def solve(items, gcd_target):

    log("Starting solver")

    slots = group_slots(items)
    trim_slots(slots)

    order = [
        "weapon","head","body","hands","legs",
        "feet","earrings","necklace","bracelet","ring","ring"
    ]

    # 🔥 CHECK FOR MISSING SLOTS
    for s in order:
        if not slots[s]:
            log(f"❌ MISSING SLOT: {s}")
            return []

    slot_items = [slots[s] for s in order]

    best_sets = []

    def dfs(i, stats, build):

        if i == len(slot_items):

            score = calculate_score(stats, gcd_target)
            best_sets.append((score, build.copy()))
            return

        for base in slot_items[i]:

            item = apply_materia(base.copy())

            new_stats = stats.copy()

            for s in ["crit","dh","det","sps"]:
                new_stats[s] = new_stats.get(s,0) + item.get(s,0)

            build.append(item)
            dfs(i+1, new_stats, build)
            build.pop()

    dfs(0, {}, [])

    best_sets.sort(reverse=True, key=lambda x: x[0])

    return best_sets[:3]
