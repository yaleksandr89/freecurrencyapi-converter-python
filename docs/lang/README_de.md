# Währungsumrechner

### Sprache Auswählen

| Русский | English | Español | 中文 | Français | Deutsch |
|---------|------------|------------|-----------|-------------|----------|
| [Русский](../../README.md) | [English](README_en.md) | [Español](README_es.md) | [中文](README_zh.md) | [Français](README_fr.md) | **Ausgewählt** |

---

**Currency Converter** ist ein Projekt für die Arbeit mit der Währungsumtausch-API. Sie können Wechselkurse abfragen, die Konvertierung durchführen und die Funktionalität durch vorgefertigte Tests testen.

---

## Projektstruktur

```plain text
currency-converter/
├── docs/...              # Materialien benutzt in README.md
├── src/
│   ├── main.py           # Hauptdatei zum Starten der Anwendung
│   ├── api_service.py    # Arbeiten mit APIs (Anfragen und Verarbeitung)
├── tests/
│   ├── test.py           # Tests, um die Funktionalität zu testen
├── index.py              # Einstiegspunkt zum Starten der App
├── .env                  # Konfigurationsdatei (Token und URL). Es wird selbst erstellt!
├── .env.example          # Beispiel für eine Konfigurationsdatei
├── .gitignore            # Ignorierte Git-Dateien
├── requirements.txt      # Liste der Abhängigkeiten
├── README.md             # Projektdokumentation
```

---

## Installation

### 1. Repository klonen

Klonen Sie das Projekt auf Ihren lokalen Computer:

```bash
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

### 2. Erstellen einer virtuellen Umgebung

Es wird empfohlen, eine virtuelle Umgebung zu verwenden, um Abhängigkeiten zu isolieren:

```bash
# Erstellen einer virtuellen Umgebung
python3 -m venv venv

# Virtuelle Umgebung aktivieren
source venv/bin/activate  # Für Bash/Zsh/Linux/macOS
venv\Scripts\activate     # Für Windows
```

### 3. Installieren von Abhängigkeiten

Legen Sie Abhängigkeiten von `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Konfiguration

1. Benennen Sie die Datei um. `env.example` in `.env`:

```bash
mv .env.example .env
```

2. Geben Sie das Token und die Basis-API-URL in `.env` ein:

```plaintext
API_TOKEN='ВАШ_API_ТОКЕН'
API_URL='https://api.freecurrencyapi.com/v1'
```

---

## Start

### 1. Starten der Anwendung

Führen Sie das Projekt über die Datei aus `index.py`:

```bash
python3 index.py
```

---

## Testen

### Ausführen von Tests

Verwenden Sie die Datei `tests/test.py`, um die Tests durchzuführen:

```bash
python3 tests/test.py
```

Diese Datei überprüft, ob die API-Verbindung korrekt ist, und zeigt eine Liste der verfügbaren Währungen an.

---

## Demonstration der Arbeit

Erfolgreiche Konvertierung

![currency-convert-result-work-success.png](/docs/img/currency-convert-result-work-success.png)

<details>
<summary>Konvertierungsvorgang (erfolgreiche Konvertierung (GIF))</summary>

![currency-convert-result-work-success.gif](/docs/img/currency-convert-result-work-success.gif)

</details>

Fehler beim Konvertieren

![currency-convert-result-work-error.png](/docs/img/currency-convert-result-work-error.png)

<details>
<summary>Konvertierungsvorgang (Konvertierungsfehler (GIF))</summary>

![currency-convert-result-work-error.gif](/docs/img/currency-convert-result-work-error.gif)

</details>

---

## Währungsrechner in PHP

Es wurde ein PHP-Projekt mit ähnlicher Funktionalität erstellt, das jedoch einige Unterschiede aufweist:

- Web-Schnittstelle implementiert
- Alle verfügbaren Service-Endpunkte werden beschrieben.

Beispielcode: [freecurrencyapi-converter-php](https://github.com/yaleksandr89/freecurrencyapi-converter-php) — alles ist da, kommt rein! 😄

---

## Beispiel

1. **Sicherheitstoken:**
   - Stellen Sie sicher, dass Ihr API-Token in `.env` korrekt angegeben ist.
   - Fügen Sie niemals eine Datei hinzu. `.env` in das Repository.

2. **Empfehlung:**
   - Verwenden Sie eine virtuelle Umgebung, um Abhängigkeiten zu isolieren.
   - Aktualisieren Sie die Einstellungen bei Bedarf über `pip install --upgrade`.
