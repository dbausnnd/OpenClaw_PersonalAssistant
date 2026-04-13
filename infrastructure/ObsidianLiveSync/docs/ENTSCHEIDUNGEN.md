# ObsidianLiveSync — Getroffene Entscheidungen

> Alle Entscheidungen aus dem Planungsgespräch vom 13.04.2026
> Diese Datei ersetzt die Liste offener Punkte in MASTERPLAN.md und DETAILBEDARF_ANTWORTEN.md

---

## 1. Domain / Subdomain

**Entscheidung:** `obsidian.dirkbusmann.de`

- Bestehende Domain bei Strato: `dirkbusmann.de`
- Hauptdomain zeigt weiterhin auf Synology im Heimnetz — **bleibt unberührt**
- Neuer DNS-Eintrag bei Strato:
  - Typ: A-Record
  - Subdomain: `obsidian`
  - Ziel: öffentliche IP des VPS
- Kein weiterer DNS-Eintrag nötig

---

## 2. Reverse Proxy

**Entscheidung:** Nginx + HTTPS — direkt von Anfang an

- Keine nackte IP-Lösung, auch nicht als temporäre Testlösung
- CouchDB wird **ausschließlich** über die Subdomain + HTTPS erreichbar sein
- Reihenfolge: Nginx wird zusammen mit CouchDB eingerichtet, nicht später
- HTTPS via Let's Encrypt / Certbot (kostenlos, automatische Erneuerung)

---

## 3. IP-Filter

**Entscheidung:** Kein IP-Filter

- Begründung: mobile Geräte haben wechselnde IP-Adressen
- Sicherheit wird stattdessen über mehrere Schichten erreicht:
  1. starkes zufälliges CouchDB-Passwort
  2. HTTPS (Transport-Verschlüsselung)
  3. LiveSync-Verschlüsselung (End-to-End-Passphrase, Details unten)
  4. Nginx Reverse Proxy
  5. optional: Fail2ban / Rate-Limit auf dem VPS

---

## 4. Verschlüsselung

**Entscheidung:** Verschlüsselung aktiv — vollständig

Zwei Ebenen:

### Ebene 1: Transport-Verschlüsselung (HTTPS)
- alle Daten zwischen Gerät und VPS laufen über HTTPS
- eingerichtet über Nginx + Let's Encrypt

### Ebene 2: End-to-End-Verschlüsselung (LiveSync-Passphrase)
- Notizen werden verschlüsselt **bevor** sie CouchDB erreichen
- selbst bei direktem Zugriff auf CouchDB-Daten wären die Inhalte nicht lesbar
- Konfiguration: im LiveSync-Plugin auf jedem Gerät wird eine Passphrase gesetzt
- diese Passphrase muss auf **allen Geräten gleich** eingetragen werden
- die Passphrase wird **nicht im Git-Repo gespeichert**
- Dirk notiert die Passphrase sicher (Passwortmanager empfohlen)

**Vergleich mit Obsidian Sync:**
Obsidian Sync bietet ebenfalls End-to-End-Verschlüsselung — der Unterschied ist:
- Obsidian Sync: fertig konfiguriertes Managed-Produkt
- LiveSync: gleiches Sicherheitsniveau, aber wir konfigurieren es selbst

---

## 5. Backup

**Entscheidung:** Git zusätzlich + Dateisystem-Backup für CouchDB

### Was über Git gesichert wird
- Vault-Markdown-Dateien: sinnvoll als Zusatz-Backup mit Versionshistorie
- nicht ausreichend als einziges Backup

### Was über Dateisystem-Backup gesichert wird
- CouchDB-Volume (gesamte Datenbank)
- Vault-Ordner
- Konfigurationsdateien (ohne Secrets)

### Speicherort Backup
- primär: `/root/backups/obsidian/` auf dem VPS
- externer Backup-Speicher: Entscheidung offen (kein zwingender Bedarf aktuell)

### Häufigkeit
- täglich
- zusätzlich: immer vor größeren Konfigurationsänderungen

---

## 6. Credential-Management

**Entscheidung:** `.env`-Datei mit Rechten 600, nie ins Git

- `.env`-Pfad: `/root/OpenClaw_PersonalAssistant/infrastructure/ObsidianLiveSync/config/.env`
- Rechte: `chmod 600`
- `.env` steht in `.gitignore`
- CouchDB-Passwort: generiert mit `openssl rand -base64 32`
- LiveSync-Passphrase: Dirk generiert und notiert im Passwortmanager
- Passwort-Rotation: **bei Bedarf** (kein fester Turnus)

---

## 7. Passwort-Rotation

**Entscheidung:** bei Bedarf

Rotation wird ausgelöst bei:
- Verdacht auf Kompromittierung
- Geräteverlust
- größerem Konfigurationswechsel
- auf explizite Anfrage

---

## 8. Sicherheits-Schichten (Übersicht)

| Schicht | Umsetzung | Status |
|---|---|---|
| Transport-Verschlüsselung | HTTPS via Nginx + Let's Encrypt | geplant |
| End-to-End-Verschlüsselung | LiveSync-Passphrase | geplant |
| Zugangsdaten | CouchDB Admin + starkes Passwort | geplant |
| Netzwerkexponierung | nur via Nginx-Proxy, nicht roh offen | geplant |
| Secrets-Schutz | `.env` lokal, nie ins Git | geplant |
| Backup | täglich, lokal | geplant |
| IP-Filter | nicht umsetzbar wegen Mobilgeräten | abgelehnt |

---

## 9. Umsetzungsreihenfolge (final)

1. **DNS bei Strato**: A-Record `obsidian.dirkbusmann.de` → VPS-IP anlegen
2. **Docker installieren** auf VPS
3. **Swap anlegen** (1–2 GB, Sicherheitspuffer)
4. **CouchDB starten** (Docker-Container, lokal gebunden, nicht direkt öffentlich)
5. **Nginx Reverse Proxy einrichten** für `obsidian.dirkbusmann.de`
6. **HTTPS einrichten** via Let's Encrypt / Certbot
7. **CouchDB absichern** (Admin-User, starkes Passwort, `.env`)
8. **LiveSync Plugin** auf einem Gerät installieren + Verbindung testen
9. **Verschlüsselung** (Passphrase) auf allen Geräten setzen
10. **Erstsync** (Mac-Vault führend)
11. **Weitere Geräte anbinden**
12. **Backup** einrichten
13. **Monitoring** einrichten

---

## Offene Punkte (nach Klärungsgespräch)

| Punkt | Status |
|---|---|
| Externer Backup-Speicher | kein akuter Bedarf, offen für später |
| Fail2ban / Rate-Limit | optional, nach Inbetriebnahme prüfen |

---

*Erstellt am 13.04.2026 — alle Entscheidungen aus Planungsgespräch Dirk + Assistent*
