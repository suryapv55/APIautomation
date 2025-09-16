import pytest
import requests
from utilities.helpers import Helpers

@pytest.fixture(scope="session")
def helpers():
    """Provide a Helpers instance for all tests."""
    return Helpers()

@pytest.fixture(scope="session")
def http_session():
    """Provide a reusable HTTP session for all tests."""
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture(scope="session")
def base_url(helpers):
    """Provide the base URL from config."""
    return helpers.config['base_url']