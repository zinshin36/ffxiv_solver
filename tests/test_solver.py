from engine.simulator import score
from engine.csv_loader import load_items, load_materia
from engine.optimizer import top_sets

def test_top_sets_runs():
    items = load_items()
    materia_list = load_materia()
    results = top_sets(items, materia_list, top_n=1)
    assert results
    assert "gear" in results[0]
    assert "dps" in results[0]
