import tkinter as tk

from engine.csv_loader import load_items, load_materia
from engine.optimizer import top_sets
from engine.logger import log


class SolverGUI:

    def __init__(self, root):

        self.root = root
        root.title("FFXIV BLM Gear Solver")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Target GCD").grid(row=0, column=0)

        self.gcd_entry = tk.Entry(frame, width=10)
        self.gcd_entry.insert(0, "2.38")
        self.gcd_entry.grid(row=0, column=1)

        run_button = tk.Button(
            frame,
            text="Run Solver",
            command=self.run_solver
        )

        run_button.grid(row=1, column=0, columnspan=2, pady=10)

    def run_solver(self):

        try:
            target_gcd = float(self.gcd_entry.get())
        except:
            target_gcd = None

        log("Running solver...")

        items = load_items()
        materia = load_materia()

        top_sets(items, materia, target_gcd)


def main():

    root = tk.Tk()

    SolverGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
