import tkinter as tk
from tkinter import messagebox

from engine.data_parser import load_all_items, filter_items
from engine.materia_system import load_materia
from engine.optimizer import solve
from engine.food_system import FOODS
from engine.logger import log


all_items = []
materia = []
max_ilvl = 0


class App:

    def __init__(self, root):

        self.root = root
        root.title("FFXIV Gear Solver")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Highest Detected iLvl").grid(row=0, column=0)

        self.max_ilvl_label = tk.Label(frame, text="Unknown")
        self.max_ilvl_label.grid(row=0, column=1)

        tk.Label(frame, text="Minimum iLvl").grid(row=1, column=0)

        self.ilvl_entry = tk.Entry(frame)
        self.ilvl_entry.insert(0, "0")
        self.ilvl_entry.grid(row=1, column=1)

        tk.Label(frame, text="Target GCD").grid(row=2, column=0)

        self.gcd_entry = tk.Entry(frame)
        self.gcd_entry.insert(0, "2.38")
        self.gcd_entry.grid(row=2, column=1)

        tk.Label(frame, text="Food").grid(row=3, column=0)

        self.food_var = tk.StringVar()
        self.food_var.set("None")

        tk.OptionMenu(frame, self.food_var, *FOODS.keys()).grid(row=3, column=1)

        tk.Button(
            frame,
            text="Load Game Data",
            command=self.load_data,
            width=25
        ).grid(row=4, column=0, columnspan=2, pady=5)

        tk.Button(
            frame,
            text="Run Solver",
            command=self.run_solver,
            width=25
        ).grid(row=5, column=0, columnspan=2, pady=5)

        self.output = tk.Text(root, width=95, height=28)
        self.output.pack(pady=10)

        log("Application started")

    def load_data(self):

        global all_items, materia, max_ilvl

        try:

            all_items, max_ilvl = load_all_items()

            materia = load_materia()

            self.max_ilvl_label.config(text=str(max_ilvl))

            self.ilvl_entry.delete(0, tk.END)
            self.ilvl_entry.insert(0, str(max_ilvl - 20))

            messagebox.showinfo(
                "Data Loaded",
                f"{len(all_items)} items loaded\nMax iLvl: {max_ilvl}"
            )

        except Exception as e:

            messagebox.showerror("Error", str(e))

    def run_solver(self):

        global all_items, materia

        if not all_items:

            messagebox.showerror("Error", "Load game data first")
            return

        try:

            min_ilvl = int(self.ilvl_entry.get())
            gcd = float(self.gcd_entry.get())

        except:

            messagebox.showerror("Error", "Invalid numeric input")
            return

        items = filter_items(all_items, min_ilvl)

        if not items:

            messagebox.showerror("Error", "No items after filter")
            return

        result, dps = solve(items, materia, gcd)

        build, stats, food = result

        self.output.delete("1.0", tk.END)

        self.output.insert(tk.END, f"Best DPS: {dps:.2f}\n\n")

        self.output.insert(tk.END, "Gear + Melds\n\n")

        for name, melds in build:

            meld_names = []

            for m in melds:

                if isinstance(m, dict):
                    meld_names.append(m.get("name", "Unknown Materia"))
                else:
                    meld_names.append(str(m))

            meld_text = ", ".join(meld_names) if meld_names else "No Melds"

            self.output.insert(
                tk.END,
                f"{name}\n   Materia: {meld_text}\n\n"
            )

        self.output.insert(tk.END, "Final Stats\n\n")

        for k, v in stats.items():

            self.output.insert(tk.END, f"{k}: {v}\n")


def main():

    root = tk.Tk()

    App(root)

    root.mainloop()


if __name__ == "__main__":
    main()
