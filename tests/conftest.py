"""Pytest configuration and shared fixtures for API tests"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import app as app_module


# Store the original activities for restoration
_original_activities = None


@pytest.fixture
def sample_activities():
    """
    Fixture that provides a fresh copy of activities data for each test.
    This ensures test isolation and prevents test interdependence.
    """
    return deepcopy(app_module.activities)


@pytest.fixture
def client(sample_activities):
    """
    Fixture that provides a TestClient with fresh activity data per test.
    This clears the app's global activities dict and restores it with a fresh copy
    before each test, ensuring complete test isolation.
    
    Arrange pattern: This fixture sets up a clean slate for each test.
    """
    # Save the current activities state
    saved_state = deepcopy(app_module.activities)
    
    # Clear and repopulate with fresh test data
    app_module.activities.clear()
    app_module.activities.update(sample_activities)
    
    # Create test client
    test_client = TestClient(app_module.app)
    
    # Yield to the test
    yield test_client
    
    # Restore original state after test completes
    app_module.activities.clear()
    app_module.activities.update(saved_state)
