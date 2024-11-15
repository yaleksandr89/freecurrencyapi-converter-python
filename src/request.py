from dotenv import load_dotenv
import os

# Загружаем данные из .env и получаем их
load_dotenv()
api_token = os.getenv("API_TOKEN")
# print(f"My API token is: {api_token}") # Проверка получения токена из .env

