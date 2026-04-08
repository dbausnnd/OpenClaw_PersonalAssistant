# GMailAssistant – Runbook

## Ziel

Der GMailAssistant soll ressourcenschonend und kostenschonend automatisch laufen, ohne dauerhaft ein LLM zu benötigen.

## Empfohlener Betriebsmodus

- Modus: `rules-first`
- Intervall: **alle 10 Minuten**
- Verarbeitung: nur `INBOX`
- Verarbeitung: nur Mails ohne bestehendes Assistenten-Label (`01` bis `09`)
- Standardfall: **kein LLM**
- LLM nur später für Ausnahmen oder manuelle Sonderprüfungen

## Ablauf pro Lauf

1. `STATUS.json` lesen
2. Wenn `status != active` oder `paused == true` oder `stopped == true` -> sofort beenden
3. `config.json` lesen
4. Gmail-Inbox abfragen
5. Nur ungelabelte Mails bearbeiten
6. Regeln anwenden
7. Label setzen
8. Bei `05`, `06`, `07`, `08`, `09` automatisch archivieren
9. `lastRun`, `lastRunResult`, `lastUpdated` in `STATUS.json` aktualisieren

## Warum 10 Minuten?

- kurz genug, damit neue Mails nicht lange als "neu" im Posteingang liegen
- lang genug, um ressourcenschonend zu bleiben
- für ein privates Postfach ein guter Kompromiss

## Pause / Stop

### Pausieren
Setze in `STATUS.json`:
- `status`: `paused`
- `paused`: `true`

### Fortsetzen
Setze in `STATUS.json`:
- `status`: `active`
- `paused`: `false`
- `stopped`: `false`

### Stoppen
Setze in `STATUS.json`:
- `status`: `stopped`
- `stopped`: `true`

## Technischer Hinweis

Die eigentliche wiederkehrende Ausführung kann später über:
- Cron
- OpenClaw Heartbeat
- oder einen kleinen lokalen Scheduler
realisiert werden.

Für die Zielarchitektur ist aktuell vorgesehen:
- häufiger, billiger Regel-Check
- kein permanenter LLM-Einsatz
