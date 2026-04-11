# GMailAssistant – Verlauf

## 2026-04-08

- Grundstruktur des Assistenten angelegt
- Gmail-Zugang technisch eingerichtet
- Startlabels definiert und in Gmail angelegt
- Alte benutzerdefinierte Labels unter `XXX ALT` gesammelt
- Kategorien nummeriert und nach Priorität sortiert
- Automatische Archivierung aktiviert für:
  - `05 Shopping`
  - `06 KI`
  - `07 Gaming`
  - `08 Werbung / Newsletter`
  - `09 Unwichtig`
- Bereits ein größerer Teil des Posteingangs wurde kategorisiert
- Betriebsmodus für ressourcenschonenden Dauerbetrieb festgelegt:
  - rules-first
  - alle 10 Minuten
  - nur ungelabelte Inbox-Mails
  - kein Standard-LLM-Einsatz

### Bereits festgelegte Sonderregeln
- Kleinanzeigen-Kommunikation -> `05 Shopping`
- DS216+/DS211J/Synology-Meldungen -> `02 Systemmeldungen`
- Apple Abo/Rechnung/Kauf -> `05 Shopping`
- OpenAI Funding/Billing/Receipt -> `05 Shopping`
- Notion Login Code -> `04 Wichtig / Persönlich`
- VitaDock -> `04 Wichtig / Persönlich`
- Doreen Busmann -> `04 Wichtig / Persönlich`

### Governance-Regel
- Wenn Regeln, Kategorien, Prioritäten, Archivierungslogik oder Struktur geändert werden, müssen die Dateien im Repository aktualisiert, committed und nach GitHub gepusht werden.

## 2026-04-11

### Fehlklassifikation LinkedIn-Einladungsmails behoben
- Problem: LinkedIn-Sammel-Mails wie "Sie haben über 10 neue Einladungen" wurden als `03 Termineinladungen` klassifiziert
- Ursache: Allgemeine Termin-Regel trifft auf das Wort "einladung" im Betreff
- Fix: LinkedIn-Mails werden jetzt **vor** der allgemeinen Termin-Regel geprüft
- Neue Regel: LinkedIn-Mails mit "neue einladungen" im Text -> `09 Unwichtig`
- Betroffene Dateien: `runner.py`, `REGELN.md`

## Hinweis

Diese Datei dient als Verlauf der Regelentwicklung. Spätere Änderungen und Lernpunkte sollen hier ergänzt werden.
