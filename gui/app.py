import tkinter as tk
import threading
import json
import os

from engine.data_parser import load_items
from engine.optimizer import solve, load_food
from engine.logger import init_logger, log
from engine.blacklist import load_blacklist


class App:

    def __init__(self, root):

        root.title("BLM Solver")

        frame = tk.Frame(root)
        frame.pack()

        # GCD
        tk.Label(frame, text="Target GCD").grid(row=0, column=0)
        self.gcd = tk.Entry(frame)
        self.gcd.insert(0, "2.38")
        self.gcd.grid(row=0, column=1)

        # ILVL
        tk.Label(frame, text="Min iLvl").grid(row=1, column=0)
        self.ilvl = tk.Entry(frame)
        self.ilvl.insert(0, "0")
        self.ilvl.grid(row=1, column=1)

        # FOOD DROPDOWN
        tk.Label(frame, text="Food").grid(row=2, column=0)

        self.food_var = tk.StringVar()
        self.food_dropdown = tk.OptionMenu(frame, self.food_var, "")
        self.food_dropdown.grid(row=2, column=1)

        # BUTTON
        tk.Button(frame, text="Run Solver", command=self.run).grid(row=3, column=0, columnspan=2)

        # LOG BOX
        self.log_box = tk.Text(root, height=20, width=90)
        self.log_box.pack()

        init_logger(self.log_box)

        log("GUI Ready")

        self.items = []
        self.max_ilvl = 0

        threading.Thread(target=self.load_data).start()

    def load_data(self):

        log("Loading systems...")

        # blacklist
        bl = load_blacklist()
        log(f"[INIT] Blacklist loaded: {len(bl)}")

        # food
        foods = load_food()

        names = [f["name"] for f in foods] if foods else ["None"]

        self.food_var.set(names[0])

        menu = self.food_dropdown["menu"]
        menu.delete(0, "end")

        for name in names:
            menu.add_command(label=name, command=lambda v=name: self.food_var.set(v))

        # items
        log("Detecting max item level...")
        self.items, self.max_ilvl = load_items()

        log(f"Max iLvl detected: {self.max_ilvl}")

    def run(self):
        threading.Thread(target=self.run_solver).start()

    def run_solver(self):

        gcd = float(self.gcd.get())
        ilvl = int(self.ilvl.get())
        food = self.food_var.get()

        log(f"Running solver | GCD={gcd} | Min iLvl={ilvl} | Food={food}")

        solve(self.items, gcd, ilvl, food)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
