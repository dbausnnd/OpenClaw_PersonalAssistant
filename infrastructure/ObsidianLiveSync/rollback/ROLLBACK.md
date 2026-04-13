# Rollback – ObsidianLiveSync

## Ziel

Wenn die Einrichtung verworfen oder zurückgebaut werden soll, muss der Ursprungszustand wiederherstellbar sein.

## Rückbau-Checkliste

Vor jedem Umbau ergänzen:
- welche Pakete wurden installiert?
- welche Dienste wurden aktiviert?
- welche Container wurden erstellt?
- welche Ports wurden geöffnet?
- welche Reverse-Proxy-Dateien wurden angelegt oder geändert?
- welche Pfade wurden für Daten persistent genutzt?
- welche Credentials wurden erzeugt?

## Aktueller Stand

- Noch kein Rückbau nötig
- Noch keine systemverändernden Schritte durchgeführt

## Prinzipien

- Vor Änderungen immer Backup in `backups/` ablegen
- Jede Dateiänderung mit Pfad dokumentieren
- Jede Port-/Dienständerung dokumentieren
- Rückbaukommandos ergänzen, sobald reale Änderungen erfolgt sind
