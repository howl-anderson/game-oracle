import pytest
from unittest.mock import patch, MagicMock
from get_matches_by_player import retry_client_execute

@pytest.fixture(autouse=True)
def mock_env_api_key():
    with patch.dict('os.environ', {'STRATZ_API_KEY': 'test_key'}):
        yield

@pytest.fixture
def mock_response():
    return {
        "data": {
            "player": {
                "matches": [
                    {
                        "id": 123456789,
                        "didRadiantWin": True,
                        "pickBans": []
                    }
                ]
            }
        }
    }

def test_retry_client_execute(mock_response):
    mock_client = MagicMock()
    mock_client.execute.return_value = mock_response
    mock_query = MagicMock()
    mock_vars = {"test": "value"}
    
    result = retry_client_execute(mock_client, mock_query, mock_vars)
    assert result == mock_response
    mock_client.execute.assert_called_once_with(mock_query, variable_values=mock_vars)
