"""Russian and English text for the command-line interface."""

_MESSAGES = {
    "welcome": (
        "Приветствуем Вас в нашем Конвертере валют! 🌍💱",
        "Welcome to our currency converter! 🌍💱",
    ),
    "instructions": (
        "\n"
        "    Наш конвертер поможет вам быстро и легко перевести валюту!\n"
        "    Вот как это работает:\n"
        "    1. Вы выбираете валюту, которую хотите конвертировать.\n"
        "    2. Вводите количество валюты.\n"
        "    3. Указываете валюты, в которые хотите конвертировать.\n\n"
        "    Готовы? Давайте начнем! 😊\n",
        "\n"
        "    1. Choose the currency you want to convert.\n"
        "    2. Enter the amount.\n"
        "    3. Choose the currencies to convert to.\n",
    ),
    "source_prompt": (
        "\nВведите валюту, которую у вас есть (например, RUB): ",
        "\nEnter the currency you have (for example, RUB): ",
    ),
    "amount_prompt": (
        "Введите количество этой валюты: ",
        "Enter the amount in that currency: ",
    ),
    "targets_prompt": (
        "Введите валюту(-ы), в которые хотите конвертировать "
        "(например, USD или USD,EUR): ",
        "Enter the currencies to convert to (for example, USD or USD,EUR): ",
    ),
    "source_invalid": (
        "Выберите исходную валюту из списка.",
        "Choose a source currency from the list.",
    ),
    "amount_parse": (
        "Введите количество числом, например 12.5.",
        "Enter a number such as 12.5.",
    ),
    "amount_invalid": (
        "Количество должно быть конечным положительным числом.",
        "The amount must be a finite positive number.",
    ),
    "amount_zero": (
        "Количество округляется до нуля с точностью до трёх знаков.",
        "The amount rounds to zero at three decimal places.",
    ),
    "amount_overflow": (
        "Сумма слишком велика для конвертации.",
        "The amount is too large to convert.",
    ),
    "targets_invalid": (
        "Укажите валюты из списка через запятую.",
        "Enter currencies from the list separated by commas.",
    ),
    "missing_variable": (
        "Отсутствует обязательная переменная окружения: {variable}",
        "Required environment variable is missing: {variable}",
    ),
    "timeout": (
        "Превышено время ожидания ответа API.",
        "The API request timed out.",
    ),
    "request_failed": (
        "Не удалось выполнить запрос к API.",
        "Could not complete the API request.",
    ),
    "http_status": ("Ошибка сервера: HTTP {status}.", "Server error: HTTP {status}."),
    "invalid_json": ("API вернул некорректный JSON.", "The API returned invalid JSON."),
    "invalid_response": (
        "Некорректный формат ответа от API.",
        "The API response has an invalid format.",
    ),
    "missing_rates": (
        "API вернул курсы для неполного списка валют.",
        "The API returned rates for an incomplete list of currencies.",
    ),
    "invalid_rate": (
        "API вернул некорректное значение курса.",
        "The API returned an invalid exchange rate.",
    ),
    "invalid_currencies": (
        "API вернул некорректный список валют.",
        "The API returned an invalid currency list.",
    ),
    "error": ("Ошибка: {message}", "Error: {message}"),
    "eof": (
        "\nВвод завершён до получения всех данных.",
        "\nInput ended before all values were entered.",
    ),
    "interrupt": ("\nКонвертация отменена.", "\nConversion cancelled."),
    "results": ("\nРезультаты конвертации:", "\nConversion results:"),
    "usage": (
        "Использование: python index.py [-h] [--lang {ru,en}]",
        "Usage: python index.py [-h] [--lang {ru,en}]",
    ),
    "help": (
        "Интерактивный конвертер валют.\n\n"
        "  -h, --help       Показать справку.\n"
        "  --lang {ru,en}   Язык интерфейса (по умолчанию ru).",
        "Interactive currency converter.\n\n"
        "  -h, --help       Show this help.\n"
        "  --lang {ru,en}   Interface language (default: ru).",
    ),
    "invalid_args": (
        "Некорректные аргументы. Используйте --help для справки.",
        "Invalid arguments. Use --help for details.",
    ),
    "invalid_lang": (
        "Для --lang укажите ru или en.",
        "Use ru or en with --lang.",
    ),
}


def translate(lang: str, key: str, **values: object) -> str:
    """Return the selected UI text."""
    template = _MESSAGES[key][lang == "en"]
    return template.format(**values) if values else template
