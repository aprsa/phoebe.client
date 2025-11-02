"""JWT authentication provider."""

from .base import AuthProvider
from ..exceptions import AuthenticationError

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False


class JWTAuthProvider(AuthProvider):
    """External JWT authentication provider."""

    def __init__(
        self,
        public_key: str,
        issuer: str,
        audience: str,
        algorithms: list[str] | None = None,
        token_url: str | None = None,
    ):
        if not JWT_AVAILABLE:
            raise ImportError("PyJWT required. Install: pip install pyjwt")

        self.public_key = public_key
        self.issuer = issuer
        self.audience = audience
        self.algorithms = algorithms or ['RS256']
        self.token_url = token_url

    def authenticate(self, credentials: dict[str, str]) -> str:
        if 'token' in credentials:
            token = credentials['token']
            self.validate_token(token)
            return token

        if self.token_url:
            import requests
            try:
                response = requests.post(self.token_url, json=credentials)
                response.raise_for_status()
                data = response.json()
                return data.get('access_token') or data.get('token')
            except requests.RequestException as e:
                raise AuthenticationError(f"Failed to obtain token: {e}")

        raise AuthenticationError("No token provided and no token_url configured")

    def validate_token(self, token: str) -> dict[str, str]:
        try:
            claims = jwt.decode(
                token,
                self.public_key,
                algorithms=self.algorithms,
                issuer=self.issuer,
                audience=self.audience,
            )
            # Return string-only dict for base class contract
            return {
                'user_id': str(claims.get('sub', '')),
                'username': str(claims.get('preferred_username', '')),
                'email': str(claims.get('email', '')),
            }
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid JWT token: {e}")
