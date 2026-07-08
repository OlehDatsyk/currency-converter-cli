"""
utils.py
========
Small, reusable, dependency-light helper functions.

Kept separate from `currency_service.py` and `main.py` so that:
    - Validation logic can be unit tested in isolation.
    - Formatting logic is not duplicated across the codebase.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

# A currency code is exactly 3 uppercase letters (ISO 4217), e.g. USD, EUR.
_CURRENCY_CODE_PATTERN = re.compile(r"^[A-Za-z]{3}$")


class ValidationError(Exception):
    """Raised when user-provided input fails validation."""


def normalize_currency_code(raw_code: str) -> str:
    """
    Normalize and validate a currency code string.

    Args:
        raw_code: User-supplied currency code, e.g. "usd", " EUR ".

    Returns:
        The normalized, uppercase 3-letter currency code, e.g. "USD".

    Raises:
        ValidationError: If the code is empty or not exactly 3 letters.
    """
    if raw_code is None:
        raise ValidationError("Currency code cannot be empty.")

    code = raw_code.strip().upper()

    if not _CURRENCY_CODE_PATTERN.match(code):
        raise ValidationError(
            f"Invalid currency code: '{raw_code}'. "
            "Currency codes must be exactly 3 letters (e.g. USD, EUR, GBP)."
        )

    return code


def parse_amount(raw_amount: str) -> float:
    """
    Parse and validate a monetary amount entered by the user.

    Args:
        raw_amount: User-supplied amount as a string, e.g. "100", "99.95".

    Returns:
        The amount as a positive float.

    Raises:
        ValidationError: If the amount is not a valid positive number.
    """
    if raw_amount is None or raw_amount.strip() == "":
        raise ValidationError("Amount cannot be empty.")

    cleaned = raw_amount.strip().replace(",", "")

    try:
        amount = float(cleaned)
    except ValueError as exc:
        raise ValidationError(
            f"Invalid amount: '{raw_amount}'. Please enter a numeric value, e.g. 100 or 99.95."
        ) from exc

    if amount <= 0:
        raise ValidationError("Amount must be a positive number greater than zero.")

    return amount


def format_money(amount: float) -> str:
    """Format a numeric amount using thousands separators and 2 decimals."""
    return f"{amount:,.2f}"


def unix_timestamp_to_readable(timestamp: int | None) -> str:
    """
    Convert a Unix timestamp (seconds) into a human-readable UTC string.

    Args:
        timestamp: Seconds since the Unix epoch, or None if unavailable.

    Returns:
        A formatted date/time string, or "Unknown" if timestamp is None.
    """
    if timestamp is None:
        return "Unknown"

    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
