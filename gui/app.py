import tkinter as tk
import json
import os
import traceback

from engine.data_parser import load_items
from engine.optimizer import run_solver
from engine.logger import log, init_logger


class App:

    def __init__(self, root):

        root.title("FFXIV Solver")

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        # GCD
        tk.Label(frame, text="Target GCD").grid(row=0, column=0)
        self.gcd = tk.Entry(frame)
        self.gcd.insert(0, "2.38")
        self.gcd.grid(row=0, column=1)

        # iLvl
        tk.Label(frame, text="Min iLvl").grid(row=1, column=0)
        self.ilvl = tk.Entry(frame)
        self.ilvl.insert(0, "780")
        self.ilvl.grid(row=1, column=1)

        # Food dropdown
        tk.Label(frame, text="Food").grid(row=2, column=0)

        self.food_var = tk.StringVar()
        self.food_dropdown = tk.OptionMenu(frame, self.food_var, "")
        self.food_dropdown.grid(row=2, column=1)

        # Buttons
        tk.Button(frame, text="Detect Max iLvl", command=self.detect_ilvl).grid(row=3, column=0)
        tk.Button(frame, text="Run Solver", command=self.run).grid(row=3, column=1)

        # Log box
        self.log_box = tk.Text(root, height=20, width=100)
        self.log_box.pack(padx=10, pady=10)

        init_logger(self.log_box)

        log("GUI Ready")

        self.load_systems()

    def load_systems(self):
        log("Loading systems...")

        self.foods = {}

        try:
            if os.path.exists("foods.json"):
                with open("foods.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # convert list → dict by name
                    for food in data:
                        name = food.get("name")
                        if name:
                            self.foods[name] = food

            menu = self.food_dropdown["menu"]
            menu.delete(0, "end")

            if not self.foods:
                log("[INIT] No valid foods found")
            else:
                for food_name in self.foods:
                    menu.add_command(
                        label=food_name,
                        command=lambda f=food_name: self.food_var.set(f)
                    )

            log(f"[INIT] Foods loaded: {len(self.foods)}")

        except Exception:
            log("[INIT ERROR] Failed to load foods.json")
            log(traceback.format_exc())

    def detect_ilvl(self):
        log("Detecting max item level...")
        _, max_ilvl = load_items()
        log(f"Max iLvl detected: {max_ilvl}")

    def run(self):
        gcd = float(self.gcd.get())
        ilvl = int(self.ilvl.get())
        food_name = self.food_var.get()

        log(f"Running solver | GCD={gcd} | Min iLvl={ilvl} | Food={food_name}")

        items, _ = load_items(ilvl)

        selected_food = self.foods.get(food_name, {})

        run_solver(items, gcd, selected_food)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
