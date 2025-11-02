import os
import pytest

from phoebe_client import PhoebeClient

pytestmark = pytest.mark.skipif(
    not os.getenv("PHOEBE_LIVE"),
    reason="Live server test requires PHOEBE_LIVE=1 and a running server",
)


def test_live_server_basic_flow():
    with PhoebeClient() as client:
        # Start session is implicit via context manager; verify server is reachable
        sessions = client.sessions.get_sessions()
        assert isinstance(sessions, dict)

        # Set and get values
        client.set_value(twig="period@binary", value=0.56)
        m1 = client.get_value(twig="mass@primary")
        # We can't assume exact value; just that a value returned without error
        assert m1 is not None
