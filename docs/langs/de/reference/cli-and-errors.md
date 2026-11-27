# CLI-Befehle, Eingaben und Fehler

## Sprache wählen

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../ru/reference/cli-and-errors.md) | [English](../../en/reference/cli-and-errors.md) | [Español](../../es/reference/cli-and-errors.md) | [中文](../../zh/reference/cli-and-errors.md) | [Français](../../fr/reference/cli-and-errors.md) | **Ausgewählt** |

## Startoptionen

Starten Sie `index.py` im Projektverzeichnis mit dem Python-Interpreter aus `.venv`, der bei der Einrichtung erstellt wurde. Beispiele für Linux und macOS:

```bash
# Interaktive Umrechnung auf Russisch.
.venv/bin/python index.py

# Englische Oberfläche.
.venv/bin/python index.py --lang en

# Hilfe ohne Lesen von .env oder API-Anfrage.
.venv/bin/python index.py --help
```

Unter Windows PowerShell verwenden Sie `.\.venv\Scripts\python.exe` statt `.venv/bin/python`. Die [Einrichtungsanleitung](../guides/getting-started.md) erläutert beide Plattformen.

| Option | Verhalten |
| --- | --- |
| `-h`, `--help` | Zeigt die Hilfe in der gewählten Sprache an, ohne `.env` zu laden oder die API aufzurufen. |
| `--lang ru` | Wählt die russische Oberfläche; dies ist die Voreinstellung. |
| `--lang en` | Wählt die englische Oberfläche; kann mit `--help` kombiniert werden. |

## Eingabe und Ausgabeformat

Die CLI lädt zunächst die Währungen und zeigt sie an. Codes stehen in eckigen Klammern; Namen stammen von FreecurrencyAPI.

1. Geben Sie eine Ausgangswährung aus der Liste ein, etwa `USD`.
2. Geben Sie eine positive endliche Zahl mit Dezimalpunkt ein, etwa `2.5`. Eingaben wie `2,5`, `NaN` und `inf` werden abgelehnt.
3. Geben Sie einen oder mehrere Zielcodes ein, etwa `EUR,GBP`. Leere Elemente, auch nach einem abschließenden Komma, sind ungültig.

Groß- und Kleinschreibung wird ignoriert; äußere Leerzeichen werden entfernt. Bei einem Eingabefehler endet der Vorgang. Starten Sie den Befehl erneut.

Der Betrag wird als `float` eingelesen und vor der Multiplikation mit `round` auf drei Dezimalstellen gerundet. Wird dabei null erreicht oder ist das Produkt nicht endlich, wird ein Fehler ausgegeben.

Die Ausgabe erfolgt auf `stdout`, eine Zeile je Zielcode in der Reihenfolge der API-Antwort. Der gerundete Ausgangsbetrag hat keine feste Dezimalstellenzahl; der umgerechnete Betrag hat zwei. Das Beispiel verwendet simulierte Testkurse.

```text
2.5 USD = 2.00 EUR
2.5 USD = 1.25 GBP
```

## Anfragen an FreecurrencyAPI

Beide Anfragen verwenden `GET`, die Basisadresse aus `API_URL` und `API_TOKEN` als Abfrageparameter `apikey`.

| Endpunkt | Verwendung durch die CLI |
| --- | --- |
| [`/currencies`](https://freecurrencyapi.com/docs/currencies) | Lädt die Währungsliste vor der ersten Eingabe und verlangt für jeden Code einen nichtleeren Namen. |
| [`/latest`](https://freecurrencyapi.com/docs/latest) | Fordert Kurse nach gültiger Eingabe an. Sendet den Ausgangscode als `base_currency` und kommaseparierte Ziele als `currencies`. Die Multiplikation erfolgt lokal. |

Akzeptiert werden HTTP 200 und ein nichtleeres JSON-Objekt `data`. Die Zeitlimits betragen 4 Sekunden für den Verbindungsaufbau und 10 Sekunden für das Lesen der Antwort. Weiterleitungen sind deaktiviert. Für jedes Ziel muss ein Kurs vorliegen; nur angeforderte Kurse werden verwendet. FreecurrencyAPI bestimmt Währungsliste, Kurse und Kontingente.

## Exit-Codes

| Code | Bedeutung |
| --- | --- |
| `0` | Umrechnung erfolgreich oder Hilfe angezeigt. |
| `1` | Fehler bei Konfiguration, Anfrage, API-Antwort oder Eingabe, einschließlich vorzeitigem Eingabeende (EOF). |
| `2` | Ungültige CLI-Argumente wie unbekannte Optionen oder nicht unterstützte `--lang`-Werte. |
| `130` | Benutzer hat die interaktive Sitzung mit Ctrl+C unterbrochen. |

## Fehlermeldungen

Fehler werden auf `stderr` in der mit `--lang` gewählten Sprache ausgegeben. Ein ungültiges `--lang` führt zu einer russischen Fehlermeldung.

| Kategorie | Ursache |
| --- | --- |
| Konfiguration | `API_TOKEN` oder `API_URL` fehlt oder besteht nur aus Leerzeichen. |
| Netzwerk | Zeitüberschreitung oder anderer Anfragefehler, etwa eine gescheiterte Verbindung. |
| HTTP | Server antwortet nicht mit Status 200; der Status wird angezeigt. |
| API-Antwort | Ungültiges JSON; fehlendes, leeres oder ungültiges `data`; fehlerhafte Währungsmetadaten; fehlender, nicht positiver, nicht numerischer oder nicht endlicher Kurs für eine Zielwährung. |
| Eingabe | Unbekannter Quell- oder Zielcode, leeres Zielelement, ungültiger Betrag, Rundung auf null oder Überlauf bei der Berechnung. |
| Sitzungsende | Eingabestrom endete vor Abschluss der Eingaben oder der Benutzer drückte Ctrl+C. |
