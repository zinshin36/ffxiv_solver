import tkinter as tk
from tkinter import filedialog

from engine.logger import log, init_logger
from engine.data_parser import load_all_items, filter_items
from engine.optimizer import solve


items = []
max_ilvl = 0


def load_game_data():

    global items, max_ilvl

    try:

        items, max_ilvl = load_all_items()

        log(f"Game data loaded. Highest ilvl: {max_ilvl}")

    except Exception as e:
        log(f"error: {e}")


def run_solver():

    global items

    if not items:
        log("No data loaded.")
        return

    try:

        min_ilvl = int(min_ilvl_entry.get())

    except:
        log("Invalid min ilvl")
        return

    filtered = filter_items(items, min_ilvl)

    if not filtered:
        log("No items after filtering")
        return

    log("Running solver...")

    results = solve(filtered)

    if not results:
        log("Solver returned no builds")
        return

    for build in results:

        log(f"Build {build['rank']}  DPS: {round(build['dps'],2)}")

        for item in build["items"]:
            log(f"   {item}")

        log("")


init_logger()

root = tk.Tk()
root.title("FFXIV Gear Solver")


load_btn = tk.Button(root, text="Load Game Data", command=load_game_data)
load_btn.pack()


tk.Label(root, text="Min ilvl").pack()

min_ilvl_entry = tk.Entry(root)
min_ilvl_entry.insert(0, "760")
min_ilvl_entry.pack()


solve_btn = tk.Button(root, text="Run Solver", command=run_solver)
solve_btn.pack()


log_box = tk.Text(root, height=20, width=80)
log_box.pack()


root.mainloop()
