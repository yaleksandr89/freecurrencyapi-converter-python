# Zur Entwicklung beitragen

## Sprache wählen

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../../.github/CONTRIBUTING.md) | [English](../en/CONTRIBUTING.md) | [Español](../es/CONTRIBUTING.md) | [中文](../zh/CONTRIBUTING.md) | [Français](../fr/CONTRIBUTING.md) | **Ausgewählt** |

## Vor dem Start

Prüfen Sie, ob Ihr Vorhaben bereits besprochen wird. Für ein [neues Issue](https://github.com/yaleksandr89/freecurrencyapi-converter-python/issues/new/choose) wählen Sie die Fehlermeldung oder den Verbesserungsvorschlag.

- Nennen Sie bei Fehlern die Umgebung, den Befehl, Eingabedaten, Schritte zur Reproduktion sowie erwartete und tatsächliche Ausgabe.
- Beschreiben Sie bei Vorschlägen die Aufgabe und das gewünschte CLI-Verhalten.
- Sicherheitslücken melden Sie gemäß der [Sicherheitsrichtlinie](SECURITY.md).

## Branches und Commits

Erstellen Sie einen separaten Branch von `master`, beispielsweise `fix/invalid-amount` oder `docs/setup-guide`. Commits und Pull-Request-Titel folgen Conventional Commits: englischer Typpräfix und **russischsprachige Beschreibung**.

```text
docs: уточнить запуск конвертера
fix: отклонять недопустимые суммы
test: проверить обработку некорректных ответов API
```

## Lokale Prüfungen

Führen Sie im Projektverzeichnis unter Linux oder macOS mit Python 3.12 oder neuer die folgenden Befehle aus. `make setup` erstellt `.venv` bei Bedarf und installiert Entwicklungsabhängigkeiten. Beim Erstellen kann der Interpreter mit `PYTHON` angegeben werden.

```bash
make setup PYTHON=python3
make check
```

`make check` führt pytest, Ruff für Stil und Formatierung sowie `pip check` aus. Die Tests simulieren FreecurrencyAPI-Antworten und brauchen keinen echten Schlüssel. PowerShell-Befehle finden Sie in der [Einrichtungsanleitung](guides/getting-started.md#lokale-prüfungen).

Nehmen Sie `.env`, echte API-Schlüssel oder Protokolle mit Geheimnissen nicht in Commits auf.

## Pull Requests

Öffnen Sie einen Pull Request nach `master`. Erläutern Sie Grund und Prüfungsergebnisse sowie mögliche Auswirkungen auf CLI, FreecurrencyAPI-Anfragen oder den Umgang mit Geheimnissen. Aktualisieren Sie gegebenenfalls Tests und Dokumentation.

Halten Sie alle sechs Dokumentationssprachen und beide Oberflächensprachen synchron.
