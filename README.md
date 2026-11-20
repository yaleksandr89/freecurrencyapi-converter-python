# Конвертер валют

[![Исходный код](https://img.shields.io/badge/GitHub-%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D1%8B%D0%B9_%D0%BA%D0%BE%D0%B4-181717?style=flat-square)](https://github.com/yaleksandr89/freecurrencyapi-converter-python)
[![Проверки CI](https://github.com/yaleksandr89/freecurrencyapi-converter-python/actions/workflows/ci.yml/badge.svg)](https://github.com/yaleksandr89/freecurrencyapi-converter-python/actions/workflows/ci.yml)
[![Python 3.12 и новее](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square)](pyproject.toml)
[![Лицензия MIT](https://img.shields.io/badge/%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F-MIT-2EA44F?style=flat-square)](LICENSE.md)

![Currency Converter — интерактивный конвертер валют на Python](docs/assets/currency-converter-readme-cover.png)

## Выберите язык

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| **Выбран** | [English](docs/lang/README_en.md) | [Español](docs/lang/README_es.md) | [中文](docs/lang/README_zh.md) | [Français](docs/lang/README_fr.md) | [Deutsch](docs/lang/README_de.md) |


Интерактивный конвертер на Python пересчитывает сумму из одной валюты в одну или несколько других по курсам FreecurrencyAPI. Ввод и результаты отображаются в терминале.

- Список доступных валют загружается при каждом интерактивном запуске.
- Курсы запрашиваются для выбранных валют после проверки ввода.
- Подсказки и сообщения доступны на русском и английском языках.

Нужен Python 3.12 или новее и собственный ключ FreecurrencyAPI. Команды ниже рассчитаны на Linux и macOS с `make`. В CI проверки выполняются на Ubuntu с Python 3.12, 3.13 и 3.14.

## Как проходит конвертация

Введите исходную валюту, сумму и целевые валюты. Конвертер получит курсы для выбранных кодов и покажет результат в терминале.

```mermaid
flowchart LR
    A["Загрузить список валют"] --> B["Принять и проверить ввод"]
    B --> C["Запросить курсы"]
    C --> D["Рассчитать и вывести суммы"]
```

Порядок работы модулей, API-запросов и обработки сбоев подробно разобран в [описании архитектуры](docs/reference/architecture.md).

## Быстрый старт

Склонируйте репозиторий, создайте виртуальное окружение с зависимостями и скопируйте шаблон настроек.

```bash
# Скачайте проект и перейдите в его каталог.
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python

# Создайте .venv и установите зависимости для разработки.
make setup

# Скопируйте шаблон настроек, не перезаписывая существующий .env.
cp -n .env.example .env
```

Запишите ключ из личного кабинета FreecurrencyAPI в `API_TOKEN` файла `.env`. Базовый адрес `API_URL` уже указан в шаблоне. Из корня проекта запустите конвертер одной из команд.

```bash
# Русский интерфейс.
make run

# Английский интерфейс.
make run CLI_LANG=en
```

Для Windows PowerShell порядок установки и запуска приведён в [руководстве по началу работы](docs/guides/getting-started.md). Параметры CLI, правила ввода и коды ошибок описаны в [справочнике команд](docs/reference/cli-and-errors.md).

## Демонстрация

### Успешная конвертация

Расчёт суммы и вывод результата.

https://github.com/user-attachments/assets/47d64727-342d-4cb8-ba4c-d223253b2338

### Ошибка при конвертации

Сообщение конвертера об ошибке.

https://github.com/user-attachments/assets/5b0408fb-e59c-467a-bef5-72b7e30c066b

### Переключение языка интерфейса

Запуск CLI с другим языком подсказок и сообщений.

https://github.com/user-attachments/assets/217d4e51-7e09-460e-a6be-c7712ecb7b0f

## Обратная связь

- Сообщить об ошибке или предложить улучшение — [GitHub Issues](https://github.com/yaleksandr89/freecurrencyapi-converter-python/issues).
- Обсудить использование конвертера — [GitHub Discussions](https://github.com/yaleksandr89/freecurrencyapi-converter-python/discussions).

---

<p align="center">
  Если проект оказался полезен, поставьте звезду на GitHub — так его будет проще найти другим. 🤘
</p>
