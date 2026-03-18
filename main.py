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


# -------------------------
# FOOD SYSTEM
# -------------------------

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


# -------------------------
# LOAD GAME DATA
# -------------------------

def load_game_data():

    global items, max_ilvl

    try:
        log("Loading game data...")

        items, max_ilvl = load_all_items()

        max_ilvl_var.set(str(max_ilvl))

        load_foods()

        log(f"Game data loaded. Highest ilvl: {max_ilvl}")

    except Exception as e:
        log(f"ERROR loading data: {e}")


# -------------------------
# SOLVER
# -------------------------

def run_solver():

    if not items:
        log("No game data loaded")
        return

    try:
        min_ilvl = int(min_ilvl_entry.get())
        gcd = float(gcd_entry.get())

        blacklist = load_blacklist()

        log(f"Min ilvl {min_ilvl}")
        log(f"GCD target {gcd}")

        filtered = [
            i for i in items
            if i["ilvl"] >= min_ilvl
            and not is_blacklisted(i["name"], blacklist)
        ]

        log(f"Items after filter: {len(filtered)}")

        results = solve(filtered, gcd)

        if not results:
            log("No builds found")
            return

        log("")
        log("===== TOP BUILDS =====")

        final_scores = []

        for idx, (score, build) in enumerate(results):

            log("")
            log(f"--- Build #{idx+1} ---")
            log(f"Base Score: {round(score, 2)}")

            stats = {"crit": 0, "dh": 0, "det": 0, "sps": 0}

            for item in build:

                log(item["name"])

                # Show materia
                for m in item.get("melds", []):
                    log(f"   -> {m}")

                # Accumulate stats
                for s in stats:
                    stats[s] += item.get(s, 0)

            # -------------------------
            # FOOD OPTIMIZATION
            # -------------------------

            best_food = None
            best_food_score = 0

            for food in foods:

                fs = stats.copy()

                for k, v in food.items():
                    if k != "name":
                        fs[k] = fs.get(k, 0) + v

                s = calculate_score(fs, gcd)

                if s > best_food_score:
                    best_food_score = s
                    best_food = food["name"]

            final_scores.append(best_food_score)

            log(f"Best Food: {best_food}")
            log(f"Final Score w/ Food: {round(best_food_score, 2)}")

        # -------------------------
        # SCORE DIFFERENCES
        # -------------------------

        log("")
        log("===== DIFFERENCES =====")

        if len(final_scores) >= 2:
            diff = final_scores[0] - final_scores[1]
            log(f"#1 vs #2: {round(diff, 2)}")

        if len(final_scores) >= 3:
            diff = final_scores[1] - final_scores[2]
            log(f"#2 vs #3: {round(diff, 2)}")

    except Exception as e:
        log(f"Solver error: {e}")


def solver_thread():
    threading.Thread(target=run_solver, daemon=True).start()


# -------------------------
# UI SETUP
# -------------------------

root = tk.Tk()
root.title("FFXIV Gear Solver")

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
