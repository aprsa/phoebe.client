"""Minimal live server smoke test.

Requires a phoebe-server running and a valid API key in config.toml.
This script will:
    1) Start a session
    2) Set period@binary to 0.56
    3) Fetch mass@primary
    4) Close the session

Run directly with Python.
"""

from phoebe_client import PhoebeClient
from phoebe_client.exceptions import SessionError, CommandError


def main() -> int:
    try:
        with PhoebeClient() as client:  # uses host/port/API key from config.toml
            # Optional: check port status (will raise if unauthorized/unavailable)
            try:
                status = client.sessions.get_port_status()
                print("Port status:", status)
            except SessionError as e:
                # Non-fatal; continue if endpoint not available
                print("Warning: could not read port status:", e)

            # Set period on the binary
            print("Setting period@binary = 0.56 ...")
            client.set_value(twig="period@binary", value=0.56)

            # Read primary mass
            print("Getting mass@primary ...")
            m1 = client.get_value(twig="mass@primary")
            print("mass@primary:", m1)
        print("Session closed. ✅")
        return 0
    except (SessionError, CommandError, ValueError) as e:
        print("Live smoke test failed:", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
