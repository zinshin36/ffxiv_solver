# gui/app.py
import sys
import traceback
from engine.logger import log

# Wrap imports in try/except to prevent silent import crash
try:
    from engine.food import load_foods
except Exception as e:
    print(f"[IMPORT FAILED] engine.food.load_foods: {e}")
    load_foods = lambda: []

try:
    from engine.data_loader import load_items, load_materia
except Exception as e:
    print(f"[IMPORT FAILED] engine.data_loader: {e}")
    load_items = lambda: []
    load_materia = lambda: []
