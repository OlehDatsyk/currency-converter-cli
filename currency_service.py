"""
currency_service.py
====================
Service layer responsible for talking to the exchange rate provider
(ExchangeRate-API.com) and turning its responses into clean, typed
Python objects.

This module knows nothing about the terminal, Rich, or user input —
that separation of concerns is what makes it easy to test and easy to
swap out for a different provider later.
"""

from __future__ import annotations

from dataclasses import dataclass

import requests

from config import Settings
from utils import unix_timestamp_to_readable


# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class CurrencyServiceError(Exception):
    """Base class for all errors raised by the currency service."""


class InvalidCurrencyError(CurrencyServiceError):
    """Raised when the API reports that a currency code is unsupported."""


class APIError(CurrencyServiceError):
    """Raised when the API responds but reports a non-recoverable error."""


class NetworkError(CurrencyServiceError):
    """Raised when the API cannot be reached at all (timeout, DNS, etc.)."""


class RateLimitError(CurrencyServiceError):
    """Raised when the API reports that the request quota was exceeded."""


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class ConversionResult:
    """
    Immutable result of a currency conversion.

    Attributes:
        source_currency: ISO currency code converted from, e.g. "USD".
        target_currency: ISO currency code converted to, e.g. "EUR".
        amount: The original amount that was converted.
        exchange_rate: The exchange rate used (1 source unit = rate target units).
        converted_amount: The resulting amount in the target currency.
        last_updated: Human-readable timestamp of when the rate was last updated.
    """

    source_currency: str
    target_currency: str
    amount: float
    exchange_rate: float
    converted_amount: float
    last_updated: str


# --------------------------------------------------------------------------- #
# Service
# --------------------------------------------------------------------------- #

class CurrencyService:
    """
    Encapsulates all communication with the ExchangeRate-API pair-conversion
    endpoint: `GET {base_url}/{api_key}/pair/{from}/{to}/{amount}`.
    """

    def __init__(self, settings: Settings, session: requests.Session | None = None) -> None:
        """
        Args:
            settings: Application settings (API key, base URL, timeout).
            session: Optional pre-configured requests.Session, useful for
                testing (dependency injection) or connection pooling.
        """
        self._settings = settings
        self._session = session or requests.Session()

    def convert(self, source_currency: str, target_currency: str, amount: float) -> ConversionResult:
        """
        Convert `amount` from `source_currency` to `target_currency` using
        live exchange rates.

        Args:
            source_currency: 3-letter ISO currency code, already normalized.
            target_currency: 3-letter ISO currency code, already normalized.
            amount: Positive amount to convert.

        Returns:
            A populated ConversionResult.

        Raises:
            InvalidCurrencyError: If either currency code is not supported.
            RateLimitError: If the API quota has been exceeded.
            APIError: For other API-reported errors (bad key, inactive
                account, malformed request, unexpected payload shape, etc.).
            NetworkError: If the request times out or the network is
                unreachable.
        """
        url = (
            f"{self._settings.api_base_url}/{self._settings.api_key}/pair/"
            f"{source_currency}/{target_currency}/{amount}"
        )

        payload = self._perform_request(url)
        self._raise_for_api_result(payload, source_currency, target_currency)

        try:
            exchange_rate = float(payload["conversion_rate"])
            converted_amount = float(payload["conversion_result"])
            last_updated_unix = payload.get("time_last_update_unix")
        except (KeyError, TypeError, ValueError) as exc:
            raise APIError(
                "The API returned an unexpected response format. "
                "This usually means the provider changed its API contract."
            ) from exc

        return ConversionResult(
            source_currency=source_currency,
            target_currency=target_currency,
            amount=amount,
            exchange_rate=exchange_rate,
            converted_amount=converted_amount,
            last_updated=unix_timestamp_to_readable(last_updated_unix),
        )

    # ------------------------------------------------------------------- #
    # Internal helpers
    # ------------------------------------------------------------------- #

    def _perform_request(self, url: str) -> dict:
        """
        Execute the HTTP GET request and return the parsed JSON body.

        Raises:
            NetworkError: On timeout, connection failure, or invalid JSON.
        """
        try:
            response = self._session.get(url, timeout=self._settings.request_timeout)
        except requests.exceptions.Timeout as exc:
            raise NetworkError(
                "The request to the exchange rate service timed out. "
                "Please check your internet connection and try again."
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise NetworkError(
                "Could not connect to the exchange rate service. "
                "Please check your internet connection and try again."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise NetworkError(f"An unexpected network error occurred: {exc}") from exc

        try:
            return response.json()
        except ValueError as exc:
            raise APIError(
                f"The API returned a non-JSON response (HTTP {response.status_code})."
            ) from exc

    @staticmethod
    def _raise_for_api_result(payload: dict, source_currency: str, target_currency: str) -> None:
        """
        Inspect the API's own `result` / `error-type` fields and raise the
        appropriate exception if the request was not successful.

        The ExchangeRate-API contract: a successful response has
        `"result": "success"`. A failed response has `"result": "error"`
        and an `"error-type"` field describing what went wrong.
        """
        result = payload.get("result")

        if result == "success":
            return

        error_type = payload.get("error-type", "unknown-error")

        if error_type == "unsupported-code":
            raise InvalidCurrencyError(
                f"Currency code not supported by the API: "
                f"'{source_currency}' or '{target_currency}'. "
                "Please double-check the ISO 4217 currency codes (e.g. USD, EUR, GBP)."
            )
        if error_type == "malformed-request":
            raise APIError(
                "The request was malformed. Please verify the currency "
                "codes and amount are valid."
            )
        if error_type == "invalid-key":
            raise APIError(
                "The configured API key is invalid. Please check the "
                "EXCHANGE_RATE_API_KEY value in your .env file."
            )
        if error_type == "inactive-account":
            raise APIError(
                "The API account is inactive. Please confirm your email "
                "address with the exchange rate provider."
            )
        if error_type == "quota-reached":
            raise RateLimitError(
                "The API request quota has been reached for this billing "
                "period. Please try again later or upgrade your plan."
            )

        raise APIError(f"The API reported an error: '{error_type}'.")
