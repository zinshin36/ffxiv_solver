# main.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from engine.csv_loader import load_items
from engine.optimizer import top_sets
from engine.logger import log

current_items = []
current_blacklist = []

def load_game_data():
    global current_items
    try:
        current_items = load_items()
        messagebox.showinfo("Success", f"Loaded {len(current_items)} items")
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
        log(str(e))

def set_blacklist():
    global current_blacklist
    blacklist_input = simpledialog.askstring(
        "Blacklist",
        "Enter items to blacklist (comma separated):"
    )
    if blacklist_input:
        current_blacklist = [x.strip() for x in blacklist_input.split(",")]
        messagebox.showinfo("Blacklist Updated", f"{len(current_blacklist)} items blacklisted")
        log(f"Blacklist updated: {current_blacklist}")

def calculate_top_sets():
    if not current_items:
        messagebox.showerror("Error", "Load game data first")
        return
    results = top_sets(current_items, top_n=10, blacklist=current_blacklist)
    if not results:
        messagebox.showinfo("Result", "No valid sets found")
        return
    output = ""
    best_dps = results[0]["dps"]
    for r in results:
        gear_names = ", ".join([i["Name"] for i in r["gear"].values()])
        diff = best_dps - r["dps"]
        output += f"DPS: {r['dps']:.2f} (-{diff:.2f}) | Gear: {gear_names}\n"
    messagebox.showinfo("Top 10 Sets", output)
    log("Top 10 sets calculated")

root = tk.Tk()
root.title("FFXIV Gear Optimizer")

tk.Button(root, text="Load Game Data", command=load_game_data, width=30).pack(pady=10)
tk.Button(root, text="Set Blacklist", command=set_blacklist, width=30).pack(pady=10)
tk.Button(root, text="Calculate Top Sets", command=calculate_top_sets, width=30).pack(pady=10)

log("Application Started")
root.mainloop()
