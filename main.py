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

    items, max_ilvl = load_all_items()

    max_ilvl_var.set(str(max_ilvl))

    log(f"Game data loaded. Highest ilvl: {max_ilvl}")


def update_progress(v):

    progress_var.set(v % 100)

    root.update_idletasks()


def run_solver():

    if not items:
        log("No game data loaded")
        return

    min_ilvl = int(min_ilvl_entry.get())

    gcd = gcd_var.get()

    food = food_var.get()

    log(f"Min ilvl {min_ilvl}")
    log(f"GCD target {gcd}")
    log(f"Food {food}")

    filtered = filter_items(items, min_ilvl)

    log(f"Items after ilvl filter ({len(filtered)})")

    results = solve(filtered, gcd, update_progress)

    log("Top builds:")

    for build in results:

        log(f"Build {build['rank']} Score {build['score']}")

        for item in build["items"]:
            log(f"  {item}")

        log("")


def solver_thread():

    threading.Thread(target=run_solver).start()


root = tk.Tk()
root.title("FFXIV BLM Gear Solver")

controls = tk.Frame(root)
controls.pack(pady=10)

tk.Button(
    controls,
    text="Load Game Data",
    command=load_game_data
).grid(row=0, column=0)

tk.Label(controls, text="Min ilvl").grid(row=0, column=1)

min_ilvl_entry = tk.Entry(controls, width=6)
min_ilvl_entry.insert(0, "760")
min_ilvl_entry.grid(row=0, column=2)

tk.Button(
    controls,
    text="Run Solver",
    command=solver_thread
).grid(row=0, column=3)

tk.Label(controls, text="Max ilvl").grid(row=0, column=4)

max_ilvl_var = tk.StringVar(value="-")

tk.Label(
    controls,
    textvariable=max_ilvl_var,
    width=6
).grid(row=0, column=5)


options = tk.Frame(root)
options.pack()

tk.Label(options, text="Food").grid(row=0, column=0)

food_var = tk.StringVar(value="None")

ttk.Combobox(
    options,
    textvariable=food_var,
    values=[
        "None",
        "Raid Food",
        "Spell Speed Food"
    ],
    state="readonly",
    width=20
).grid(row=0, column=1)

tk.Label(options, text="Target GCD").grid(row=0, column=2)

gcd_var = tk.StringVar(value="2.50")

ttk.Combobox(
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
).grid(row=0, column=3)


progress_var = tk.IntVar()

ttk.Progressbar(
    root,
    orient="horizontal",
    length=450,
    variable=progress_var
).pack(pady=10)


log_box = tk.Text(root, height=20, width=110)
log_box.pack()

init_logger(log_box)

log("Application started")

root.mainloop()
