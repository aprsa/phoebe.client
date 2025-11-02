"""Internal authentication provider."""

from typing import Dict, Any
from .base import AuthProvider
from ..exceptions import AuthenticationError


class InternalAuthProvider(AuthProvider):
    """Built-in authentication provider."""
    
    def __init__(self, api_url: str):
        self.api_url = api_url
    
    def authenticate(self, credentials: Dict[str, Any]) -> str:
        import requests
        
        username = credentials.get('username')
        password = credentials.get('password')
        
        if not username or not password:
            raise AuthenticationError("Username and password required")
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                json={"username": username, "password": password}
            )
            response.raise_for_status()
            return response.json().get('token')
        except requests.RequestException as e:
            raise AuthenticationError(f"Authentication failed: {e}")
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        import requests
        
        try:
            response = requests.get(
                f"{self.api_url}/auth/validate",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise AuthenticationError(f"Token validation failed: {e}")
