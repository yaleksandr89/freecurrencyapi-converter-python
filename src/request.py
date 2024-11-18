import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()


def get_environment_variable(var_name):
    """
    Получает переменную окружения. Выбрасывает исключение, если переменной нет.
    """
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Отсутствует обязательная переменная окружения: {var_name}")
    return value


# Глобальные переменные для API
API_TOKEN = get_environment_variable("API_TOKEN")
API_URL = get_environment_variable("API_URL")


def fetch_currency_rates(base_currency="USD", currencies=None, amount=1.0):
    """
    Возвращает последние курсы обмена валют.
    :param base_currency: Валюта-основа (по умолчанию USD).
    :param currencies: Список целевых валют (например: ["EUR", "GBP"]).
    :param amount: Количество валюты для конвертации (дробное число, округляется до 3 знаков).
    :return: Возвращает последние курсы обмена валют относительно базовой (base_currency).
    """
    try:
        # Проверка корректности введенного количества
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Количество должно быть положительным числом.")

        amount = round(amount, 3)

        # Формирование параметров запроса
        latest_endpoint = f"{API_URL}/latest"
        params = {
            "apikey": API_TOKEN,
            "base_currency": base_currency,
        }

        if currencies:
            params["currencies"] = ",".join(currencies)

        # Отправка запроса
        response = requests.get(latest_endpoint, params=params)

        # Проверка ответа
        if response.status_code != 200:
            error_info = response.json()
            error_message = error_info.get("message", "Неизвестная ошибка")
            return {"error": f"Ошибка сервера: {response.status_code}", "message": error_message}

        data = response.json()

        # Проверка содержимого ответа
        if "data" not in data:
            return {"error": "Некорректный формат ответа от API."}

        # Применение количества к курсам
        rates = data["data"]
        adjusted_rates = {currency: rate * amount for currency, rate in rates.items()}

        return adjusted_rates

    except requests.RequestException as e:
        return {"error": f"Ошибка при соединении с API: {e}"}
    except ValueError as e:
        return {"error": str(e)}


# latest_currency_rates = fetch_currency_rates(currencies=["RUB"], amount=100)
# pprint(latest_currency_rates)

def get_all_currencies():
    """
    Получает все поддерживаемые валюты с API freecurrencyapi.com.
    :return: Список поддерживаемых валют
    """
    try:
        # Формирование эндпоинта
        currencies_endpoint = f"{API_URL}/currencies?apikey={API_TOKEN}"

        # Отправка запроса
        response = requests.get(currencies_endpoint)

        # Проверка ответа
        if response.status_code != 200:
            error_info = response.json()
            error_message = error_info.get("message", "Неизвестная ошибка")
            return {"error": f"Ошибка сервера: {response.status_code}", "message": error_message}

        data = response.json()

        # Проверка содержимого ответа
        if "data" not in data:
            return {"error": "Некорректный формат ответа от API."}

        # Применение количества к курсам
        currencies = data["data"]

        return currencies

    except requests.RequestException as e:
        return {"error": f"Ошибка при соединении с API: {e}"}
    except ValueError as e:
        return {"error": str(e)}


all_currencies = get_all_currencies()
pprint(all_currencies)
