import tkinter as tk
from tkinter import messagebox

from engine.data_parser import load_items
from engine.materia_system import load_materia
from engine.optimizer import solve
from engine.logger import log


items = []
materia = []


def load_data():

    global items, materia

    try:

        items = load_items(650)
        materia = load_materia()

        messagebox.showinfo(
            "Loaded",
            f"{len(items)} items loaded"
        )

    except Exception as e:

        messagebox.showerror("Error", str(e))


def run_solver():

    if not items:
        messagebox.showerror("Error", "Load data first")
        return

    result, dps = solve(items, materia, 2.38)

    build, stats, food = result

    output = f"Best DPS: {dps:.2f}\n\n"

    for name, melds in build:

        meld_names = [m["name"] for m in melds]

        output += f"{name} | {', '.join(meld_names)}\n"

    messagebox.showinfo("Best Build", output)


root = tk.Tk()
root.title("FFXIV Gear Solver")

tk.Button(root, text="Load Game Data", command=load_data, width=30).pack(pady=10)
tk.Button(root, text="Run Solver", command=run_solver, width=30).pack(pady=10)

log("Application started")

root.mainloop()
