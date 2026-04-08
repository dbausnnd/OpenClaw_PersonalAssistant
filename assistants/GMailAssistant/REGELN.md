# GMailAssistant – Regeln

## Zweck

Der GMailAssistant verarbeitet das Gmail-Postfach `dirkbusmann@gmail.com`, kategorisiert eingehende Mails, vergibt Labels und archiviert bestimmte Kategorien automatisch.

## Kategorien

1. `01 Spam / Verdächtig`
2. `02 Systemmeldungen`
3. `03 Termineinladungen`
4. `04 Wichtig / Persönlich`
5. `05 Shopping`
6. `06 KI`
7. `07 Gaming`
8. `08 Werbung / Newsletter`
9. `09 Unwichtig`

## Priorität bei Überschneidungen

1. Spam / Verdächtig
2. Systemmeldungen
3. Termineinladungen
4. Wichtig / Persönlich
5. Shopping
6. KI
7. Gaming
8. Werbung / Newsletter
9. Unwichtig

## Automatische Archivierung

Folgende Labels werden automatisch archiviert, wobei das Label erhalten bleibt:
- `05 Shopping`
- `06 KI`
- `07 Gaming`
- `08 Werbung / Newsletter`
- `09 Unwichtig`

Archivieren bedeutet:
- Label `INBOX` wird entfernt
- andere Labels bleiben erhalten
- ungelesene Mails bleiben ungelesen

## Sonderregeln

### Systemmeldungen
- Mails von `DS216+` oder `DS211J`
- typischerweise von `Synology DiskStation`
- oft von `dirkbusmann@gmail.com`
- -> `02 Systemmeldungen`

### Kleinanzeigen
- Kommunikationsmails über Kleinanzeigen
- z. B. `Nutzer-Anfrage zu deiner Anzeige`
- `Re: Nutzer-Anfrage zu deiner Anzeige`
- -> `05 Shopping`

### Apple
- Abo-, Rechnungs-, Kauf- oder Bestellmails von Apple
- -> `05 Shopping`

### OpenAI
- Funding-, Billing-, Receipt-, Charged- oder Invoice-Mails
- -> `05 Shopping`
- sonstige KI-/Produktmails -> `06 KI`

### Notion
- Login Codes / Verifizierungs-Codes
- -> `04 Wichtig / Persönlich`

### VitaDock
- immer -> `04 Wichtig / Persönlich`

### Doreen Busmann
- immer -> `04 Wichtig / Persönlich`

### LinkedIn
- Kontaktanfragen -> `04 Wichtig / Persönlich`
- Einladungen -> `03 Termineinladungen`
- Jobalerts / Profilbesuche / allgemeines Rauschen -> `09 Unwichtig`

### GitHub
- Sicherheits- und Verifikationsmails -> `04 Wichtig / Persönlich`

## Betriebsprinzip

- Regeln dürfen erweitert werden
- Änderungen sollen in `HISTORY.md` dokumentiert werden
- Der Assistent soll später pausierbar und stoppbar sein
- Wenn Regeln, Kategorien, Prioritäten, Archivierungslogik oder Struktur geändert werden, müssen die Dateien in diesem Repository aktualisiert, committed und nach GitHub gepusht werden
