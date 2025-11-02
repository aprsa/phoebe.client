"""Authentication providers for PHOEBE Client."""

from .base import AuthProvider
from .internal import InternalAuthProvider

try:
    from .jwt import JWTAuthProvider
    __all__ = ['AuthProvider', 'InternalAuthProvider', 'JWTAuthProvider']
except ImportError:
    __all__ = ['AuthProvider', 'InternalAuthProvider']
