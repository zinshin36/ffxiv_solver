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


items = []
max_ilvl = 0
foods = []


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


def is_blm_item(item):

    # Try multiple possible fields depending on CSV
    fields = [
        str(item.get("job", "")),
        str(item.get("classjob", "")),
        str(item.get("ClassJobCategory", "")),
        str(item.get("ClassJob", ""))
    ]

    combined = " ".join(fields).lower()

    return "black" in combined or "blm" in combined


def load_game_data():

    global items, max_ilvl

    log("Loading game data...")

    items, max_ilvl = load_all_items()

    max_ilvl_var.set(str(max_ilvl))

    load_foods()

    log(f"Game data loaded. Highest ilvl: {max_ilvl}")


def update_progress(v):

    progress_var.set(v)
    root.update_idletasks()


def detect_best_food(build, gcd):

    if not build:
        return

    stats = {}

    for item in build:
        for s in ["crit", "dh", "det", "sps"]:
            stats[s] = stats.get(s, 0) + item.get(s, 0)

    scores = []

    for food in foods:

        fs = apply_food(stats, food)
        score = calculate_score(fs, gcd)

        scores.append((score, food["name"]))

    scores.sort(reverse=True)

    log("")
    log("Top foods:")

    for score, name in scores[:5]:
        log(f"{name}  score {round(score,2)}")

    log("")


def run_solver():

    if not items:
        log("No game data loaded")
        return

    min_ilvl = int(min_ilvl_entry.get())
    gcd = float(gcd_entry.get())

    blacklist = load_blacklist()

    log(f"Min ilvl {min_ilvl}")
    log(f"GCD target {gcd}")

    filtered = [
        i for i in items
        if i["ilvl"] >= min_ilvl
        and not is_blacklisted(i["name"], blacklist)
        and is_blm_item(i)
    ]

    log(f"Items after ilvl filter ({len(filtered)})")

    best_build, score = solve(filtered, gcd, update_progress)

    if not best_build:
        log("No build found")
        return

    log("")
    log(f"Best score {round(score,2)}")
    log("")

    for item in best_build:
        log(item["name"])

    detect_best_food(best_build, gcd)


def solver_thread():
    threading.Thread(target=run_solver).start()


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
gcd_entry.insert(0, "2.40")
gcd_entry.grid(row=0, column=1)

progress_var = tk.IntVar()

ttk.Progressbar(
    root,
    orient="horizontal",
    length=450,
    variable=progress_var,
    maximum=100
).pack(pady=10)

log_box = tk.Text(root, height=20, width=110)
log_box.pack()

init_logger(log_box)

log("Application started")

root.mainloop()
