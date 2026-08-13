"""Python client for Pepkio ligo-ratio-calc tool."""

from __future__ import annotations

from .client import PepkioClient
from .config import DEFAULT_API_BASE_URL, TOOL_ID
from .exceptions import PepkioAPIError, PepkioAuthError, PepkioHTTPError, PepkioRunError
from .models import RunOptions, RunResult

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_API_BASE_URL",
    "TOOL_ID",
    "PepkioAPIError",
    "PepkioAuthError",
    "PepkioClient",
    "PepkioHTTPError",
    "PepkioRunError",
    "RunOptions",
    "RunResult",
    "__version__",
]
