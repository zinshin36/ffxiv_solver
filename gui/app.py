import tkinter as tk
import threading

from engine.data_parser import load_items
from engine.optimizer import solve
from engine.logger import init_logger, log


class App:

    def __init__(self, root):

        root.title("BLM Solver")

        frame = tk.Frame(root)
        frame.pack()

        tk.Label(frame, text="Target GCD").grid(row=0, column=0)
        self.gcd = tk.Entry(frame)
        self.gcd.insert(0, "2.38")
        self.gcd.grid(row=0, column=1)

        tk.Label(frame, text="Min iLvl").grid(row=1, column=0)
        self.ilvl = tk.Entry(frame)
        self.ilvl.insert(0, "0")
        self.ilvl.grid(row=1, column=1)

        tk.Button(frame, text="Run Solver", command=self.run).grid(row=2, column=0, columnspan=2)

        # LOG BOX
        self.log_box = tk.Text(root, height=20, width=80)
        self.log_box.pack()

        init_logger(self.log_box)

        log("GUI Ready")

        self.items = []
        self.max_ilvl = 0

        threading.Thread(target=self.load_data).start()

    def load_data(self):
        log("Detecting max item level...")
        self.items, self.max_ilvl = load_items()
        log(f"Max iLvl detected: {self.max_ilvl}")

    def run(self):
        threading.Thread(target=self.run_solver).start()

    def run_solver(self):

        gcd = float(self.gcd.get())
        ilvl = int(self.ilvl.get())

        log(f"Running solver | GCD={gcd} | Min iLvl={ilvl}")

        solve(self.items, gcd, ilvl)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
