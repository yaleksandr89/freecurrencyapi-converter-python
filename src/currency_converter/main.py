"""Interactive prompts and output for the currency converter."""

import argparse
import sys
from collections.abc import Sequence
from functools import partial

from dotenv import load_dotenv

from .api_service import (
    AmountError,
    CurrencyAPIError,
    fetch_currency_rates,
    get_all_currencies,
    normalize_amount,
)
from .i18n import translate


class InputError(ValueError):
    """Invalid input identified by a translation key."""


def main(argv: Sequence[str] | None = None) -> int:
    """Parse CLI options before loading configuration or calling the API."""
    parser = argparse.ArgumentParser(
        add_help=False, allow_abbrev=False, exit_on_error=False
    )
    parser.add_argument("--lang", default="ru")
    parser.add_argument("-h", "--help", action="store_true")
    options = argparse.Namespace(lang="ru")
    try:
        options, extras = parser.parse_known_args(argv, namespace=options)
    except argparse.ArgumentError:
        print(translate(options.lang, "invalid_lang"), file=sys.stderr)
        return 2

    lang = options.lang
    if lang not in ("ru", "en"):
        print(translate("ru", "invalid_lang"), file=sys.stderr)
        return 2
    if extras:
        print(translate(lang, "invalid_args"), file=sys.stderr)
        return 2
    if options.help:
        print(translate(lang, "usage"))
        print()
        print(translate(lang, "help"))
        return 0
    return start_converter(lang)


def start_converter(lang: str = "ru") -> int:
    """Return 0 on success, 1 on error, and 130 on interrupt."""
    message = partial(translate, lang)

    try:
        load_dotenv()
        print(message("welcome"))
        print(message("instructions"))
        all_currencies = get_all_currencies()
        for count, (code, metadata) in enumerate(all_currencies.items(), start=1):
            print(f"{count}. [{code}] {metadata['name']}")

        if sys.stdin is not None and sys.stdin.isatty():
            try:
                import readline  # noqa: F401 - enables terminal line editing
            except ImportError:
                pass

        user_currency = input(message("source_prompt")).strip().upper()
        if user_currency not in all_currencies:
            raise InputError("source_invalid")

        raw_amount = input(message("amount_prompt")).strip()
        try:
            current_amount = float(raw_amount)
        except ValueError:
            raise InputError("amount_parse") from None
        current_amount = normalize_amount(current_amount)

        targets = input(message("targets_prompt"))
        conversion_currencies = [code.strip().upper() for code in targets.split(",")]
        if any(code not in all_currencies for code in conversion_currencies):
            raise InputError("targets_invalid")

        currency_rates = fetch_currency_rates(
            user_currency, conversion_currencies, current_amount
        )
    except (CurrencyAPIError, AmountError, InputError) as error:
        if isinstance(error, CurrencyAPIError):
            detail = message(error.code, **error.details)
        else:
            detail = message(str(error))
        print(message("error", message=detail), file=sys.stderr)
        return 1
    except EOFError:
        print(message("eof"), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(message("interrupt"), file=sys.stderr)
        return 130

    print(message("results"))
    for currency, rate in currency_rates.items():
        print(f"{current_amount} {user_currency} = {rate:.2f} {currency}")
    return 0
