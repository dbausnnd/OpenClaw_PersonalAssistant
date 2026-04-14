# Ausführung Phase 1 – Laufzeit + CouchDB

> Erstellt vor Ausführung — Zustand, Schritte und Rollback dokumentiert bevor irgendwas geändert wird.
> Datum: 2026-04-14

---

## Ziel dieser Phase

Phase 1 umfasst drei Schritte:
1. **Docker** auf dem VPS installieren
2. **Swap** (2 GB) anlegen — Sicherheitspuffer für RAM
3. **CouchDB** als Docker-Container starten, lokal gebunden, abgesichert

Was in dieser Phase **nicht** gemacht wird:
- kein Nginx / kein Reverse Proxy (braucht DNS-Eintrag)
- kein HTTPS / kein Certbot
- keine Geräteanbindung

---

## Zustand vor Ausführung (Baseline Phase 1)

| Komponente | Zustand |
|---|---|
| OS | Ubuntu 24.04.4 LTS |
| Kernel | Linux 6.8.0-106 |
| Docker | nicht installiert |
| Swap | nicht vorhanden |
| CouchDB | nicht vorhanden |
| Offene Ports (öffentlich) | SSH (22) |
| Offene Ports (lokal) | litellm :4000, openclaw-gateway :18789/:18791 |

---

## Schritt 1 — Docker installieren

### Warum Docker
CouchDB läuft als Docker-Container. Das hält das System sauber und isoliert.

### Quelle
Offizielle Docker-Repository für Ubuntu (nicht das Ubuntu-native `docker.io` Paket — das ist veraltet).

### Befehle
```bash
apt-get update
apt-get install -y ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Verifizierung
```bash
docker --version
docker compose version
docker run hello-world
```

### Rollback Docker
```bash
apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
apt-get autoremove -y
rm -rf /var/lib/docker
rm -f /etc/apt/sources.list.d/docker.list
rm -f /etc/apt/keyrings/docker.asc
```

---

## Schritt 2 — Swap anlegen (2 GB)

### Warum Swap
Der VPS hat keinen Swap. Bei RAM-Engpass (CouchDB + andere Dienste) würde der Kernel Prozesse abwürgen. 2 GB Swap als Sicherheitsnetz.

### Befehle
```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Verifizierung
```bash
swapon --show
free -h
```

### Rollback Swap
```bash
swapoff /swapfile
# In /etc/fstab die Zeile '/swapfile none swap sw 0 0' entfernen
sed -i '/swapfile/d' /etc/fstab
rm -f /swapfile
```

---

## Schritt 3 — CouchDB als Docker-Container starten

### Warum lokal gebunden
Port 5984 wird **nur auf 127.0.0.1** gebunden — nicht öffentlich erreichbar.
Externe Erreichbarkeit kommt später über Nginx + HTTPS (sobald DNS eingerichtet ist).

### Datenpfad
CouchDB-Daten liegen persistent auf dem Host:
```
/root/data/couchdb/
```

### Konfigurationspfad
Docker Compose Datei:
```
/root/OpenClaw_PersonalAssistant/infrastructure/ObsidianLiveSync/config/docker-compose.yml
```

### Credentials
- Admin-User: `admin`
- Admin-Passwort: generiert mit `openssl rand -base64 32`
- gespeichert in: `infrastructure/ObsidianLiveSync/config/.env` (Rechte 600, nie im Git)

### Starten
```bash
cd /root/OpenClaw_PersonalAssistant/infrastructure/ObsidianLiveSync/config
docker compose up -d
```

### Verifizierung
```bash
docker ps | grep couchdb
curl -s http://localhost:5984/
curl -s -u admin:PASSWORT http://localhost:5984/_all_dbs
```

### Rollback CouchDB
```bash
cd /root/OpenClaw_PersonalAssistant/infrastructure/ObsidianLiveSync/config
docker compose down
docker volume prune -f
rm -rf /root/data/couchdb
```

---

## Schritte in Reihenfolge

1. Docker installieren → verifizieren
2. Swap anlegen → verifizieren
3. `.env`-Datei anlegen mit Passwort (Rechte 600)
4. Datenpfad anlegen (`/root/data/couchdb/`)
5. CouchDB-Container starten
6. CouchDB intern testen
7. Dokumentation aktualisieren + commit

---

## Erwarteter Zustand nach Ausführung

| Komponente | Erwarteter Zustand |
|---|---|
| Docker | installiert, Version 25+ |
| Swap | 2 GB, aktiv |
| CouchDB | läuft als Container `couchdb-livesync`, Port 5984 nur lokal |
| Öffentliche Ports | unverändert (nur SSH) |

---

*Erstellt am 2026-04-14 vor Ausführung*
