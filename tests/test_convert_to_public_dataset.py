import pytest
from convert_to_public_dataset import process_matches

@pytest.fixture
def sample_match_data():
    return {
        "match_id": 123456789,
        "radiant_win": True,
        "RadiantHeroes": [1, 2, 3, 4, 5],
        "DireHeroes": [6, 7, 8, 9, 10],
        "RadiantBanedHeroes": [11, 12],
        "DireBanedHeroes": [13, 14]
    }

def test_process_matches(sample_match_data):
    result = process_matches(sample_match_data)
    assert isinstance(result, dict)
    assert "radiant_heroes" in result
    assert "dire_heroes" in result
