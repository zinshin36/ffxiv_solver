# tests/test_solver.py
import os
import pytest
from engine.csv_loader import load_items, load_materia
from engine.optimizer import top_sets
from engine.simulator import simulate_dps  # now exists
