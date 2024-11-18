# Конвертер валют

### Выберите язык

| Русский  | English                              | Español                              | 中文                              | Français                              | Deutsch                              |
|----------|--------------------------------------|--------------------------------------|---------------------------------|---------------------------------------|--------------------------------------|
| **Выбран** | [English](./docs/lang/README_en.md) | [Español](./docs/lang/README_es.md) | [中文](./docs/lang/README_zh.md) | [Français](./docs/lang/README_fr.md) | [Deutsch](./docs/lang/README_de.md) |

---

**Currency Converter** — это проект для работы с API обмена валют. Вы можете запрашивать курсы валют, выполнять конвертацию и тестировать функционал через готовые тесты.

---

## Структура проекта

```plaintext
currency-converter/
├── docs/...              # Материалы используемые в README.md
├── src/
│   ├── main.py           # Основной файл для запуска приложения
│   ├── api_service.py    # Работа с API (запросы и обработка)
├── tests/
│   ├── test.py           # Тесты для проверки функционала
├── index.py              # Точка входа для запуска приложения
├── .env                  # Конфигурационный файл (токен и URL). Создается самостоятельно!
├── .env.example          # Пример конфигурационного файла
├── .gitignore            # Игнорируемые файлы Git
├── requirements.txt      # Список зависимостей
├── README.md             # Документация проекта
```

---

## Установка

### 1. Клонирование репозитория

Склонируйте проект на ваш локальный компьютер:

```bash
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

### 2. Создание виртуального окружения

Рекомендуется использовать виртуальное окружение для изоляции зависимостей:

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate  # Для Bash/Zsh/Linux/MacOS
venv\Scripts\activate     # Для Windows
```

### 3. Установка зависимостей

Установите зависимости из `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Конфигурация

1. Переименуйте файл `.env.example` в `.env`:

```bash
mv .env.example .env
```

2. Укажите токен и базовый URL API в `.env`:

```plaintext
API_TOKEN='ВАШ_API_ТОКЕН'
API_URL='https://api.freecurrencyapi.com/v1'
```

---

## Запуск

### 1. Запуск приложения

Запустите проект через файл `index.py`:

```bash
python3 index.py
```

---

## Тестирование

### Запуск тестов

Для выполнения тестов используйте файл `tests/test.py`:

```bash
python tests/test.py
```

Этот файл проверяет корректность подключения к API и отображает список доступных валют.

---

## Демонстрация работы

Успешная конвертация

![currency-convert-result-work-success.png](docs/img/currency-convert-result-work-success.png)

<details>
<summary>Процесс конвертации (успешная конвертация (GIF))</summary>

![currency-convert-result-work-success.gif](docs/img/currency-convert-result-work-success.gif)

</details>

Ошибка при конвертации

![currency-convert-result-work-error.png](docs/img/currency-convert-result-work-error.png)

<details>
<summary>Процесс конвертации (ошибка при конвертации (GIF))</summary>

![currency-convert-result-work-error.gif](docs/img/currency-convert-result-work-error.gif)

</details>

---

## Currency Converter на PHP

Создан проект на PHP с похожим функционалом, но имеющий ряд отличий:

- Реализован веб-интерфейс
- Описаны все имеющиеся эндпоинты сервиса.

Пример кода: [freecurrencyapi-converter-php](https://github.com/yaleksandr89/freecurrencyapi-converter-php) — всё там, заходите! 😄

---

## Примечания

1. **Токен безопасности:**
   - Убедитесь, что ваш токен API указан корректно в `.env`.
   - Никогда не добавляйте файл `.env` в репозиторий.

2. **Рекомендации:**
   - Используйте виртуальное окружение для изоляции зависимостей.
   - Обновляйте зависимости при необходимости через `pip install --upgrade`.

3. **Доработка:**
   - Основной функционал (`main.py`) будет реализован позже.
   - Для добавления новых тестов используйте директорию `tests`.
