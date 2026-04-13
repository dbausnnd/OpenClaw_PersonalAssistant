# 🔍 ObsidianLiveSync — Antworten auf Detailbedarf

> Basierend auf DETAILBEDARF.md vom 13.04.2026

---

## 1. OpenClaw-Zugriff auf den Vault

### Empfohlener Ansatz: Dateisystemzugriff

OpenClaw greift **nicht über die CouchDB-API** auf den Vault zu,
sondern direkt über das **Dateisystem** des VPS.

Das ist der sauberste und robusteste Weg:
- kein Abhängigkeitsproblem mit CouchDB-Protokoll oder LiveSync-Internas
- einfache, nachvollziehbare Lese- und Schreiboperationen
- keine proprietären Schnittstellenänderungen bei LiveSync-Updates

### Vault-Pfad

Der Vault liegt auf dem VPS unter:

```
/root/.openclaw/workspace/obsidian/DirkVault/
```

Dieser Pfad wird dem Assistenten bekannt gemacht durch:
- Eintrag in der Vault-Konfiguration (`config/STATE.json`)
- bei Bedarf zusätzlich als Umgebungsvariable in OpenClaw-Konfiguration

### Dateisystemrechte

Der Assistent läuft als `root` auf dem VPS.
Zur sauberen Trennung werden folgende Rechte empfohlen:

```
Vault-Besitzer: root
Schreibrecht: nur auf freigegebene Ordner
Lesrecht: auf gesamten Vault
```

Eine Umsetzung über feste Verzeichnisrechte mit `chmod` / `chown` ist sinnvoll,
sobald die endgültige Ordnerstruktur feststeht.

---

## 2. Schreibregeln für OpenClaw

### Grundregel
Der Assistent schreibt **standardmäßig nur in `00 Inbox`**, sofern nicht ausdrücklich anders beauftragt.

### Schreibregel-Matrix

| Ordner | Lesen | Schreiben (automatisch) | Schreiben (auf Auftrag) |
|---|---|---|---|
| `00 Inbox` | ✅ | ✅ | ✅ |
| `01 Projekte` | ✅ | ❌ | ✅ |
| `02 Wissen` | ✅ | ❌ | ✅ |
| `03 Personen` | ✅ | ❌ | ✅ |
| `04 Journal` | ✅ | ❌ | ✅ |
| `99 Admin` | ✅ | ❌ | ✅ |

### Technische Durchsetzung

Zwei Varianten — empfohlen wird Variante B:

**Variante A: Nur dokumentiert**
Die Regeln sind als Konvention festgehalten (ASSISTANT_RULES.md). Der Assistent hält sie ein.

**Variante B: Teilweise technisch erzwungen (empfohlen)**
Für `00 Inbox` gibt es dedizierte Schreibrechte. Andere Ordner werden mit eingeschränkten Rechten belegt.
Wenn der Assistent dort schreiben will, muss ein expliziter Auftrag vorliegen.

### Weitere Regeln
- keine bestehenden Dateien ohne Auftrag löschen
- keine Massenumstrukturierungen ohne Auftrag
- neue Inhalte aus Mails oder anderen Quellen → immer zuerst in `00 Inbox`
- Betriebsregeln werden in `99 Admin/ASSISTANT_RULES.md` gepflegt

---

## 3. Erstkopplung des echten Vaults

### Führender Stand: Mac-Vault

Der Mac-Vault ist führend. Beim ersten Sync gewinnt der Mac.
Der vorbereitete VPS-Vault ist nur ein Landefeld — er kann vollständig überschrieben werden.

### Geplanter Ablauf Erstkopplung

1. **Backup VPS-Vault** (vorbereitete Struktur sichern, bevor sie überschrieben wird)
2. **Backup Mac-Vault** (Snapshot des Ist-Zustands vor dem ersten Sync)
3. LiveSync auf dem Mac auf **„Initial Setup: Rebuild server data"** setzen
4. erste Synchronisation beobachten
5. prüfen, ob alle Dateien korrekt auf VPS angekommen sind
6. erst dann weiteres Gerät koppeln

### Zu vermeiden beim Erstsync
- LiveSync **nicht gleichzeitig auf mehreren Geräten** aktivieren
- immer erst ein Gerät koppeln, testen, dann das nächste

### Validierung
- Dateianzahl auf VPS mit Dateianzahl auf Mac vergleichen
- Stichprobenkontrolle einiger Notizen auf inhaltliche Integrität

---

## 4. Konfliktverhalten bei gleichzeitigen Änderungen

### Wie Konflikte entstehen
LiveSync erkennt Konflikte und markiert betroffene Dateien mit dem Suffix `_conflicted`.

### Erkennungsstrategie
- `_conflicted`-Dateien sind im Vault als separate Dateien sichtbar
- Obsidian zeigt sie ganz normal an
- optional: tägliche Suche nach `_conflicted` im Vault-Pfad auf dem VPS

### Auflösung
- Dirk entscheidet, welche Version korrekt ist (manuell)
- kein automatisches Überschreiben ohne Rückmeldung
- der Assistent **löst Konflikte nicht autonom auf**

### Prävention durch OpenClaw
- der Assistent schreibt **nur in `00 Inbox`** automatisch
- keine Aktionen auf Dateien, die Dirk gerade aktiv bearbeitet
- wenn ein Schreibauftrag zu einer bestehenden Datei kommt, Datei zuerst lesen und prüfen

