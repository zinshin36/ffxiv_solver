import tkinter as tk
from tkinter import messagebox

from engine.csv_loader import load_items, load_materia
from engine.gear_filter import filter_items, group_by_slot
from engine.solver import solve


class App:

    def __init__(self, root):

        self.root = root

        self.blacklist = []

        root.title("FFXIV BiS Solver")

        self.entry = tk.Entry(root)
        self.entry.pack()

        tk.Button(root, text="Add Blacklist", command=self.add).pack()

        self.listbox = tk.Listbox(root)
        self.listbox.pack()

        tk.Button(root, text="Run Solver", command=self.run).pack()

        self.output = tk.Text(root, width=80, height=20)
        self.output.pack()

    def add(self):

        t = self.entry.get()

        if not t:
            return

        self.blacklist.append(t)

        self.listbox.insert(tk.END, t)

        self.entry.delete(0, tk.END)

    def run(self):

        self.output.delete("1.0", tk.END)

        try:

            items = load_items()

            materia = load_materia()

            filtered = filter_items(items, self.blacklist)

            slots = group_by_slot(filtered)

            results = solve(slots, materia)

        except Exception as e:

            messagebox.showerror("Error", str(e))
            return

        best = results[0][1]

        for i, (gear, dps) in enumerate(results, 1):

            diff = best - dps

            self.output.insert(tk.END, f"\nRank {i}\n")
            self.output.insert(tk.END, f"DPS {dps}\n")
            self.output.insert(tk.END, f"Loss {diff}\n")

            for g in gear:

                self.output.insert(tk.END, f"  {g['name']}\n")
