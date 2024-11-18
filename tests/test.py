import os
import requests
from pprint import pprint
from dotenv import load_dotenv


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


def get_online_currencies():
    currencies_endpoint = f"{API_URL}/currencies?apikey={API_TOKEN}"
    response = requests.get(currencies_endpoint)
    pprint(response.json().get('data'))


get_online_currencies()