### Benachrichtigung bei Konflikten
- optional: der Assistent prüft periodisch auf `_conflicted`-Dateien im Vault
- bei Fund: Hinweis an Dirk per Telegram

---

## 5. Backup-Konzept

### Was wird gesichert
1. CouchDB-Datenpfad (CouchDB-Volume)
2. Vault-Dateipfad auf dem VPS
3. alle Konfigurationsdateien (docker-compose, env, proxy)

### Häufigkeit
- täglich (empfohlen)
- zusätzlich: immer vor größeren Konfigurationsänderungen

### Wohin
- primär: lokaler Backup-Pfad auf dem VPS (z. B. `/root/backups/obsidian/`)
- empfohlen zusätzlich: externer Speicher oder S3-kompatibler Dienst

### Rückspielen (Grundprinzip)
1. CouchDB-Container stoppen
2. Vault-Pfad ersetzen durch Backup-Stand
3. CouchDB-Volume ersetzen durch Backup-Stand
4. Container neu starten
5. LiveSync auf einem Gerät testen

### Vollständige Rückspielprozedur
Wird in `rollback/ROLLBACK.md` ergänzt, sobald die echte Konfiguration steht.

### Verifizierung
- nach jeder Backup-Erstellung: Datei- und Ordneranzahl prüfen
- wöchentlich: stichprobenartig eine Datei aus dem Backup lesen

---

## 6. Credential-Management

### Grundregel
**Keine Secrets im Git-Repo.**

### Speicherort `.env`
- Pfad: `/root/OpenClaw_PersonalAssistant/infrastructure/ObsidianLiveSync/config/.env`
- Rechte: `600` (nur root liest und schreibt)
- `.env` steht in `.gitignore` — wird nie committet

### Passwortgenerierung
Empfehlung: sicheres Zufallspasswort generieren, z. B.:

```bash
openssl rand -base64 32
```

### Wer kennt das Passwort
- liegt lokal auf dem VPS in `.env`
- Dirk sollte es an sicherer Stelle außerhalb des Servers notieren (Passwortmanager empfohlen)

### Passwort-Rotation
- noch kein fester Turnus definiert
- bei Bedarf: neues Passwort generieren, CouchDB-Admin aktualisieren, Geräte neu verbinden

### `.gitignore` Eintrag
Folgendes wird in `.gitignore` ergänzt:

```
infrastructure/ObsidianLiveSync/config/.env
infrastructure/ObsidianLiveSync/config/*.env
infrastructure/ObsidianLiveSync/backups/
```

---

## 7. Reverse Proxy Konfiguration

### Empfohlener Reverse Proxy
Nginx — wird auf dem VPS am häufigsten eingesetzt, gut dokumentiert.

Falls bereits ein Nginx-Prozess auf dem VPS läuft: prüfen und ggf. erweitern.

### Domain / Subdomain
**Entschieden:** `obsidian.dirkbusmann.de`

- bestehende Domain bei Strato: `dirkbusmann.de`
- Hauptdomain bleibt unberührt (zeigt weiterhin auf Synology)
- DNS-Eintrag: A-Record `obsidian` → VPS-IP

### HTTPS
- Let's Encrypt via Certbot (kostenfrei, weit verbreitet)
- Certbot kann direkt auf dem VPS installiert werden

### Zusätzliche Absicherung
- **IP-Filter: abgelehnt** (mobile Geräte mit wechselnden IPs)
- Sicherheit stattdessen über: CouchDB-Auth + HTTPS + LiveSync-Passphrase + Nginx

### Konfigurationsdateien
Nginx-Konfig-Datei wird nach Erstellung gesichert unter:
`infrastructure/ObsidianLiveSync/config/nginx-couchdb.conf`

Dieses Template wird im Repo gehalten (kein Secret darin).

---

## 8. Monitoring und Betriebszustand

### CouchDB-Laufzeitprüfung
```bash
docker ps | grep couchdb
curl -s http://localhost:5984/
```

Gibt CouchDB-Status zurück, wenn der Container läuft.

### Sync-Aktivitätsprüfung
- LiveSync-Status ist direkt in der Obsidian-App auf den Geräten sichtbar
- optional: periodische Prüfung des letzten Änderungszeitstempels im Vault-Pfad

### Alerts bei Ausfall
- optional: der Assistent prüft periodisch per Heartbeat ob CouchDB antwortet
- bei Ausfall: Hinweis an Dirk per Telegram

### RAM und Speicher
- Heartbeat-fähige Prüfung:

```bash
free -h
df -h /
```

- empfohlen: regelmäßige Beobachtung in den ersten Wochen

### Stabilitätskriterium
Das System gilt als „stabil in Betrieb" wenn:
- CouchDB läuft ohne Unterbrechungen über 7 Tage
- Sync zwischen allen Geräten funktioniert in beide Richtungen
- kein unerwarteter RAM-Anstieg oder Platzmangel

---

## Entschiedene Punkte (Stand 13.04.2026)

| Punkt | Entscheidung |
|---|---|
| Domain / Subdomain | `obsidian.dirkbusmann.de` |
| Passwort-Rotation | bei Bedarf |
| Backup-Speicher | lokal auf VPS, extern optional später |
| IP-Filter | nein (Mobilgeräte) |
| Verschlüsselung | aktiv: HTTPS + LiveSync-Passphrase |
| Reverse Proxy | Nginx + Let's Encrypt, direkt von Anfang an |

---

*Erstellt am 13.04.2026*
