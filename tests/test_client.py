"""Tests for PhoebeClient."""

from unittest.mock import patch
from phoebe_client import PhoebeClient


def test_client_initialization():
    client = PhoebeClient(host="test", port=8000)
    assert client.host == "test"
    assert client.port == 8000


@patch('phoebe_client.server_api.SessionAPI.start_session')
def test_auto_session(mock_start):
    mock_start.return_value = {'session_id': 'test-123'}
    client = PhoebeClient(auto_session=True)
    assert client.phoebe.session_id == 'test-123'
