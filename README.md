# PHOEBE Client

Python Client Library for interacting with PHOEBE backend services.

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)

## Features

- 🚀 **Simple API** - Clean, intuitive interface for PHOEBE operations
- 🔐 **Pluggable Authentication** - Support for JWT and internal auth
- 🔄 **Session Management** - Automatic session lifecycle handling
- 📦 **Type Hints** - Full type annotation support
- ✅ **Well Tested** - Comprehensive test suite

## Installation

```bash
# Basic installation
pip install .

# With development tools
pip install -e .[dev]

# With JWT authentication support
pip install -e .[jwt]

# With all optional dependencies
pip install -e .[all]
```

## Configuration

Create `config.toml` in the project root (already included in this repo) and set your server and API key:

```toml
[server]
host = "localhost"
port = 8001
timeout = 30

[auth]
# API key issued by phoebe-server; sent as X-API-Key header
api_key = "your-api-key"
```

Constructor arguments override config values; if not provided, values from `config.toml` are used, then sensible defaults.

## Quick Start

```python
from phoebe_client import PhoebeClient

# Create client with automatic session management
with PhoebeClient(host="localhost", port=8001) as client:
    # Set parameters
    client.set_value(twig='period@binary', value=1.5)
    client.set_value(twig='teff@primary', value=6000)
    
    # Run computation
    result = client.run_compute()
    print("Computation successful!" if result.get('success') else "Failed")
```

See examples/ directory for more usage patterns.
