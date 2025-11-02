"""Server API clients for PHOEBE backend communication.

This module consolidates all HTTP communication with the phoebe-server:
- BaseAPI: Shared connection plumbing (host/port/timeout, base_url, X-API-Key headers)
- SessionAPI: Session lifecycle management (start/end sessions, memory/port status)
- PhoebeAPI: PHOEBE command execution via unified execute() method
"""

import requests
from typing import Any

from .config import CONFIG, ServerConfig
from .exceptions import SessionError, CommandError
from .utils.serialization import make_json_serializable


class BaseAPI:
    """Base class for server API clients.

    Provides common server connection handling (host/port/timeout), base_url property,
    and headers with X-API-Key from config.toml.
    """

    def __init__(self, host: str | None = None, port: int | None = None, timeout: int | None = None):
        cfg: ServerConfig = CONFIG.server
        self._host = host or cfg.host
        self._port = port or cfg.port
        self._timeout = timeout or cfg.timeout
        self._jwt_token: str | None = None  # optional per-request user identity token (not for authorization)

    @property
    def base_url(self) -> str:
        return f"http://{self._host}:{self._port}"

    def set_jwt_token(self, token: str | None) -> None:
        """Set or clear the JWT used for user identification.

        Note: Server authorization remains based on X-API-Key; JWT is forwarded
        only for user identification/auditing and optional session tagging.
        """
        self._jwt_token = token

    def _get_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if CONFIG.auth.api_key:
            headers["X-API-Key"] = CONFIG.auth.api_key
        if self._jwt_token:
            headers["Authorization"] = f"Bearer {self._jwt_token}"
        return headers


class SessionAPI(BaseAPI):
    """API client for PHOEBE session management.

    Manages backend session lifecycle: start/end sessions, query memory usage,
    and port status. Uses X-API-Key from config for server authentication.
    """

    def __init__(self, host: str | None = None, port: int | None = None, timeout: int | None = None):
        super().__init__(host=host, port=port, timeout=timeout)

    def _request(self, method: str, endpoint: str, **kwargs) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method,
                url,
                headers=self._get_headers(),
                timeout=self._timeout,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status in (401, 403):
                raise SessionError(
                    f"Server authentication failed (status {status}). Check API key in config.toml."
                ) from e
            raise SessionError(f"Request failed: {e}") from e
        except requests.RequestException as e:
            raise SessionError(f"Request failed: {e}") from e

    def get_sessions(self) -> dict[str, Any]:
        return self._request("GET", "/dash/sessions")

    def start_session(self) -> dict[str, Any]:
        return self._request("POST", "/dash/start-session")

    def end_session(self, client_id: str) -> dict[str, Any]:
        return self._request("POST", f"/dash/end-session/{client_id}")

    def update_user_info(self, client_id: str, first_name: str, last_name: str):
        return self._request(
            "POST",
            f"/dash/update-user-info/{client_id}",
            json={"first_name": first_name, "last_name": last_name},
        )

    def get_memory_usage(self) -> dict[str, Any]:
        return self._request("GET", "/dash/session-memory")

    def get_port_status(self) -> dict[str, Any]:
        return self._request("GET", "/dash/port-status")


class PhoebeAPI(BaseAPI):
    """API client for PHOEBE parameter operations.

    Executes PHOEBE commands via unified execute() method, which POSTs to
    /send/{client_id} with JSON payload. All commands flow through this
    single endpoint with server-side PHOEBE Bundle method dispatch.
    """

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        timeout: int | None = None,
        client_id: str | None = None,
    ):
        super().__init__(host=host, port=port, timeout=timeout)
        self.client_id = client_id

    def set_client_id(self, client_id: str | None):
        self.client_id = client_id

    def execute(self, command: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.client_id:
            raise ValueError("No client ID set. Call set_client_id() first.")

        payload: dict[str, Any] = {**(args or {}), "command": command}

        try:
            response = requests.post(
                f"{self.base_url}/send/{self.client_id}",
                json=make_json_serializable(payload),
                headers=self._get_headers(),
                timeout=self._timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status in (401, 403):
                raise CommandError(
                    f"Server authentication failed (status {status}). Check API key in config.toml."
                ) from e
            raise CommandError(f"Command failed: {e}") from e
        except requests.RequestException as e:
            raise CommandError(f"Command failed: {e}") from e
