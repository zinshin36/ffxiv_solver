import tkinter as tk
from tkinter import ttk
import json
import os

from engine.optimizer import run_solver

class App:
    def __init__(self, root, items_by_slot):
        self.root = root
        self.items_by_slot = items_by_slot

        self.root.title("BIS Solver")

        self.min_ilvl = tk.IntVar(value=780)
        self.gcd = tk.DoubleVar(value=0.0)

        self.build_mode = tk.StringVar(value="CRIT")

        self.foods = self.load_foods()
        self.selected_food = tk.StringVar(value=list(self.foods.keys())[0] if self.foods else "")

        self.build_ui()

    def load_foods(self):
        if not os.path.exists("foods.json"):
            return {}
        with open("foods.json") as f:
            return json.load(f)

    def build_ui(self):
        tk.Label(self.root, text="Min iLvl").pack()
        tk.Entry(self.root, textvariable=self.min_ilvl).pack()

        tk.Label(self.root, text="Target GCD (0 = ignore)").pack()
        tk.Entry(self.root, textvariable=self.gcd).pack()

        tk.Label(self.root, text="Food").pack()
        ttk.Combobox(self.root, textvariable=self.selected_food, values=list(self.foods.keys())).pack()

        tk.Label(self.root, text="Build Type").pack()
        ttk.Combobox(
            self.root,
            textvariable=self.build_mode,
            values=["CRIT","SPS"]
        ).pack()

        tk.Button(self.root, text="Run Solver", command=self.run).pack()

        self.output = tk.Text(self.root, height=30, width=80)
        self.output.pack()

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def run(self):
        self.output.delete(1.0, tk.END)

        min_ilvl = self.min_ilvl.get()
        gcd = self.gcd.get()
        food = self.foods.get(self.selected_food.get(), {})

        filtered = {}

        for slot, items in self.items_by_slot.items():
            valid = [i for i in items if i["ilvl"] >= min_ilvl]
            filtered[slot] = sorted(valid, key=lambda x: (x["ilvl"], sum(x["stats"].values())), reverse=True)[:3]

            self.log(f"[SLOT] {slot}: {len(filtered[slot])} items")

        results = run_solver(filtered, food, gcd if gcd > 0 else None, self, self.build_mode.get())

        self.log("\n===== RESULTS =====\n")

        for i, (dps, build, result) in enumerate(results, 1):
            self.log(f"=== BUILD {i} ===")
            self.log(f"DPS: {round(dps,2)}")
            self.log(f"GCD: {result['gcd']:.3f}")

            stats = result["stats"]
            self.log(f"CRIT: {stats['crit']}  DH: {stats['dh']}  DET: {stats['det']}  SPS: {stats['sps']}\n")

            for slot, item in build.items():
                self.log(f"{slot}: {item['name']}")
                melds = result["melds"][slot]
                if melds:
                    self.log(f"  melds: {', '.join(melds)}")

            self.log("")
