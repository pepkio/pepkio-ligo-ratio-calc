"""API error types for Pepkio Tools."""

from __future__ import annotations

from typing import Any


class PepkioAPIError(Exception):
    """Raised when the Pepkio Tools API returns an error or a run fails."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}
        self.response_body = response_body

    def __str__(self) -> str:
        parts = [self.message]
        if self.code:
            parts.append(f"code={self.code}")
        if self.status_code is not None:
            parts.append(f"status={self.status_code}")
        return " ".join(parts)


class PepkioAuthError(PepkioAPIError):
    """Raised when authentication fails (HTTP 401/403 or invalid API key)."""


class PepkioHTTPError(PepkioAPIError):
    """Raised when an HTTP 4xx or 5xx error occurs."""


class PepkioRunError(PepkioAPIError):
    """Raised when a tool execution returns an error status or body."""
