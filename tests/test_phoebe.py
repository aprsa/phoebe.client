"""Tests for PhoebeAPI."""

import pytest
from phoebe_client.server_api import PhoebeAPI


def test_phoebe_api_init():
    api = PhoebeAPI(client_id="test-123")
    assert api.client_id == "test-123"


def test_send_command_without_client_id():
    api = PhoebeAPI()
    with pytest.raises(ValueError, match="No client ID"):
        api.execute("get_value")
