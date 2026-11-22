# Installation und erster Start

## Sprache wählen

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](getting-started.md) | [English](getting-started_en.md) | [Español](getting-started_es.md) | [中文](getting-started_zh.md) | [Français](getting-started_fr.md) | **Ausgewählt** |

## Eigenständige Programme

Sobald auf der [Releases-Seite](https://github.com/yaleksandr89/freecurrencyapi-converter-python/releases) ein Archiv für Ihr System verfügbar ist, laden Sie es herunter und entpacken Sie es in einen Ordner. Das eigenständige Programm läuft ohne Python und `make`.

1. Kopieren Sie im entpackten Ordner `.env.example` nach `.env` und tragen Sie Ihren FreecurrencyAPI-Schlüssel in `API_TOKEN` ein. Übernehmen Sie `API_URL` aus der Vorlage.
2. Doppelklicken Sie unter Windows auf `currency-converter.exe`. Führen Sie unter Linux und macOS `./currency-converter` in einem Terminal in diesem Ordner aus. Unter macOS können Sie auch `Launch Currency Converter.command` öffnen.

Die beiliegende `README.md` enthält eine kurze Anleitung auf Russisch und Englisch.

## Voraussetzungen für die Installation aus dem Quellcode

- Git zum Klonen des Repositorys, Python 3.12 oder neuer sowie `venv` mit `pip`.
- Ein eigener FreecurrencyAPI-Schlüssel für Umrechnungen. Registrieren Sie sich und entnehmen Sie den Schlüssel Ihrem Benutzerkonto. Die API ist in der [FreecurrencyAPI-Dokumentation](https://freecurrencyapi.com/docs/) beschrieben.

## Quellcode herunterladen

Klonen Sie das Repository und wechseln Sie in das Stammverzeichnis mit `index.py`. Führen Sie alle folgenden Befehle dort aus.

```bash
# Repository klonen und ins Projektverzeichnis wechseln.
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

## Abhängigkeiten installieren

### Linux und macOS

Prüfen Sie, ob `python3` Python 3.12 oder neuer startet und `make` installiert ist. `make setup` erstellt `.venv`, sofern es noch nicht existiert, und installiert das Projekt samt Entwicklungsabhängigkeiten.

```bash
# Python-Version überprüfen.
python3 --version

# .venv erstellen und Entwicklungsabhängigkeiten installieren.
make setup

# Lokale Konfiguration erstellen, ohne einen bestehenden Schlüssel zu überschreiben.
cp -n .env.example .env
```

Ist der passende Interpreter unter einem anderen Namen verfügbar, geben Sie ihn mit `PYTHON` an, zum Beispiel `make setup PYTHON=python3.12`. Diese Variable wirkt nur beim Erstellen der Umgebung.

### Windows PowerShell

In diesem Beispiel ist `python` Python 3.12 oder neuer und über `PATH` verfügbar. Die Befehle nutzen den Interpreter aus `.venv` direkt; weder Aktivierung noch `make` sind erforderlich.

```powershell
# Installierte Python-Version prüfen.
python --version

# Umgebung erstellen und Entwicklungsabhängigkeiten installieren.
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

# Beispielkonfiguration nur kopieren, wenn .env fehlt.
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Möchten Sie nur das Programm samt Laufzeitabhängigkeiten installieren, ersetzen Sie `requirements-dev.txt` durch `requirements.txt` im `pip install`-Befehl. Für lokale Prüfungen werden die Entwicklungsabhängigkeiten benötigt.

## API-Schlüssel und Adresse konfigurieren

Öffnen Sie die neue Datei `.env` im Editor. Ersetzen Sie `API_TOKEN` durch Ihren Schlüssel. In `API_URL` steht die API-Basisadresse ohne konkreten Endpunkt.

```ini
API_TOKEN=your_api_token_here
API_URL=https://api.freecurrencyapi.com/v1
```

Bewahren Sie den Schlüssel lokal auf. Committen Sie `.env` nicht und veröffentlichen Sie den Inhalt nicht in Fehlerberichten. Bereits gesetzte Prozess-Umgebungsvariablen haben Vorrang vor den Werten in `.env`.

## Starten und prüfen

Starten Sie den Rechner unter Linux und macOS mit `make`:

```bash
# Russische Oberfläche (Standard).
make run

# Englische Oberfläche.
make run CLI_LANG=en
```

Unter Windows PowerShell führen Sie `index.py` mit dem Python-Interpreter der virtuellen Umgebung aus:

```powershell
# Russische Oberfläche (Standard).
.\.venv\Scripts\python.exe index.py

# Englische Oberfläche.
.\.venv\Scripts\python.exe index.py --lang en
```

Nach der Begrüßung wird die Währungsliste angezeigt. Wenn `USD`, `EUR` und `GBP` enthalten sind, geben Sie nacheinander `USD`, `12.5` und `EUR,GBP` ein und bestätigen jede Eingabe mit Enter. Bei Erfolg erscheint eine Zeile je Zielwährung. Die Werte hängen von den abgerufenen Kursen ab.

Mit der Hilfeoption können Sie den CLI-Start ohne API-Schlüssel und Anfrage prüfen: `.venv/bin/python index.py --help` unter Linux/macOS bzw. `.\.venv\Scripts\python.exe index.py --help` in PowerShell.

## Wenn der Start fehlschlägt

| Symptom | Prüfen Sie |
| --- | --- |
| `API_TOKEN` oder `API_URL` fehlt | Dateinamen `.env`, Variablennamen und nichtleere Werte prüfen. Bereits in der Shell gesetzte Variablen ebenfalls kontrollieren. |
| Fehler mit HTTP-Statuscode | Basisadresse, Gültigkeit des Schlüssels und verbleibendes FreecurrencyAPI-Kontingent prüfen. |
| Zeitüberschreitung oder Anfragefehler | `API_URL` und die Verfügbarkeit von FreecurrencyAPI prüfen. |
| CLI lehnt die Eingabe ab | Rechner neu starten, Codes aus der Liste wählen, Zielwährungen mit Kommas trennen und einen positiven Betrag mit Dezimalpunkt eingeben. |

Fehlerursachen und Exit-Codes finden Sie in der [CLI- und Fehlerreferenz](../reference/cli-and-errors_de.md).

## Lokale Prüfungen

Prüfen Sie das Projekt nach Installation der Entwicklungsabhängigkeiten im Stammverzeichnis.

Unter Linux und macOS:

```bash
# Tests, Ruff und Prüfung der installierten Abhängigkeiten ausführen.
make check
```

Unter Windows PowerShell:

```powershell
# Offline-Tests.
.\.venv\Scripts\python.exe -m pytest

# Stil und Formatierung prüfen.
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .

# Installierte Abhängigkeiten prüfen.
.\.venv\Scripts\python.exe -m pip check
```

Die Tests simulieren FreecurrencyAPI-Antworten und Netzwerkfehler und blockieren echte HTTP-Anfragen. Ein echter Schlüssel wird nicht benötigt. Nur eine interaktive Umrechnung prüft, ob Schlüssel und Dienst tatsächlich funktionieren.
