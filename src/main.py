from api_service import fetch_currency_rates, get_all_currencies


def start_converter():
    ALL_CURRENCIES = get_all_currencies()

    # 1.
    print("Приветствуем Вас в нашем Конвертере валют! 🌍💱")

    # 2.
    print("""
    Наш конвертер поможет вам быстро и легко перевести валюту!
    Вот как это работает:
    1. Вы выбираете валюту, которую хотите конвертировать.
    2. Вводите количество валюты.
    3. Указываете валюты, в которые хотите конвертировать.
    
    Готовы? Давайте начнем! 😊
    """)

    # 3. Список доступных валют
    count = 1
    for key in ALL_CURRENCIES:
        print(f"{count}. [{key}] {ALL_CURRENCIES[key]['name']}")
        count += 1

    # 4. Ввод исходной валюты
    user_currency = input("\nВведите валюту, которую у вас есть (например, RUB): ").upper()

    # 5. Ввод суммы
    current_amount = float(input("Введите количество этой валюты: "))

    # 6. Ввод валюты(-й) для конвертации
    conversion_currency = input("Введите валюту(-ы), в которые хотите конвертировать (например, USD или USD,EUR): ").upper().split(',')

    # 7. Получение курса и вывод результата
    currency_rates = fetch_currency_rates(user_currency, conversion_currency, current_amount)

    # 8. Вывод результатов
    print("\nРезультаты конвертации:")

    if 'error' in currency_rates:
        print(f"{currency_rates['error']}")
    else:
        for currency, rate in currency_rates.items():
            print(f"{current_amount} {user_currency} = {rate:.2f} {currency}")

if __name__ == "__main__":
    start_converter()
