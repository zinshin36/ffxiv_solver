import tkinter as tk
from tkinter import ttk
import threading

from engine.logger import log, init_logger
from engine.data_parser import load_all_items, filter_items
from engine.optimizer import solve


items = []
max_ilvl = 0


def load_game_data():

    global items, max_ilvl

    log("Loading game data...")

    try:

        items, max_ilvl = load_all_items()

        max_ilvl_var.set(str(max_ilvl))

        log(f"Game data loaded. Highest ilvl: {max_ilvl}")

    except Exception as e:
        log(f"error loading data: {e}")


def update_progress(value):

    progress_var.set(value)
    root.update_idletasks()


def run_solver():

    if not items:
        log("No game data loaded")
        return

    try:
        min_ilvl = int(min_ilvl_entry.get())
    except:
        log("Invalid min ilvl")
        return

    gcd = gcd_var.get()
    food = food_var.get()

    log(f"Items after ilvl filter ({len(items)})")
    log("Running solver...")

    filtered = filter_items(items, min_ilvl)

    progress_var.set(0)

    results = solve(filtered, update_progress)

    if not results:
        log("Solver returned no builds")
        return

    log("Best builds:")

    for build in results:

        log(f"Build {build['rank']} DPS {build['dps']}")

        for item in build["items"]:
            log(f"  {item}")

        log("")


def run_solver_thread():

    threading.Thread(target=run_solver).start()


root = tk.Tk()
root.title("FFXIV BLM Gear Solver")

# ----------------
# Controls
# ----------------

controls = tk.Frame(root)
controls.pack(pady=10)

load_btn = tk.Button(controls, text="Load Game Data", command=load_game_data)
load_btn.grid(row=0, column=0, padx=5)

tk.Label(controls, text="Min ilvl").grid(row=0, column=1)

min_ilvl_entry = tk.Entry(controls, width=6)
min_ilvl_entry.insert(0, "760")
min_ilvl_entry.grid(row=0, column=2)

solve_btn = tk.Button(controls, text="Run Solver", command=run_solver_thread)
solve_btn.grid(row=0, column=3, padx=5)

tk.Label(controls, text="Max ilvl").grid(row=0, column=4)

max_ilvl_var = tk.StringVar(value="-")

max_ilvl_label = tk.Label(controls, textvariable=max_ilvl_var, width=6)
max_ilvl_label.grid(row=0, column=5)


# ----------------
# Food + GCD
# ----------------

options = tk.Frame(root)
options.pack()

tk.Label(options, text="Food").grid(row=0, column=0)

food_var = tk.StringVar(value="None")

food_dropdown = ttk.Combobox(
    options,
    textvariable=food_var,
    values=[
        "None",
        "Raid Food",
        "Spell Speed Food"
    ],
    state="readonly",
    width=20
)

food_dropdown.grid(row=0, column=1, padx=10)

tk.Label(options, text="Target GCD").grid(row=0, column=2)

gcd_var = tk.StringVar(value="2.50")

gcd_dropdown = ttk.Combobox(
    options,
    textvariable=gcd_var,
    values=[
        "2.50",
        "2.48",
        "2.46",
        "2.44",
        "2.42",
        "2.40"
    ],
    state="readonly",
    width=10
)

gcd_dropdown.grid(row=0, column=3)


# ----------------
# Progress bar
# ----------------

progress_var = tk.IntVar()

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=400,
    variable=progress_var,
    mode="determinate"
)

progress.pack(pady=10)


# ----------------
# Log window
# ----------------

log_box = tk.Text(root, height=20, width=100)
log_box.pack()

init_logger(log_box)

log("Application started")

root.mainloop()
