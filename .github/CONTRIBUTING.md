# Участие в разработке / Contributing

## Перед началом / Before you start

- Проверьте, есть ли открытое обсуждение. Для [нового Issue](https://github.com/yaleksandr89/freecurrencyapi-converter-python/issues/new/choose) выберите форму ошибки или предложения.
- Для ошибки укажите окружение, команду и входные данные, шаги воспроизведения, ожидаемый и фактический вывод. Для предложения опишите задачу и желаемое поведение CLI.
- Об уязвимостях сообщайте по [политике безопасности](SECURITY.md).

## Ветки и коммиты / Branches and commits

Создайте отдельную ветку от `master`, например `fix/invalid-amount` или `feature/currency-search`. Используйте Conventional Commits.

```text
fix: reject invalid conversion amounts
feat: add currency search
test: cover malformed API responses
```

## Локальная проверка / Local checks

Нужен Python 3.12 или новее. При первом запуске `make setup` создаёт `.venv` выбранным интерпретатором и устанавливает зависимости для разработки. При необходимости укажите путь к нужному Python через `PYTHON`.

```sh
make setup PYTHON=python3
make check
```

`make check` запускает pytest, Ruff и `pip check` через `.venv/bin/python`. Тесты подменяют ответы FreecurrencyAPI и работают без сети и реального токена. Не добавляйте в коммиты `.env`, реальные API-токены и журналы с секретами.

## Pull request

Откройте PR в `master`. Укажите причину изменения, выполненные проверки и влияние на команды, вывод CLI или запросы к FreecurrencyAPI. При необходимости обновите тесты и документацию.
