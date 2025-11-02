"""Base authentication provider interface."""

from abc import ABC, abstractmethod


class AuthProvider(ABC):
    """Abstract authentication provider interface."""
    
    @abstractmethod
    def authenticate(self, credentials: dict[str, str]) -> str:
        """Authenticate and return token.
        
        Args:
            credentials: Auth credentials, typically {"token": "..."} for JWT
                        or {"username": "...", "password": "..."} for internal auth.
        """
        pass
    
    @abstractmethod
    def validate_token(self, token: str) -> dict[str, str]:
        """Validate token and return user info (e.g., username, roles)."""
        pass
