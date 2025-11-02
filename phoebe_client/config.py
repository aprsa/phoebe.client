"""
Configuration loader for PHOEBE Client.
"""

from dataclasses import dataclass
from pathlib import Path
import tomllib

# Hardcoded defaults
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8001
DEFAULT_TIMEOUT = 30

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.toml"


@dataclass(frozen=True)
class ServerConfig:
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    timeout: int = DEFAULT_TIMEOUT

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


@dataclass(frozen=True)
class AuthConfig:
    api_key: str = ""


@dataclass(frozen=True)
class AppConfig:
    server: ServerConfig = ServerConfig()
    auth: AuthConfig = AuthConfig()


def _load_config_file() -> AppConfig:
    if CONFIG_PATH.exists():
        try:
            with CONFIG_PATH.open("rb") as f:
                data = tomllib.load(f)
        except Exception:
            data = {}
    else:
        data = {}

    server_data = data.get("server", {}) if isinstance(data, dict) else {}
    auth_data = data.get("auth", {}) if isinstance(data, dict) else {}

    server = ServerConfig(
        host=str(server_data.get("host", DEFAULT_HOST)),
        port=int(server_data.get("port", DEFAULT_PORT)),
        timeout=int(server_data.get("timeout", DEFAULT_TIMEOUT)),
    )
    auth = AuthConfig(api_key=str(auth_data.get("api_key", "")))
    return AppConfig(server=server, auth=auth)


# Loaded at import and treated as read-only configuration
CONFIG: AppConfig = _load_config_file()
