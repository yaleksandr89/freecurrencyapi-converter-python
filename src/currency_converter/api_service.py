"""Exchange rates and currency metadata from FreecurrencyAPI."""

import math
import os
from collections.abc import Sequence
from typing import TypedDict, cast

import requests

# Connection and response read timeouts, in seconds.
HTTP_TIMEOUT = (4, 10)


class CurrencyMetadata(TypedDict):
    """Validated fields used from the API's currency metadata."""

    name: str


class CurrencyAPIError(Exception):
    """An API failure identified by a stable code and safe details."""

    def __init__(self, code: str, **details: object) -> None:
        super().__init__(code)
        self.code = code
        self.details = details


class AmountError(ValueError):
    """An invalid amount identified by a stable code."""


def get_environment_variable(var_name: str) -> str:
    """Return a stripped environment value or raise CurrencyAPIError if blank."""
    value = os.getenv(var_name, "").strip()
    if not value:
        raise CurrencyAPIError("missing_variable", variable=var_name)
    return value


def _fetch_data(endpoint: str, params: dict[str, str]) -> dict[str, object]:
    """Return the non-empty data object from a successful API response."""
    token = get_environment_variable("API_TOKEN")
    url = get_environment_variable("API_URL").rstrip("/")
    try:
        response = requests.get(
            f"{url}/{endpoint}",
            params={**params, "apikey": token},
            timeout=HTTP_TIMEOUT,
            allow_redirects=False,
        )
    except requests.Timeout:
        raise CurrencyAPIError("timeout") from None
    except requests.RequestException:
        raise CurrencyAPIError("request_failed") from None

    if response.status_code != 200:
        raise CurrencyAPIError("http_status", status=response.status_code)

    try:
        payload = response.json()
    except (ValueError, RecursionError):
        raise CurrencyAPIError("invalid_json") from None

    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict) or not data:
        raise CurrencyAPIError("invalid_response")
    return data


def _is_positive_number(value: object) -> bool:
    """Check whether a value can be represented as a positive finite float."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value) and value > 0
    except OverflowError:
        return False


def normalize_amount(amount: float) -> float:
    """Return the positive amount used for conversion."""
    if not _is_positive_number(amount):
        raise AmountError("amount_invalid")

    rounded_amount = round(float(amount), 3)
    if rounded_amount == 0:
        raise AmountError("amount_zero")
    return rounded_amount


def fetch_currency_rates(
    base_currency: str = "USD",
    currencies: Sequence[str] | None = None,
    amount: float = 1.0,
) -> dict[str, float]:
    """Return converted amounts after rounding the input to three decimal places.

    If target currencies are provided, return exactly those currencies.
    Raise ValueError for an invalid amount, including one that rounds to zero.
    Raise CurrencyAPIError if the request fails or the response is invalid.
    """
    rounded_amount = normalize_amount(amount)

    params = {"base_currency": base_currency}
    if currencies:
        params["currencies"] = ",".join(currencies)

    rates = _fetch_data("latest", params)
    requested = set(currencies or ())
    if not requested.issubset(rates):
        raise CurrencyAPIError("missing_rates")

    adjusted_rates = {}
    for currency, rate in rates.items():
        if requested and currency not in requested:
            continue
        if not isinstance(rate, (int, float)) or not _is_positive_number(rate):
            raise CurrencyAPIError("invalid_rate")
        adjusted_rate = rate * rounded_amount
        if not math.isfinite(adjusted_rate):
            raise AmountError("amount_overflow")
        adjusted_rates[currency] = adjusted_rate
    return adjusted_rates


def get_all_currencies() -> dict[str, CurrencyMetadata]:
    """Return metadata keyed by currency code, with a non-empty name for each code.

    Raise CurrencyAPIError if the list cannot be fetched or validated.
    """
    currencies = {}
    for code, metadata in _fetch_data("currencies", {}).items():
        if not isinstance(metadata, dict):
            raise CurrencyAPIError("invalid_currencies")
        name = metadata.get("name")
        if not isinstance(name, str) or not name.strip():
            raise CurrencyAPIError("invalid_currencies")
        currencies[code] = cast(CurrencyMetadata, metadata)
    return currencies


def get_currency_codes() -> list[str]:
    """Return currency codes in API response order, or raise CurrencyAPIError."""
    return list(get_all_currencies())
