from engine.simulator import score


def test_score():

    stats = {
        "WeaponDamage": 100,
        "Intelligence": 200
    }

    result = score(stats)

    assert result > 0
