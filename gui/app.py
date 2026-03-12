import tkinter as tk
from tkinter import messagebox

from engine.csv_loader import load_items, load_materia
from engine.gear_filter import filter_items, group_by_slot
from engine.solver import solve


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("FFXIV Gear Solver")

        self.blacklist = []

        self.box = tk.Listbox(root, width=40)
        self.box.pack()

        entry_frame = tk.Frame(root)
        entry_frame.pack()

        self.entry = tk.Entry(entry_frame, width=30)
        self.entry.pack(side=tk.LEFT)

        add = tk.Button(entry_frame, text="Add", command=self.add_blacklist)
        add.pack(side=tk.LEFT)

        remove = tk.Button(root, text="Remove Selected", command=self.remove_blacklist)
        remove.pack()

        run = tk.Button(root, text="Run Solver", command=self.run_solver)
        run.pack()

        self.output = tk.Text(root, width=80, height=20)
        self.output.pack()

    def add_blacklist(self):

        text = self.entry.get()

        if not text:
            return

        self.blacklist.append(text)

        self.box.insert(tk.END, text)

        self.entry.delete(0, tk.END)

    def remove_blacklist(self):

        sel = self.box.curselection()

        if not sel:
            return

        idx = sel[0]

        self.box.delete(idx)

        del self.blacklist[idx]

    def run_solver(self):

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

        best = results[0]["dps"]

        for i, r in enumerate(results, 1):

            diff = best - r["dps"]

            self.output.insert(tk.END, f"\nRank {i}\n")
            self.output.insert(tk.END, f"DPS {r['dps']:.2f}\n")
            self.output.insert(tk.END, f"Loss {diff:.2f}\n")

            for g in r["gear"]:
                self.output.insert(tk.END, f"  {g['name']}\n")
