"""Client exceptions."""

class PhoebeClientError(Exception):
    """Base exception for PHOEBE Client errors."""
    pass

class AuthenticationError(PhoebeClientError):
    """Authentication-related errors."""
    pass

class SessionError(PhoebeClientError):
    """Session management errors."""
    pass

class CommandError(PhoebeClientError):
    """PHOEBE command execution errors."""
    pass
