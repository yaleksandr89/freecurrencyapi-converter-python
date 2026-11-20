# Installation and first run

## Choose language

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](getting-started.md) | **Selected** | [Español](getting-started_es.md) | [中文](getting-started_zh.md) | [Français](getting-started_fr.md) | [Deutsch](getting-started_de.md) |

## Requirements

- Git to clone the repository, Python 3.12 or newer, and the `venv` module with `pip`.
- Your own FreecurrencyAPI key for conversions. Register with the service and obtain a key from your account. The [FreecurrencyAPI documentation](https://freecurrencyapi.com/docs/) describes the API.

## Get the source code

Clone the repository and enter its root directory containing `index.py`. Run all subsequent commands from that directory.

```bash
# Clone the project and enter its directory.
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

## Install dependencies

### Linux and macOS

Verify that `python3` resolves to Python 3.12 or newer and that `make` is installed. `make setup` creates `.venv` if it does not exist and installs the application and development dependencies.

```bash
# Check that Python 3.12 or newer is available.
python3 --version

# Create .venv and install development dependencies.
make setup

# Create the local configuration without overwriting an existing API key.
cp -n .env.example .env
```

If a suitable interpreter has a different name, supply `PYTHON`, for example `make setup PYTHON=python3.12`. This variable is only used when creating the environment.

### Windows PowerShell

In this example, `python` is Python 3.12 or newer available on `PATH`. Commands invoke the interpreter in `.venv` directly; activation and `make` are not required.

```powershell
# Check the installed Python version.
python --version

# Create the virtual environment and install development dependencies.
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

# Copy .env.example only if .env does not already exist.
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

To install only the application and its runtime dependencies, use `requirements.txt` instead of `requirements-dev.txt` in the `pip install` command. Development dependencies are required for local checks.

## Configure the API key and address

Open the new `.env` file in an editor. Replace `API_TOKEN` with your key. Keep `API_URL` as the API base address, without an endpoint path.

```ini
API_TOKEN=your_api_token_here
API_URL=https://api.freecurrencyapi.com/v1
```

Keep your key local. Do not commit `.env` or include it in bug reports. Environment variables already set in the process take precedence over values loaded from `.env`.

## Run and verify

On Linux and macOS, run the converter using `make`:

```bash
# Russian interface (default).
make run

# English interface.
make run CLI_LANG=en
```

On Windows PowerShell, run `index.py` with the Python interpreter from the virtual environment:

```powershell
# Russian interface (default).
.\.venv\Scripts\python.exe index.py

# English interface.
.\.venv\Scripts\python.exe index.py --lang en
```

After the greeting, the converter displays the currency list. If it includes `USD`, `EUR`, and `GBP`, enter `USD`, `12.5`, and `EUR,GBP`, pressing Enter after each value. On success, the CLI prints a line for each target currency. The numbers depend on the current rates.

To verify that the CLI starts without an API key or API request, use the help option: `.venv/bin/python index.py --help` on Linux/macOS or `.\.venv\Scripts\python.exe index.py --help` in PowerShell.

## If the application does not start

| Symptom | What to check |
| --- | --- |
| `API_TOKEN` or `API_URL` is missing | Check the `.env` filename, variable names, and nonempty values. Also check any values already set in the shell. |
| An HTTP status error | Check the base URL, key validity, and remaining FreecurrencyAPI request quota. |
| Timeout or request failure | Check `API_URL` and the availability of FreecurrencyAPI. |
| CLI rejects input | Restart the converter, choose codes from the displayed list, separate target currencies with commas, and enter a positive amount with a decimal point. |

For error categories and exit codes, see the [CLI and errors reference](../reference/cli-and-errors_en.md).

## Local checks

After installing development dependencies, check the project from the repository root.

On Linux and macOS:

```bash
# Run tests, Ruff, and installed-dependency checks.
make check
```

On Windows PowerShell:

```powershell
# Offline tests.
.\.venv\Scripts\python.exe -m pytest

# Linting and formatting.
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .

# Verify installed dependencies.
.\.venv\Scripts\python.exe -m pip check
```

The tests mock FreecurrencyAPI responses and failures and prevent real HTTP requests. They do not need a live key or API response. A real interactive conversion is required to verify access to the service and key validity.
