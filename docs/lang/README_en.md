# Currency Converter

### Choose Language

| Русский                    | English | Español | 中文 | Français | Deutsch |
|----------------------------|------------|------------|-----------|-------------|----------|
| [Русский](../../README.md) | **Selected** | [Español](README_es.md) | [中文](README_zh.md) | [Français](README_fr.md) | [Deutsch](README_de.md) |

---

**Currency Converter** is a project for working with the currency exchange API. You can request exchange rates, perform conversions, and test functionality through ready-made tests.

---

## Project structure

```plain text
currency-converter/
├── docs/...              # Materials used in README.md
├── src/
│   ├── main.py           # The main file for launching the application
│   ├── api_service.py    # Working with the API (requests and processing)
├── tests/
│   ├── test.py           # Tests to check the functionality
├── index.py              # The entry point for launching the application
├── .env                  # Configuration file (token and URL). It is created independently!
├── .env.example          # Example of a configuration file
├── .gitignore            # Ignored Git files
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation
```

---

## Installation

### 1. Cloning a repository

Clone the project to your local computer:

```bash
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

### 2. Creating a virtual environment

It is recommended to use a virtual environment to isolate dependencies:

```bash
# Creating a virtual environment
python3 -m venv venv

# Virtual Environment activation
source venv/bin/activate  # For Bash/Zsh/Linux/macOS
venv\Scripts\activate     # For Windows
```

### 3. Installing dependencies

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Configuration

1. Rename the `.env.example` file to `.env`:

```bash
mv .env.example .env
```

2. Specify the token and the base API URL in `.env`:

```plaintext
API_TOKEN='ВАШ_API_ТОКЕН'
API_URL='https://api.freecurrencyapi.com/v1'
```

---

## Launch

### 1. Launching the application

Run the project through the file `index.py`:

```bash
python3 index.py
```

---

## Testing

### Running tests

To run the tests, use the file `tests/test.py`:

```bash
python3 tests/test.py
```

This file checks the correctness of the API connection and displays a list of available currencies.

---

## Demonstration of the work

Successful conversion

![currency-convert-result-work-success.png](/docs/img/currency-convert-result-work-success.png)

<details>
<summary>Conversion process (successful conversion (GIF))</summary>

![currency-convert-result-work-success.gif](/docs/img/currency-convert-result-work-success.gif)

</details>

Conversion error

![currency-convert-result-work-error.png](/docs/img/currency-convert-result-work-error.png)

<details>
<summary>Conversion process (error during conversion (GIF))</summary>

![currency-convert-result-work-error.gif](/docs/img/currency-convert-result-work-error.gif)

</details>

---

## Currency Converter in PHP

A PHP project has been created with similar functionality, but with a number of differences:

- Implemented a web interface
- All available service endpoints are described.

Code example: [freecurrencyapi-converter-php](https://github.com/yaleksandr89/freecurrencyapi-converter-php) — Everyone's there, come in! 😄

---

## Notes

1. **Security Token:**
   - Make sure that your API token is specified correctly in `.env`.
   - Never add the `.env` file to the repository.

2. **Recommendations:**
   - Use a virtual environment to isolate dependencies.
   - Update dependencies if necessary via `pip install --upgrade`.