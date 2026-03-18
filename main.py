import tkinter as tk
from tkinter import ttk
import threading
import json
import os

from engine.logger import log, init_logger
from engine.data_parser import load_all_items
from engine.optimizer import solve
from engine.blacklist import load_blacklist, is_blacklisted
from engine.dps import calculate_score
from engine.materia import apply_materia


items = []
max_ilvl = 0
foods = []


# -----------------------------
# FOOD HANDLING
# -----------------------------
def load_foods():
    global foods
    if not os.path.exists("foods.json"):
        default_foods = [
            {"name": "Archon Burger", "crit": 90, "dh": 60},
            {"name": "Tacos de Carne Asada", "crit": 80, "sps": 70},
            {"name": "Stuffed Peppers", "dh": 90, "det": 60},
            {"name": "Pumpkin Ratatouille", "sps": 100},
            {"name": "Scallop Salad", "crit": 60, "det": 90}
        ]
        with open("foods.json", "w") as f:
            json.dump(default_foods, f, indent=4)
        foods = default_foods
        log("foods.json created")
        return

    with open("foods.json", "r") as f:
        foods = json.load(f)

    log(f"{len(foods)} foods loaded")


def apply_food(stats, food):
    result = stats.copy()
    for k, v in food.items():
        if k == "name":
            continue
        result[k] = result.get(k, 0) + v
    return result


# -----------------------------
# ITEM FILTERING
# -----------------------------
def is_blm_item(item):
    """Soft match: only caster/black mage gear"""
    possible_fields = ["job", "classjob", "ClassJob", "ClassJobCategory", "EquipRestriction"]
    combined = ""
    for f in possible_fields:
        if f in item:
            combined += str(item.get(f, "")) + " "
    combined = combined.lower()
    return any(x in combined for x in ["black", "blm", "thaum", "caster", "mage"])


def load_game_data():
    global items, max_ilvl
    log("Loading game data...")
    all_items, max_ilvl = load_all_items()

    # Filter for Black Mage / caster items
    items = [i for i in all_items if is_blm_item(i)]

    load_foods()
    max_ilvl_var.set(str(max_ilvl))
    log(f"Caster items loaded: {len(items)}")
    log(f"Game data loaded. Highest ilvl: {max_ilvl}")


# -----------------------------
# SOLVER
# -----------------------------
def run_solver():
    if not items:
        log("No game data loaded")
        return

    min_ilvl = int(min_ilvl_entry.get())
    gcd = float(gcd_entry.get())

    blacklist = load_blacklist()

    # Filter by ilvl + blacklist
    filtered = [
        i for i in items
        if i["ilvl"] >= min_ilvl and not is_blacklisted(i["name"], blacklist)
    ]
    log(f"Items after filter: {len(filtered)}")

    if not filtered:
        log("No items after filtering")
        return

    top_builds = solve(filtered, gcd, top_n=3)

    if not top_builds:
        log("No builds found")
        return

    log("\n--- TOP BUILDS ---")
    best_score = top_builds[0][0]

    for idx, (score, build) in enumerate(top_builds, start=1):
        log(f"\nBuild {idx} | DPS: {round(score, 2)} | Δ DPS: {round(best_score - score, 2)}")
        # Detect best food for this build
        stats_sum = {"crit":0,"dh":0,"det":0,"sps":0}
        for item in build:
            for s in stats_sum:
                stats_sum[s] += item.get(s,0)

        best_food = None
        best_food_score = -1
        for food in foods:
            fs = apply_food(stats_sum, food)
            s = calculate_score(fs, gcd)
            if s > best_food_score:
                best_food_score = s
                best_food = food

        log(f"  Food: {best_food['name']} | Score with food: {round(best_food_score,2)}")

        # Show items + materia
        for item in build:
            item_display = f"{item['name']} (ilvl {item['ilvl']})"
            if "materia_slots" in item and item["materia_slots"] > 0:
                item_display += f" | Materia slots: {item['materia_slots']}"
            log("   - " + item_display)


def solver_thread():
    threading.Thread(target=run_solver).start()


# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("FFXIV BLM Gear Solver")

controls = tk.Frame(root)
controls.pack(pady=10)

tk.Button(controls, text="Load Game Data", command=load_game_data).grid(row=0, column=0)
tk.Label(controls, text="Min ilvl").grid(row=0, column=1)
min_ilvl_entry = tk.Entry(controls, width=6)
min_ilvl_entry.insert(0, "780")
min_ilvl_entry.grid(row=0, column=2)
tk.Button(controls, text="Run Solver", command=solver_thread).grid(row=0, column=3)

tk.Label(controls, text="Max ilvl").grid(row=0, column=4)
max_ilvl_var = tk.StringVar(value="-")
tk.Label(controls, textvariable=max_ilvl_var, width=6).grid(row=0, column=5)

options = tk.Frame(root)
options.pack()
tk.Label(options, text="Target GCD").grid(row=0, column=0)
gcd_entry = tk.Entry(options, width=6)
gcd_entry.insert(0, "2.2")
gcd_entry.grid(row=0, column=1)

progress_var = tk.IntVar()
ttk.Progressbar(root, orient="horizontal", length=450, variable=progress_var, maximum=100).pack(pady=10)

log_box = tk.Text(root, height=25, width=110)
log_box.pack()

init_logger(log_box)
log("Application started")
root.mainloop()
