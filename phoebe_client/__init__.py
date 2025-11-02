"""PHOEBE Client for interacting with PHOEBE backend services."""

__version__ = "0.1.0"

from .client import PhoebeClient
from .server_api import SessionAPI, PhoebeAPI
from .exceptions import PhoebeClientError, AuthenticationError, SessionError, CommandError

__all__ = [
    'PhoebeClient',
    'SessionAPI',
    'PhoebeAPI',
    'PhoebeClientError',
    'AuthenticationError',
    'SessionError',
    'CommandError',
]
