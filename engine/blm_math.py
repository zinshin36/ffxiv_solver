import tkinter as tk

from engine.logger import log
from engine.csv_loader import load_items, load_materia
from engine.optimizer import top_sets


def run_solver():

    try:
        target_gcd = float(gcd_entry.get())
    except:
        target_gcd = None

    log("Running solver...")

    items = load_items()
    materia = load_materia()

    top_sets(items, materia, target_gcd)


root = tk.Tk()
root.title("FFXIV BLM Gear Solver")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()


tk.Label(frame, text="Target GCD").grid(row=0, column=0)

gcd_entry = tk.Entry(frame, width=10)
gcd_entry.insert(0, "2.38")
gcd_entry.grid(row=0, column=1)


run_button = tk.Button(frame, text="Run Solver", command=run_solver)
run_button.grid(row=1, column=0, columnspan=2, pady=10)


root.mainloop()
