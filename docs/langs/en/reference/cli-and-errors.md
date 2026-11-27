# CLI commands, input and errors

## Choose language

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../ru/reference/cli-and-errors.md) | **Selected** | [Español](../../es/reference/cli-and-errors.md) | [中文](../../zh/reference/cli-and-errors.md) | [Français](../../fr/reference/cli-and-errors.md) | [Deutsch](../../de/reference/cli-and-errors.md) |

## Launch options

Run `index.py` from the repository root using the Python interpreter in `.venv`, created during installation. Examples for Linux and macOS:

```bash
# Interactive conversion in Russian.
.venv/bin/python index.py

# English interface.
.venv/bin/python index.py --lang en

# Help without reading .env or calling the API.
.venv/bin/python index.py --help
```

In Windows PowerShell, replace `.venv/bin/python` with `.\.venv\Scripts\python.exe`. Both installation methods are explained in the [getting started guide](../guides/getting-started.md).

| Option | Behavior |
| --- | --- |
| `-h`, `--help` | Displays help in the selected language without reading `.env` or making an API request. |
| `--lang ru` | Selects the Russian interface; this is the default. |
| `--lang en` | Selects the English interface; can be combined with `--help`. |

## Input and result format

The CLI first retrieves and prints the list of currencies. Codes appear in square brackets; currency names come from FreecurrencyAPI.

1. Enter a source currency code from the list, for example `USD`.
2. Enter a positive finite number. Use a decimal point, for example `2.5`. Inputs such as `2,5`, `NaN`, and `inf` are rejected.
3. Enter one or more target currency codes from the list, for example `EUR,GBP`. Empty items, including trailing commas, are invalid.

Currency codes are case-insensitive; spaces around codes are ignored. If the input is invalid, the current run ends; start the command again to retry.

The amount is converted to `float` and rounded with `round` to three decimal places before multiplication by the exchange rate. A value that rounds to zero or a product that overflows the finite range causes an error.

Results are written to standard output, one line per target code in API response order. The rounded source amount is printed without fixed decimal places; the converted amount uses two decimal places. The following example uses test rates, not live rates.

```text
2.5 USD = 2.00 EUR
2.5 USD = 1.25 GBP
```

## FreecurrencyAPI requests

Both endpoints use `GET`, the base URL from `API_URL`, and `API_TOKEN` as the query parameter `apikey`.

| Endpoint | How the CLI uses it |
| --- | --- |
| [`/currencies`](https://freecurrencyapi.com/docs/currencies) | Requests the list before the first input prompt. Requires each currency to have a nonempty name. |
| [`/latest`](https://freecurrencyapi.com/docs/latest) | Requests rates after valid input. Sends the source code as `base_currency` and comma-separated targets as `currencies`. The multiplication by the amount happens locally. |

The client accepts HTTP 200 responses containing a nonempty JSON object named `data`. The connection timeout is 4 seconds; the response-read timeout is 10 seconds. Redirects are disabled. A rate must be present for each requested currency, and only requested rates are used. FreecurrencyAPI determines the available currencies, rates, and quotas.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Conversion succeeded or help was displayed. |
| `1` | Configuration, request, API response, or input failure, including unexpected end of input (EOF). |
| `2` | Invalid CLI arguments, including unknown flags or unsupported `--lang` values. |
| `130` | The user interrupted the interactive session with Ctrl+C. |

## Error messages

Errors are printed to `stderr`. Their language follows `--lang`. An unsupported `--lang` value produces a Russian-language error message.

| Category | Cause |
| --- | --- |
| Configuration | `API_TOKEN` or `API_URL` is missing or contains only whitespace. |
| Network | A timeout or another request error, such as a connection failure. |
| HTTP | The server returned a status other than 200; the CLI prints the status. |
| API response | Malformed JSON; missing, empty, or invalid `data`; invalid currency metadata; missing, nonpositive, nonnumeric, or nonfinite exchange rates for requested currencies. |
| Input | Unknown source or target codes, empty target items, invalid amount, amount rounding to zero, or overflow during calculation. |
| Session end | The input stream ended before all values were entered, or the user pressed Ctrl+C. |
