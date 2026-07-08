"""
config.py
=========
Centralized application configuration.

This module is responsible for:
    - Loading environment variables from a `.env` file (via python-dotenv)
    - Exposing typed, validated configuration values to the rest of the app
    - Failing fast (with a clear error message) if required configuration
      is missing, instead of letting the app crash later with a cryptic
      network/API error.

No other module should read `os.environ` directly — everything should go
through this module so configuration stays in one place.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load the .env file (if present) into the process environment.
# This must run before we read any environment variables below.
load_dotenv()


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    """
    Immutable application settings.

    Attributes:
        api_key: Secret API key used to authenticate with the exchange
            rate provider (ExchangeRate-API.com).
        api_base_url: Base URL of the exchange rate provider's REST API.
        request_timeout: Maximum number of seconds to wait for the API
            to respond before treating the call as a network failure.
    """

    api_key: str
    api_base_url: str
    request_timeout: float


def _get_env(name: str, default: str | None = None, required: bool = False) -> str:
    """
    Fetch a single environment variable with optional validation.

    Args:
        name: Name of the environment variable.
        default: Value to use if the variable is not set.
        required: If True, raises ConfigurationError when the variable
            is missing/empty and no default is provided.

    Returns:
        The resolved string value.

    Raises:
        ConfigurationError: If the variable is required but not set.
    """
    value = os.getenv(name, default)
    if required and (value is None or value.strip() == ""):
        raise ConfigurationError(
            f"Missing required environment variable: '{name}'.\n"
            f"Hint: copy '.env.example' to '.env' and fill in your API key."
        )
    return value  # type: ignore[return-value]


def load_settings() -> Settings:
    """
    Build and return a validated Settings instance from environment
    variables.

    Raises:
        ConfigurationError: If any required setting is missing or invalid.
    """
    api_key = _get_env("EXCHANGE_RATE_API_KEY", required=True)

    api_base_url = _get_env(
        "EXCHANGE_RATE_API_BASE_URL",
        default="https://v6.exchangerate-api.com/v6",
    ).rstrip("/")

    timeout_raw = _get_env("REQUEST_TIMEOUT_SECONDS", default="10")
    try:
        request_timeout = float(timeout_raw)
        if request_timeout <= 0:
            raise ValueError
    except ValueError as exc:
        raise ConfigurationError(
            f"REQUEST_TIMEOUT_SECONDS must be a positive number, got: '{timeout_raw}'"
        ) from exc

    return Settings(
        api_key=api_key,
        api_base_url=api_base_url,
        request_timeout=request_timeout,
    )
