# Currency Converter

[![Source Code](https://img.shields.io/badge/source-yaleksandr89%2Ffreecurrencyapi--converter--python-blue.svg?style=flat-square)](https://github.com/yaleksandr89/freecurrencyapi-converter-python)
[![CI](https://github.com/yaleksandr89/freecurrencyapi-converter-python/actions/workflows/ci.yml/badge.svg)](https://github.com/yaleksandr89/freecurrencyapi-converter-python/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white)](../../pyproject.toml)
[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](../../LICENSE.md)

![Currency Converter — interactive Python currency converter](../assets/currency-converter-readme-cover.png)

## Choose language

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../README.md) | **Selected** | [Español](README_es.md) | [中文](README_zh.md) | [Français](README_fr.md) | [Deutsch](README_de.md) |

An interactive Python CLI that converts an amount from one currency into one or several others using FreecurrencyAPI exchange rates. Input and results appear in the terminal.

- The list of available currencies is retrieved at the beginning of each interactive run.
- Rates are requested for the selected currencies after input validation.
- Prompts and messages are available in Russian and English.

Python 3.12 or newer and your own FreecurrencyAPI key are required. The commands below target Linux and macOS with `make`. CI runs on Ubuntu with Python 3.12, 3.13, and 3.14.

## How conversion works

Enter the source currency, amount, and target currencies. The converter fetches the selected rates and prints the results in the terminal.

```mermaid
flowchart LR
    A["Load currency list"] --> B["Read and validate input"]
    B --> C["Fetch exchange rates"]
    C --> D["Calculate and display amounts"]
```

For module responsibilities, API requests, and error paths, see the [architecture overview](../reference/architecture_en.md).

## Quick start

Clone the repository, create the virtual environment with its dependencies, and copy the configuration example.

```bash
# Clone the repository and enter its directory.
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python

# Create .venv and install development dependencies.
make setup

# Copy the configuration example without overwriting an existing .env.
cp -n .env.example .env
```

Put the key from your FreecurrencyAPI account into `API_TOKEN` in `.env`. The example already contains the `API_URL` base address. Run either command from the repository root.

```bash
# Russian interface.
make run

# English interface.
make run CLI_LANG=en
```

For Windows PowerShell installation and execution, see the [getting started guide](../guides/getting-started_en.md). CLI options, input rules, and exit codes are documented in the [CLI reference](../reference/cli-and-errors_en.md).

## Demonstrations

### Successful conversion

Amount conversion and output.

https://github.com/user-attachments/assets/47d64727-342d-4cb8-ba4c-d223253b2338

### Conversion error

An error reported by the converter.

https://github.com/user-attachments/assets/5b0408fb-e59c-467a-bef5-72b7e30c066b

### Switching the interface language

Starting the CLI with a different language for prompts and messages.

https://github.com/user-attachments/assets/217d4e51-7e09-460e-a6be-c7712ecb7b0f

## Feedback

- Report a bug or suggest an improvement — [GitHub Issues](https://github.com/yaleksandr89/freecurrencyapi-converter-python/issues).
- Discuss using the converter — [GitHub Discussions](https://github.com/yaleksandr89/freecurrencyapi-converter-python/discussions).

---

<p align="center">
  If this project was useful, give it a star on GitHub so others can find it more easily. 🤘
</p>
