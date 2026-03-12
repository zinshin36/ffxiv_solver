import tkinter as tk
from tkinter import simpledialog, messagebox
from engine.csv_loader import load_items, load_materia
from engine.optimizer import top_sets
from engine.logger import logging

class App:
    def __init__(self, root):
        self.root = root
        root.title("FFXIV BiS Solver")

        tk.Button(root, text="Build Top Sets", command=self.build_top_sets).pack(pady=10)

    def build_top_sets(self):
        try:
            items = load_items()
            materia_list = load_materia()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load game data: {e}")
            return

        blacklist_input = simpledialog.askstring(
            "Blacklist",
            "Enter gear names to blacklist (comma-separated):"
        )

        blacklist = []
        if blacklist_input:
            blacklist = [x.strip() for x in blacklist_input.split(",")]

        top10 = top_sets(items, materia_list, blacklist=blacklist)

        if not top10:
            messagebox.showinfo("Result", "No gear sets found.")
            return

        output = ""
        best_dps = top10[0]["dps"]
        for i, s in enumerate(top10):
            output += f"Set {i+1} | DPS {s['dps']:.2f} | Diff {best_dps - s['dps']:.2f}\n"
            for item in s["gear"].values():
                output += f"  {item['name']} (i{item['ilvl']}) Materia:{item.get('MateriaApplied',0)}\n"
            output += "\n"

        messagebox.showinfo("Top Sets", output)
