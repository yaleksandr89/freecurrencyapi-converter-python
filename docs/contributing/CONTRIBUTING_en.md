# Contributing

## Choose language

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../.github/CONTRIBUTING.md) | **Selected** | [Español](CONTRIBUTING_es.md) | [中文](CONTRIBUTING_zh.md) | [Français](CONTRIBUTING_fr.md) | [Deutsch](CONTRIBUTING_de.md) |

## Before you start

Check whether your change is already being discussed. To open a [new issue](https://github.com/yaleksandr89/freecurrencyapi-converter-python/issues/new/choose), choose the bug report or feature request form.

- For bugs, include the environment, command, input data, reproduction steps, and expected and actual output.
- For feature requests, describe the problem and expected CLI behavior.
- Report vulnerabilities using the [security policy](../security/SECURITY_en.md).

## Branches and commits

Create a separate branch from `master`, for example `fix/invalid-amount` or `docs/setup-guide`. Use Conventional Commits for commits and pull request titles, with an English type prefix and a **Russian-language description**.

```text
docs: уточнить запуск конвертера
fix: отклонять недопустимые суммы
test: проверить обработку некорректных ответов API
```

## Local checks

From the repository root on Linux or macOS, with Python 3.12 or newer, run the following commands. `make setup` creates `.venv` if needed and installs development dependencies. Use `PYTHON` to select the interpreter when creating the environment.

```bash
make setup PYTHON=python3
make check
```

`make check` runs pytest, Ruff linting and formatting checks, and `pip check`. Tests mock FreecurrencyAPI responses and do not require a live API key. PowerShell commands are described in the [getting started guide](../guides/getting-started_en.md#local-checks).

Do not commit `.env`, real API keys, or logs containing secrets.

## Pull requests

Open a pull request targeting `master`. Describe the reason for the change, completed checks, and any impact on CLI behavior, FreecurrencyAPI requests, or secret handling. Update tests and documentation when relevant.
