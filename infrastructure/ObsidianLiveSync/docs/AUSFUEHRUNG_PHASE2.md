# Ausführung Phase 2 – Nginx Reverse Proxy + HTTPS

> Erstellt vor Ausführung — Zustand, Schritte und Rollback dokumentiert bevor irgendwas geändert wird.
> Datum: 2026-04-15

---

## Ziel dieser Phase

Phase 2 richtet den öffentlichen Zugang zu CouchDB ein — ausschließlich über HTTPS und einen Nginx Reverse Proxy.

1. **Nginx** installieren und konfigurieren
2. **Certbot** installieren und Let's Encrypt Zertifikat ausstellen
3. Nginx als **Reverse Proxy** für `obsidian.dirkbusmann.de` → `127.0.0.1:5984` einrichten
4. HTTPS von außen verifizieren

Was in dieser Phase **nicht** gemacht wird:
- kein LiveSync Plugin auf Geräten
- kein Portainer
- keine Geräteanbindung

---

## Zustand vor Ausführung (Baseline Phase 2)

| Komponente | Zustand |
|---|---|
| OS | Ubuntu 24.04.4 LTS |
| Docker | installiert, Version 29.4.0 ✅ |
| Swap | 2 GB aktiv ✅ |
| CouchDB | läuft als Container `couchdb-livesync`, Port 5984 nur lokal ✅ |
| Nginx | nicht installiert |
| Certbot | nicht installiert |
| HTTPS | nicht aktiv |
| DNS | `obsidian.dirkbusmann.de` → `157.90.117.9` ✅ propagiert |
| Öffentliche Ports | SSH (22) |

---

## Schritt 1 — Nginx installieren

```bash
apt-get update
apt-get install -y nginx
systemctl enable nginx
systemctl start nginx
```

### Rollback Nginx
```bash
systemctl stop nginx
apt-get purge -y nginx nginx-common
apt-get autoremove -y
```

---

## Schritt 2 — Nginx-Konfiguration für obsidian.dirkbusmann.de

Konfigurationsdatei: `/etc/nginx/sites-available/obsidian`

Proxy-Weiterleitung: `obsidian.dirkbusmann.de` → `http://127.0.0.1:5984`

### Rollback Nginx-Config
```bash
rm /etc/nginx/sites-enabled/obsidian
rm /etc/nginx/sites-available/obsidian
systemctl reload nginx
```

---

## Schritt 3 — Certbot + Let's Encrypt Zertifikat

```bash
apt-get install -y certbot python3-certbot-nginx
certbot --nginx -d obsidian.dirkbusmann.de --non-interactive --agree-tos -m admin@dirkbusmann.de
```

Certbot übernimmt automatisch:
- Zertifikat ausstellen
- Nginx-Config auf HTTPS umschreiben
- HTTP → HTTPS Redirect einrichten
- Auto-Renewal über systemd-Timer

### Rollback Certbot
```bash
certbot delete --cert-name obsidian.dirkbusmann.de
apt-get purge -y certbot python3-certbot-nginx
```

---

## Erwarteter Zustand nach Ausführung

| Komponente | Erwarteter Zustand |
|---|---|
| Nginx | installiert, läuft, Reverse Proxy aktiv |
| HTTPS | aktiv mit Let's Encrypt Zertifikat |
| `obsidian.dirkbusmann.de` | erreichbar über HTTPS, leitet zu CouchDB weiter |
| Öffentliche Ports | SSH (22), HTTP (80 → Redirect), HTTPS (443) |
| CouchDB | weiterhin nur lokal auf 127.0.0.1:5984 (Nginx davor) |

---

*Erstellt am 2026-04-15 vor Ausführung*
