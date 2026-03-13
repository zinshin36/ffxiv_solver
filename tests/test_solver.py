import os
import pytest
from engine.csv_loader import load_items, load_materia
from engine.optimizer import top_sets
from engine.simulator import simulate_dps

# Ensure we are reading CSVs from relative folder
@pytest.fixture
def csv_folder():
    folder = os.path.join(os.getcwd(), "game_data")
    if not os.path.exists(folder):
        pytest.fail(f"game_data folder not found in {os.getcwd()}")
    return folder

def test_top_sets_runs(csv_folder):
    # Load real CSVs
    items = load_items(csv_folder)
    materia_list = load_materia(csv_folder)

    # Run top_sets optimizer (top 1 for test speed)
    top10 = top_sets(items, materia_list, top_n=1)

    # Assertions
    assert top10, "top_sets returned empty"
    assert "gear" in top10[0], "No gear in top_sets output"
    assert "dps" in top10[0], "No dps in top_sets output"
