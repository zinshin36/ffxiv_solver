from engine.simulator import score

def test_score_basic():
    # minimal stats for testing
    gear_set = {
        "Weapon": {"stats": {"WeaponDamage": 100, "Intelligence": 200}},
        "Head": {"stats": {"Intelligence": 50}},
    }

    result = score(gear_set)
    assert result > 0
