**Шаг не обязательный, может быть пропущен**

* Создать виртуальное окружение: `python3 -m venv venv`
* Активировать виртуальное окружение: 
  * Для Bash/Zsh: `source venv/bin/activate`
  * Для Windows: `venv\Scripts\activate`

---

1. Установите зависимость `requests` и `python-dotenv`:
   * 1 вариант: `pip install requests==2.32.3 python-dotenv==1.0.1`
   * 2 вариант: `pip install -r requirements.txt`
2. Подключить API токен:
   * Переименовать `.env.example` в `.env` и указать токен для Freecurrencyapi
   * Импортировать необходимые модули и проверить, что токен получен в файле [request.py](src/request.py)
