"""Shared test configuration and fixtures."""
import pytest
from main import limiter


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset rate limiter between tests."""
    # Clear rate limiter storage before each test
    if hasattr(limiter, '_storage'):
        limiter._storage.storage.clear()
    yield
    # Clear again after test
    if hasattr(limiter, '_storage'):
        limiter._storage.storage.clear()
