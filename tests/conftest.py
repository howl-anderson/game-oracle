import pytest
import json
from pathlib import Path

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory for test data."""
    return tmp_path / "test_data"

@pytest.fixture
def setup_test_environment(test_data_dir):
    """Set up test environment with necessary directories."""
    test_data_dir.mkdir(parents=True, exist_ok=True)
    return test_data_dir
