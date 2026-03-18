import tkinter as tk
from tkinter import ttk
import threading
import json
import os

from engine.logger import log, init_logger
from engine.data_parser import load_all_items
from engine.optimizer import solve
from engine.blacklist import load_blacklist, is_blacklisted


items = []
max_ilvl = 0
foods = []


def load_foods():
    """Load foods from foods.json or create default."""
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


def is_blm_item(item):
    """Check if item is caster/BLM compatible."""
    possible_fields = ["job", "classjob", "ClassJob", "ClassJobCategory", "EquipRestriction"]
    combined = ""
    for f in possible_fields:
        if f in item:
            combined += str(item.get(f, "")) + " "
    combined = combined.lower()

    if any(x in combined for x in ["black", "blm", "thaum", "caster", "mage"]):
        return True

    # fallback: allow if no job info exists
    return combined.strip() == ""


def load_game_data():
    """Load all items and foods."""
    global items, max_ilvl
    log("Loading game data...")

    # Load items
    all_items = load_all_items(os.path.join("game_data", "Item.csv"))
    # Filter caster items
    items = [i for i in all_items if is_blm_item(i)]
    max_ilvl = max([i.get("ilvl", 0) for i in items]) if items else 0

    max_ilvl_var.set(str(max_ilvl))
    load_foods()

    log(f"Game data loaded. Highest ilvl: {max_ilvl}")
    log(f"Caster items loaded: {len(items)}")


def update_progress(v):
    progress_var.set(v)
    root.update_idletasks()


def run_solver():
    """Run solver with user-selected GCD and min ilvl, display top 3 builds."""
    if not items:
        log("No game data loaded")
        return

    min_ilvl_val = int(min_ilvl_entry.get())
    gcd_val = float(gcd_entry.get())

    blacklist = load_blacklist()

    log(f"Min ilvl: {min_ilvl_val}")
    log(f"GCD target: {gcd_val}")

    # Filter by ilvl and blacklist
    filtered_items = [
        i for i in items
        if i.get("ilvl", 0) >= min_ilvl_val
        and not is_blacklisted(i.get("name", ""), blacklist)
    ]

    log(f"Items after filter: {len(filtered_items)}")
    if not filtered_items:
        log("No items found after filter!")
        return

    # Solve for top 3 builds
    best_builds = solve(filtered_items, gcd_val, progress=update_progress, top_n=3, foods=foods)

    if not best_builds:
        log("No builds found")
        return

    log("\n=== TOP 3 BUILDS ===")
    for i, b in enumerate(best_builds):
        log(f"\n--- Build #{i+1} | Score {round(b['score'],2)} | Food: {b['food']} ---")
        for item in b["build"]:
            mat = ", ".join([f"{m['stat']}+{m['value']}" for m in item["materia_applied"]])
            log(f"{item['name']} | Materia: {mat}")


def solver_thread():
    threading.Thread(target=run_solver).start()


# ----------------------
# GUI SETUP
# ----------------------
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

log_box = tk.Text(root, height=25, width=120)
log_box.pack()

init_logger(log_box)
log("Application started")

root.mainloop()
