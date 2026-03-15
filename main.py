import tkinter as tk
from tkinter import messagebox

from engine.data_parser import load_items
from engine.materia_system import load_materia
from engine.optimizer import solve
from engine.food_system import FOODS
from engine.logger import log


items = []
materia = []


class App:

    def __init__(self, root):

        self.root = root
        root.title("FFXIV Gear Solver")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Target GCD").grid(row=0, column=0)

        self.gcd = tk.Entry(frame)
        self.gcd.insert(0, "2.38")
        self.gcd.grid(row=0, column=1)

        tk.Label(frame, text="Minimum iLvl").grid(row=1, column=0)

        self.ilvl = tk.Entry(frame)
        self.ilvl.insert(0, "650")
        self.ilvl.grid(row=1, column=1)

        tk.Label(frame, text="Food").grid(row=2, column=0)

        self.food = tk.StringVar()
        self.food.set("None")

        tk.OptionMenu(frame, self.food, *FOODS.keys()).grid(row=2, column=1)

        tk.Button(
            frame,
            text="Load Game Data",
            command=self.load_data,
            width=25
        ).grid(row=3, column=0, columnspan=2, pady=5)

        tk.Button(
            frame,
            text="Run Solver",
            command=self.run_solver,
            width=25
        ).grid(row=4, column=0, columnspan=2, pady=5)

        self.output = tk.Text(root, width=90, height=25)
        self.output.pack(pady=10)

        log("Application started")

    def load_data(self):

        global items, materia

        try:

            ilvl = int(self.ilvl.get())

            items = load_items(ilvl)
            materia = load_materia()

            messagebox.showinfo(
                "Loaded",
                f"{len(items)} items loaded\n{len(materia)} materia loaded"
            )

        except Exception as e:

            messagebox.showerror("Error", str(e))

    def run_solver(self):

        if not items:
            messagebox.showerror("Error", "Load data first")
            return

        try:

            gcd = float(self.gcd.get())

        except:

            messagebox.showerror("Error", "Invalid GCD value")
            return

        result, dps = solve(items, materia, gcd)

        build, stats, food = result

        self.output.delete("1.0", tk.END)

        self.output.insert(tk.END, f"Best DPS: {dps:.2f}\n\n")

        self.output.insert(tk.END, "Gear + Melds\n\n")

        for name, melds in build:

            meld_names = [m["name"] for m in melds]

            self.output.insert(
                tk.END,
                f"{name} | {', '.join(meld_names)}\n"
            )

        self.output.insert(tk.END, "\nStats\n\n")

        for k, v in stats.items():

            self.output.insert(tk.END, f"{k}: {v}\n")

        self.output.insert(tk.END, f"\nFood: {food}\n")


def main():

    root = tk.Tk()

    App(root)

    root.mainloop()


if __name__ == "__main__":
    main()
