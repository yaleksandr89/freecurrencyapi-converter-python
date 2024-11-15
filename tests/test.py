import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_token = os.getenv('API_TOKEN')


def get_online_currencies():
    all_currencies_url = f'https://api.freecurrencyapi.com/v1/currencies?apikey={api_token}&currencies='
    response = requests.get(all_currencies_url)
    print(response.json().get('data'))
    return response.json().get('data')


get_online_currencies()
