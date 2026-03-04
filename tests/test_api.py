"""Tests for the unitfyi API client."""

from unitfyi.api import UnitFYI


def test_client_init() -> None:
    """Client initializes with default URL."""
    client = UnitFYI()
    assert str(client._client.base_url).rstrip("/") == "https://unitfyi.com/api"
    client.close()


def test_client_custom_url() -> None:
    """Client accepts custom base URL."""
    client = UnitFYI(base_url="https://custom.example.com/api")
    assert str(client._client.base_url).rstrip("/") == "https://custom.example.com/api"
    client.close()


def test_client_context_manager() -> None:
    """Client works as context manager."""
    with UnitFYI() as client:
        assert client._client is not None
