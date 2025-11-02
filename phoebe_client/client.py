"""Main client library that combines session and PHOEBE operations."""

from typing import Any
from .server_api import SessionAPI, PhoebeAPI
from .auth.base import AuthProvider
from .exceptions import AuthenticationError


class PhoebeClient:
    """Main PHOEBE Client providing unified access."""

    def __init__(self, host: str | None = None, port: int | None = None, auth_provider: AuthProvider | None = None, auto_session: bool = False):
        self.host = host
        self.port = port
        self.auth_provider = auth_provider
        self.jwt_token: str | None = None  # UI authentication token

        self.sessions = SessionAPI(host=host, port=port)
        self.phoebe = PhoebeAPI(host=host, port=port)

        if auto_session:
            self.create_session()

    def authenticate(self, credentials: dict[str, str]) -> 'PhoebeClient':
        """Authenticate UI user via injected provider."""
        if not self.auth_provider:
            raise AuthenticationError("No authentication provider configured")
        self.jwt_token = self.auth_provider.authenticate(credentials)
        # Forward JWT to APIs for identification/auditing on requests
        self.sessions.set_jwt_token(self.jwt_token)
        self.phoebe.set_jwt_token(self.jwt_token)
        return self

    def create_session(self) -> dict[str, Any]:
        response = self.sessions.start_session()
        self.phoebe.set_client_id(response.get('client_id'))
        return response

    def close_session(self):
        if self.phoebe.client_id:
            self.sessions.end_session(self.phoebe.client_id)
            self.phoebe.set_client_id(None)

    def get_parameter(self, twig: str) -> dict[str, Any]:
        return self.phoebe.execute(
            command='get_parameter',
            args={'twig': twig}
        )

    def get_value(self, twig: str | None = None, uniqueid: str | None = None) -> Any:
        return self.phoebe.execute(
            command='get_value',
            args={'twig': twig, 'uniqueid': uniqueid}
        )

    def set_value(self, twig: str | None = None, uniqueid: str | None = None, value=None) -> dict[str, Any]:
        return self.phoebe.execute(
            command='set_value',
            args={'twig': twig, 'uniqueid': uniqueid, 'value': value}
        )

    def add_dataset(self, kind: str | None = None, **kwargs) -> dict[str, Any]:
        return self.phoebe.execute(
            command='add_dataset',
            args={'kind': kind, **kwargs}
        )

    def remove_dataset(self, dataset: str) -> dict[str, Any]:
        return self.phoebe.execute(
            command='remove_dataset',
            args={'dataset': dataset}
        )

    def run_compute(self, **kwargs) -> dict[str, Any]:
        return self.phoebe.execute(
            command='run_compute',
            args=kwargs
        )

    def run_solver(self, **kwargs) -> dict[str, Any]:
        return self.phoebe.execute(
            command='run_solver',
            args=kwargs
        )

    def load_bundle(self, bundle: str) -> dict[str, Any]:
        return self.phoebe.execute(
            command='load_bundle',
            args={'bundle': bundle}
        )

    def save_bundle(self) -> dict[str, Any]:
        return self.phoebe.execute(
            command='save_bundle',
            args={}
        )

    def __enter__(self):
        if not self.phoebe.client_id:
            self.create_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()
