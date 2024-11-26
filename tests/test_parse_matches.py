import pytest
from pathlib import Path
import json
from parse_matches import MatchData, parse_single_file

@pytest.fixture
def sample_match_data():
    return {
        "players": [{
            "matches": [{
                "id": 123456789,
                "didRadiantWin": True,
                "pickBans": [
                    {"isPick": True, "isRadiant": True, "heroId": 1},
                    {"isPick": True, "isRadiant": False, "heroId": 2},
                    {"isPick": False, "isRadiant": True, "heroId": 3},
                    {"isPick": False, "isRadiant": False, "heroId": 4}
                ]
            }]
        }]
    }

@pytest.fixture
def sample_match_file(tmp_path, sample_match_data):
    match_file = tmp_path / "test_match.json"
    match_file.write_text(json.dumps(sample_match_data))
    return match_file

def test_match_data_to_dict():
    match_data = MatchData(
        match_id=123,
        radiant_win=True,
        radiant_heroes=[1, 2, 3],
        dire_heroes=[4, 5, 6],
        radiant_bans=[7, 8],
        dire_bans=[9, 10]
    )
    result = match_data.to_dict()
    assert result["match_id"] == 123
    assert result["radiant_win"] is True
    assert result["RadiantHeroes"] == [1, 2, 3]
    assert result["DireHeroes"] == [4, 5, 6]
    assert result["RadiantBanedHeroes"] == [7, 8]
    assert result["DireBanedHeroes"] == [9, 10]

def test_parse_single_file(sample_match_file):
    result = parse_single_file(sample_match_file)
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], dict)
    assert "match_id" in result[0]
    assert "radiant_win" in result[0]
