import pytest
from unittest.mock import patch, MagicMock
from get_players import setup_client, DIVISIONS

@pytest.fixture(autouse=True)
def mock_env_api_key():
    with patch.dict('os.environ', {'STRATZ_API_KEY': 'test_key'}):
        yield

def test_setup_client():
    with patch('get_players.RequestsHTTPTransport') as mock_transport:
        client = setup_client()
        assert client is not None

def test_division_names():
    assert all(d in ["AMERICAS", "SE_ASIA", "EUROPE", "CHINA"] for d in DIVISIONS)
