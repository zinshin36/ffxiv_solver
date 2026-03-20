import tkinter as tk
from tkinter import ttk
import traceback

from engine.logger import log
from engine.data_loader import load_items
from engine.materia_system import load_materia
from engine.food import load_foods
from engine.blacklist import load_blacklist, is_blacklisted
from engine.optimizer import run_solver


def group_by_slot(items):
    slots = {}

    for item in items:
        slot = item["slot"]

        if slot == "ring":
            slots.setdefault("ring1", []).append(item)
            slots.setdefault("ring2", []).append(item)
        else:
            slots.setdefault(slot, []).append(item)

    return slots


def filter_items(items, min_ilvl, blacklist):
    out = []

    for item in items:
        if item["ilvl"] < min_ilvl:
            continue

        if is_blacklisted(item["name"], blacklist):
            continue

        out.append(item)

    return out


def main():

    log("[GUI] Starting application")

    foods = load_foods()
    items = load_items()
    materia = load_materia()
    blacklist = load_blacklist()

    max_ilvl = max(x["ilvl"] for x in items)

    log(f"[INIT] Foods loaded: {len(foods)}")
    log(f"[INIT] Items loaded: {len(items)}")
    log(f"[INIT] Max iLvl detected: {max_ilvl}")
    log(f"[INIT] Blacklist loaded: {len(blacklist)}")

    root = tk.Tk()
    root.title("FFXIV BIS Solver")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # -------------------------
    # INPUTS
    # -------------------------
    tk.Label(frame, text="Min iLvl").grid(row=0, column=0)
    ilvl_entry = tk.Entry(frame)
    ilvl_entry.insert(0, str(max_ilvl - 10))
    ilvl_entry.grid(row=0, column=1)

    tk.Label(frame, text="Target GCD").grid(row=1, column=0)
    gcd_entry = tk.Entry(frame)
    gcd_entry.insert(0, "2.2")
    gcd_entry.grid(row=1, column=1)

    tk.Label(frame, text="Food").grid(row=2, column=0)

    food_names = ["None"] + [f["name"] for f in foods]
    food_var = tk.StringVar(value="None")

    food_dropdown = ttk.Combobox(frame, textvariable=food_var, values=food_names)
    food_dropdown.grid(row=2, column=1)

    # -------------------------
    # OUTPUT
    # -------------------------
    output = tk.Text(root, width=100, height=25)
    output.pack()

    # -------------------------
    # RUN BUTTON
    # -------------------------
    def run():

        try:
            min_ilvl = int(ilvl_entry.get())
            target_gcd = float(gcd_entry.get())
            selected_food = food_var.get()

            log(f"[RUN] Min iLvl={min_ilvl} | GCD={target_gcd} | Food={selected_food}")

            filtered = filter_items(items, min_ilvl, blacklist)

            log(f"[FILTER] Items after filter: {len(filtered)}")

            slots = group_by_slot(filtered)

            for s, lst in slots.items():
                log(f"[SLOT] {s}: {len(lst)} items")

            # food bonus
            food_bonus = {}

            for f in foods:
                if f["name"] == selected_food:
                    food_bonus = f["bonus"]

            results = run_solver(
                slots,
                target_gcd,
                food_bonus,
                log   # ✅ FIXED LOGGER
            )

            output.delete("1.0", tk.END)

            for i, r in enumerate(results):
                output.insert(tk.END, f"\n=== BUILD {i+1} ===\n")
                output.insert(tk.END, f"DPS: {r['result']['dps']:.2f}\n")
                output.insert(tk.END, f"GCD: {r['result']['gcd']}\n\n")

                for slot, item in r["build"].items():
                    output.insert(tk.END, f"{slot}: {item['name']}\n")

        except Exception as e:
            log("[CRASH DETECTED]")
            log(str(e))
            log(traceback.format_exc())

    tk.Button(frame, text="Run Solver", command=run).grid(row=3, columnspan=2)

    log("[GUI] Ready")
    root.mainloop()


if __name__ == "__main__":
    main()
