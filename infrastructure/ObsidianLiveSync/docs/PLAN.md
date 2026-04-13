# Plan – ObsidianLiveSync

## Zielbild

- CouchDB läuft auf dem VPS
- Obsidian LiveSync Plugin auf Dirks Geräten verbindet sich mit dieser Instanz
- Änderungen synchronisieren bidirektional zwischen Geräten und VPS
- Der Assistent kann auf den Vault auf dem VPS zugreifen und dort mitschreiben

## Vorbedingungen

1. Docker oder Podman installieren
2. Kleine Swap-Datei als Sicherheitsreserve anlegen
3. Sichere Erreichbarkeit definieren
4. Zugangsdaten sicher festlegen
5. Backup- und Rückbaupfad festhalten

## Geplante Schritte

### Phase 0 – Dokumentation & Baseline
- Projektstruktur anlegen
- Systemzustand dokumentieren
- Rückbau-Ordner vorbereiten

### Phase 1 – Laufzeit vorbereiten
- Docker installieren
- Swap optional anlegen
- Bestehende Konfigurationen sichern

### Phase 2 – Dienst aufsetzen
- CouchDB-Container starten
- Datenpfad festlegen
- Absicherung definieren
- Exponierung minimieren

### Phase 3 – Geräte verbinden
- LiveSync Plugin auf Geräten konfigurieren
- Verbindung testen
- Synchronisationsverhalten beobachten

### Phase 4 – Betriebsregeln
- Festlegen, was der Assistent automatisch in den Vault schreiben darf
- Wartungs- und Backup-Routine definieren

## Rückbaugrundsatz

Jede Änderung muss so dokumentiert werden, dass sie vollständig rückgängig gemacht werden kann.
