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

- Phase 1 gestartet am 2026-04-14
- Geplante systemverändernde Schritte in Phase 1:
  - Docker installieren
  - 2 GB Swap anlegen
  - CouchDB lokal via Docker Compose starten
- Vor Ausführung dokumentiert in: `docs/AUSFUEHRUNG_PHASE1.md`

## Rückbau Phase 1

### Docker entfernen
```bash
apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
apt-get autoremove -y
rm -rf /var/lib/docker
rm -f /etc/apt/sources.list.d/docker.list
rm -f /etc/apt/keyrings/docker.asc
```

### Swap entfernen
```bash
swapoff /swapfile
sed -i '/swapfile/d' /etc/fstab
rm -f /swapfile
```

### CouchDB entfernen
```bash
cd /root/OpenClaw_PersonalAssistant/infrastructure/ObsidianLiveSync/config
docker compose down
rm -rf /root/data/couchdb
rm -f /root/OpenClaw_PersonalAssistant/infrastructure/ObsidianLiveSync/config/.env
```

## Prinzipien

- Vor Änderungen immer Backup in `backups/` ablegen
- Jede Dateiänderung mit Pfad dokumentieren
- Jede Port-/Dienständerung dokumentieren
- Rückbaukommandos ergänzen, sobald reale Änderungen erfolgt sind
