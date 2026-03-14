import tkinter as tk
from tkinter import messagebox, simpledialog

from engine.csv_loader import load_items, load_materia
from engine.optimizer import top_sets
from engine.logger import log


items = []
materia = []
blacklist = []


def load_data():

    global items, materia

    try:

        items = load_items()
        materia = load_materia()

        messagebox.showinfo("Loaded", f"{len(items)} items loaded")

    except Exception as e:

        messagebox.showerror("Error", str(e))


def set_blacklist():

    global blacklist

    text = simpledialog.askstring(
        "Blacklist",
        "Enter item names separated by commas"
    )

    if not text:
        return

    blacklist = [x.strip() for x in text.split(",")]

    log(f"Blacklist set: {blacklist}")


def run_solver():

    if not items:

        messagebox.showerror("Error", "Load data first")
        return

    results = top_sets(items, materia, blacklist)

    if not results:

        messagebox.showinfo("Result", "No sets found")
        return

    best = results[0]["dps"]

    output = ""

    for r in results:

        diff = best - r["dps"]

        gear = ", ".join(
            [g["Name"] for g in r["gear"].values()]
        )

        output += f"{r['dps']:.2f} DPS (-{diff:.2f})\n{gear}\n\n"

    messagebox.showinfo("Top 10 Sets", output)


root = tk.Tk()
root.title("FFXIV Gear Solver")

tk.Button(root, text="Load Game Data", command=load_data, width=30).pack(pady=10)
tk.Button(root, text="Set Blacklist", command=set_blacklist, width=30).pack(pady=10)
tk.Button(root, text="Run Solver", command=run_solver, width=30).pack(pady=10)

log("Application started")

root.mainloop()
