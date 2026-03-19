import tkinter as tk
from tkinter import scrolledtext

from engine.data_parser import load_items
from engine.optimizer import run_solver
from engine.logger import log, init_logger, set_widget


class App:

    def __init__(self, root):

        root.title("BLM Gear Solver")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # --- GCD ---
        tk.Label(frame, text="Target GCD").grid(row=0, column=0)
        self.gcd = tk.Entry(frame)
        self.gcd.insert(0, "2.38")
        self.gcd.grid(row=0, column=1)

        # --- iLvl ---
        tk.Label(frame, text="Min Item Level").grid(row=1, column=0)
        self.ilvl = tk.Entry(frame)
        self.ilvl.insert(0, "0")
        self.ilvl.grid(row=1, column=1)

        # --- Detect Button ---
        tk.Button(
            frame,
            text="Detect Max iLvl",
            command=self.detect_ilvl
        ).grid(row=2, column=0, columnspan=2, pady=5)

        # --- Run Button ---
        tk.Button(
            frame,
            text="Run Solver",
            command=self.run
        ).grid(row=3, column=0, columnspan=2, pady=5)

        # --- Log Box ---
        self.log_box = scrolledtext.ScrolledText(frame, height=20)
        self.log_box.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)

        frame.rowconfigure(4, weight=1)
        frame.columnconfigure(1, weight=1)

        # attach logger to GUI
        init_logger(self.log_box)
        set_widget(self.log_box)

        log("GUI Ready")

    def detect_ilvl(self):
        try:
            log("Detecting max item level...")
            _, max_ilvl = load_items()
            self.ilvl.delete(0, tk.END)
            self.ilvl.insert(0, str(max_ilvl))
            log(f"Max iLvl detected: {max_ilvl}")
        except Exception as e:
            log(f"[ERROR] iLvl detection failed: {e}")

    def run(self):
        try:
            gcd = float(self.gcd.get())
            min_ilvl = int(self.ilvl.get())

            log(f"Running solver | GCD={gcd} | Min iLvl={min_ilvl}")

            items, _ = load_items(min_ilvl)

            if not items:
                log("[ERROR] No items after filtering")
                return

            run_solver(items, gcd)

        except Exception as e:
            log(f"[GUI ERROR] {e}")


def main():
    root = tk.Tk()
    root.geometry("700x500")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
