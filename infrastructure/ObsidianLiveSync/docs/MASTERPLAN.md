# ObsidianLiveSync – Gesamtvorhaben

## Zweck

Dieses Dokument beschreibt das komplette Vorhaben, Dirks Obsidian-Vaults über einen VPS bidirektional zu synchronisieren, sodass:

- Dirk auf seinen Geräten wie gewohnt mit Obsidian arbeitet
- der Assistent auf demselben Datenbestand lesen und schreiben kann
- neue Notizen des Assistenten automatisch auf Dirks Geräten erscheinen
- Änderungen von Dirks Geräten automatisch auf dem VPS ankommen
- das System dokumentiert, nachvollziehbar und rückbaubar bleibt

---

## 1. Zielbild

### Gewünschtes Ergebnis

Am Ende soll folgendes möglich sein:

1. Dirk erstellt oder ändert Notizen auf Mac, iPhone oder anderen Geräten
2. Diese Änderungen werden automatisch auf den VPS synchronisiert
3. Der Assistent kann auf dem VPS direkt auf den Vault zugreifen
4. Der Assistent kann neue Notizen anlegen oder bestehende ergänzen
5. Diese Änderungen werden automatisch zurück auf Dirks Geräte synchronisiert

### Wichtig

Das Ziel ist **kein einmaliger Export** und **keine statische Kopie**.
Es geht um einen **dauerhaften, bidirektionalen Sync**.

---

## 2. Warum nicht Obsidian Sync

### Obsidian Sync
Obsidian Sync ist der offizielle, bezahlte Cloud-Dienst von Obsidian.

Vorteile:
- sehr einfach
- offiziell unterstützt
- wenig technische Komplexität

Nachteile für dieses Vorhaben:
- läuft nicht als selbst gehostete Server-Instanz auf dem VPS
- der VPS kann nicht einfach als „Obsidian-Sync-Server“ verwendet werden
- der Assistent hat dadurch keinen sauberen, serverseitigen Zugriff auf den zentralen synchronisierten Datenbestand

### Schlussfolgerung
Für das Ziel „VPS als gemeinsame Zentrale für Dirk + Assistent“ ist **Obsidian Sync nicht die passende Architektur**.

---

## 3. Warum Obsidian LiveSync

### Obsidian LiveSync
Obsidian LiveSync ist eine self-hosted Synchronisationslösung für Obsidian, die typischerweise mit **CouchDB** arbeitet.

### Vorteile
- self-hosted auf dem eigenen VPS
- keine Abhängigkeit vom offiziellen Obsidian-Sync-Dienst
- bidirektionale Synchronisation
- geeignet für mehrere Geräte
- der VPS kann zentraler Datenknoten sein
- der Assistent kann lokal mit den Dateien auf dem VPS arbeiten

### Nachteile
- technischer in Einrichtung und Betrieb
- saubere Sicherheitskonfiguration nötig
- Backups und Monitoring sind wichtiger als bei Managed-Diensten

### Schlussfolgerung
Für dieses Vorhaben ist **Obsidian LiveSync + CouchDB auf dem VPS die passende Lösung**.

---

## 4. Geplante Architektur

## Komponenten

### A. VPS
Der VPS übernimmt folgende Aufgaben:
- Host für CouchDB
- Host für den Obsidian-Vault
- Arbeitsumgebung für den Assistenten
- optional Reverse-Proxy-Endpunkt für abgesicherten Zugriff

### B. CouchDB
CouchDB dient als Synchronisationsdatenbank für LiveSync.

### C. Obsidian auf Dirks Geräten
Auf den Geräten läuft:
- Obsidian App
- Community Plugin: Self-hosted LiveSync

### D. Assistent
Der Assistent arbeitet serverseitig mit dem Vault auf dem VPS.

---

## 5. Aktueller Ist-Zustand des VPS

Bei der Prüfung wurde festgestellt:

- OS: Ubuntu 24.04.4 LTS
- Kernel: Linux 6.8
- CPU: 2 vCPU
- RAM: 3.7 GiB gesamt
- verfügbar bei Prüfung: ca. 2.2 GiB
- Swap: nicht vorhanden
- freier Speicher: ca. 31 GiB
- Docker: nicht installiert
- Podman: nicht installiert
- UFW: nicht installiert bzw. nicht aktiv
- sichtbare Dienste: SSH öffentlich, OpenClaw/LiteLLM lokal gebunden

### Bewertung
Der Server ist **grundsätzlich geeignet**, aber nicht sofort betriebsbereit für LiveSync.

---

## 6. Risiken und Engpässe

### 6.1 RAM
CouchDB ist nicht extrem schwergewichtig, braucht aber stabilen RAM.

Bewertung:
- grundsätzlich machbar
- bei Parallelbetrieb mit weiteren Diensten begrenzter Puffer

Empfehlung:
- kleine Swap-Datei anlegen
- Ressourcenverbrauch nach Inbetriebnahme beobachten

### 6.2 Kein Docker/Podman
Es gibt noch keine Container-Laufzeit.

Empfehlung:
- Docker installieren
- Installation dokumentieren
- genaue Version und Konfiguration festhalten

### 6.3 Kein aktiver Host-Firewall-Standard
Wenn CouchDB falsch veröffentlicht wird, wäre das unnötig riskant.

Empfehlung:
- CouchDB nicht direkt offen ins Internet hängen
- möglichst nur via Reverse Proxy und HTTPS erreichbar machen
- Exponierung bewusst minimieren

### 6.4 Kein Backup-Konzept aktiv für dieses Vorhaben
Ohne Backup ist ein Notes-System zu fragil.

Empfehlung:
- Backup-Pfad für CouchDB-Daten und Vault definieren
- Rückbau- und Sicherungsstrategie dokumentieren

---

## 7. Sicherheitsprinzipien

Für dieses Vorhaben gelten folgende Sicherheitsprinzipien:

1. **Keine unnötig offenen Ports**
2. **CouchDB nicht ungeschützt öffentlich freigeben**
3. **starke Admin-Zugangsdaten verwenden**
4. **Reverse Proxy mit HTTPS bevorzugen**
5. **vor jeder Änderung Backup/Bestandsaufnahme**
6. **jede Änderung dokumentieren**
7. **Rückbaukommandos mitführen**
8. **Zugangsdaten niemals im Git-Repo speichern**
9. **Datenpfade und Konfigurationen klar trennen**
10. **erst klein und sauber aufbauen, dann erweitern**

---

## 8. Sicherheitsaspekte im Detail

## 8.1 Netzwerkfreigabe
### Schlechte Variante
- Port 5984 direkt öffentlich erreichbar
- Basic-Setup ohne weitere Absicherung

### Bessere Variante
- CouchDB nur lokal oder intern binden
- Nginx oder vergleichbaren Reverse Proxy davor setzen
- Zugriff nur über HTTPS
- wenn möglich zusätzlich IP-/Zugriffsbegrenzung

### Empfehlung
**Reverse Proxy vorziehen**, statt CouchDB roh ins Internet zu hängen.

---

## 8.2 Zugangsdaten
Für CouchDB werden Admin-Credentials benötigt.

Regeln:
- starkes, zufälliges Passwort
- nicht im Repo speichern
- nur in lokaler Systemkonfiguration / Secret-Datei / Env-Datei mit restriktiven Rechten
- Ablageort dokumentieren, aber Secret selbst nicht committen

---

## 8.3 Datenpersistenz
CouchDB-Daten und Vault-Daten müssen persistent gespeichert werden.

Erforderlich:
- klar definierte Host-Pfade
- dokumentierte Volume-Mounts
- vor Änderungen Sicherung der Persistenzpfade

---

## 8.4 Assistentenrechte
Der Assistent soll auf den Vault zugreifen können, aber das System nicht unkontrolliert verändern.

Daher:
- keine automatischen Löschroutinen
- keine großflächigen Umstrukturierungen ohne Auftrag
- neue Inhalte bevorzugt in definierte Zielordner oder Inbox schreiben
- Betriebsregeln separat dokumentieren

---

## 8.5 Backups
Empfohlen:
- Backup der CouchDB-Daten
- Backup des Vault-Dateibaums
- optional Git-basierte zusätzliche Sicherung für nicht-sensitive Strukturdateien

Backups müssen klären:
- was wird gesichert?
- wie oft?
- wohin?
- wie wird zurückgespielt?

---

## 8.6 Rückbau
Jeder Schritt muss rückbaubar sein.

Dokumentiert werden müssen:
- installierte Pakete
- erzeugte Container
- erzeugte Volumes und Datenpfade
- geänderte Proxy-Dateien
- geöffnete Ports
- Dienste und Autostarts

---

## 9. Geplante Verzeichnis- und Projektdokumentation

Bereits angelegt unter:
`infrastructure/ObsidianLiveSync/`

### Aktuelle Struktur
- `README.md`
- `docs/PLAN.md`
- `docs/BASELINE.md`
- `rollback/ROLLBACK.md`
- `config/STATE.json`

### Zweck
- Planung sauber festhalten
- Ist-Zustand dokumentieren
- Rückbau dokumentieren
- Status maschinenlesbar mitführen

---

## 10. Bisher vorbereitete Vault-Struktur

Auf dem VPS wurde bereits ein vorbereiteter Vault-Pfad angelegt:

`/root/.openclaw/workspace/obsidian/DirkVault`

Mit diesen Bereichen:
- `00 Inbox`
- `01 Projekte`
- `02 Wissen`
- `03 Personen`
- `04 Journal`
- `99 Admin`
- `.obsidian`

Wichtig:
Das ist nur ein vorbereitetes Landefeld. Der spätere echte produktive Vault kann diese Struktur ganz oder teilweise ersetzen.

---

## 11. Umsetzung in Phasen

## Phase 0 – Planung und Dokumentation
### Ziel
Noch keine Systemänderung. Nur Planung, Baseline, Rückbaupfad.

### Status
Bereits erfolgt.

### Ergebnisse
- Projektname definiert: `ObsidianLiveSync`
- Repo-Struktur angelegt
- Baseline dokumentiert
- Rückbau-Datei angelegt

---

## Phase 1 – Laufzeit vorbereiten
### Ziel
Server in einen Zustand bringen, auf dem LiveSync sauber betrieben werden kann.

### Schritte
1. Docker installieren
2. Docker-Version dokumentieren
3. optional: 1–2 GB Swap anlegen
4. Änderungen dokumentieren
5. Vorher/Nachher-Zustand sichern

### Sicherheitsaspekte
- nur notwendige Pakete installieren
- Systemänderungen protokollieren
- Rückbaukommandos ergänzen

### Warum Swap empfohlen ist
Der VPS hat keinen Swap. Bei Speicherdruck kann das zu unnötigen Problemen führen. Eine kleine Swap-Datei dient als Sicherheitspuffer.

---

## Phase 2 – CouchDB aufsetzen
### Ziel
Die LiveSync-Datenbank auf dem VPS bereitstellen.

### Schritte
1. persistenten Datenpfad festlegen
2. Konfigurationspfad festlegen
3. Secret-/Env-Handling definieren
4. CouchDB-Container starten
5. Erreichbarkeit intern testen
6. Admin-Zugang absichern
7. Betriebszustand dokumentieren

### Geplante Einstellungen
- definierter Containername
- persistente Volumes
- restriktive Rechte
- Admin-Benutzer + starkes Passwort
- kein unnötig offener Direktzugriff

### Sicherheitsaspekte
- keine Secrets im Git
- keine unkontrollierte Außenfreigabe
- Logging und Pfade dokumentieren

---

## Phase 3 – Sichere Erreichbarkeit
### Ziel
CouchDB so bereitstellen, dass Dirks Geräte zuverlässig synchronisieren können.

### Varianten
#### Variante A – Direktzugriff auf CouchDB-Port
- einfacher
- aber schlechtere Sicherheitslage

#### Variante B – Reverse Proxy mit HTTPS
- sauberer
- besser kontrollierbar
- empfehlenswert

### Empfehlung
**Variante B**

### Schritte
1. Domain/Subdomain oder feste Zieladresse festlegen
2. Nginx oder vorhandenen Reverse Proxy konfigurieren
3. HTTPS aktivieren
4. Zugriff testen
5. Konfiguration dokumentieren

---

## Phase 4 – Geräte anbinden
### Ziel
Dirks bestehende Vaults mit dem VPS koppeln.

### Schritte
1. auf den Geräten das Community Plugin **Self-hosted LiveSync** installieren
2. Verbindungsdaten eintragen
3. initiale Synchronisation sauber planen
4. Konfliktverhalten beobachten
5. Testnotizen in beide Richtungen anlegen

### Wichtig
Hier muss sauber entschieden werden:
- welcher Vault ist die führende Ausgangsbasis?
- wie erfolgt der erste Sync?
- wie werden Konflikte vermieden?

---

## Phase 5 – Betriebsregeln für den Assistenten
### Ziel
Definieren, wie der Assistent im Vault arbeiten darf.

### Beispiele
- ungeklärte Inhalte in `00 Inbox`
- Projektwissen in `01 Projekte`
- Personenwissen nur gezielt in `03 Personen`
- Tageslog in `04 Journal`
- technische Metadaten in `99 Admin`

### Zusätzliche Regeln
- keine automatischen Löschungen
- keine unaufgeforderten Massenumbauten
- Änderungen nachvollziehbar halten

---

## 12. Offene Entscheidungen

Vor der echten Umsetzung sind noch Entscheidungen sinnvoll:

1. **Docker ja oder Podman?**
   - aktuelle Empfehlung: Docker

2. **Swap ja oder nein?**
   - aktuelle Empfehlung: ja, klein (1–2 GB)

3. **CouchDB direkt oder hinter Reverse Proxy?**
   - aktuelle Empfehlung: Reverse Proxy

4. **Welche Adresse/Domain soll genutzt werden?**
   - noch offen

5. **Wie sollen Credentials verwaltet werden?**
   - noch offen, aber nicht im Git

6. **Wie soll Backup konkret aussehen?**
   - noch offen

7. **Wie erfolgt die Erstkopplung des bestehenden Vaults?**
   - noch offen, muss sauber geplant werden

---

## 13. Empfohlene Zielkonfiguration

Wenn ich das Vorhaben heute sauber bauen würde, wäre die Zielkonfiguration:

### Server
- Ubuntu 24.04
- Docker installiert
- kleine Swap-Datei aktiv

### Sync-Layer
- CouchDB im Docker-Container
- persistente Datenhaltung auf Host-Pfaden
- Admin-Zugang über starke Credentials

### Exponierung
- Reverse Proxy mit HTTPS
- kein offener roher CouchDB-Port ins Internet, wenn vermeidbar

### Obsidian
- Self-hosted LiveSync Plugin auf allen Geräten
- VPS als zentrale Sync-Instanz

### Betrieb
- dokumentierte Konfiguration
- dokumentierter Rückbau
- definierte Regeln für Assistenten-Schreibzugriffe

---

## 14. Was bereits entschieden wurde

Folgende Punkte sind bereits klar:

- keine einmalige statische Kopie
- echter bidirektionaler Sync ist Pflicht
- Obsidian Sync wird dafür nicht verwendet
- LiveSync ist die bevorzugte Lösung
- alles soll dokumentiert werden
- alles soll unter dem Namen `ObsidianLiveSync` geführt werden
- Rückbau muss jederzeit möglich sein
- jede Änderung soll nachvollziehbar bleiben

---

## 15. Was noch nicht gemacht wurde

Wichtig zur Einordnung:

**Bisher wurden noch keine systemverändernden Schritte für LiveSync ausgeführt.**

Noch nicht erfolgt:
- kein Docker installiert
- kein Swap angelegt
- kein CouchDB gestartet
- kein Reverse Proxy eingerichtet
- kein Port geöffnet
- kein Secret erzeugt
- kein Gerät verbunden

---

## 16. Vorschlag für die Freigabe-Reihenfolge

Wenn das Dokument freigegeben ist, würde ich die Umsetzung in genau dieser Reihenfolge starten:

1. Docker installieren
2. optional kleine Swap-Datei anlegen
3. Basis-Konfigurations- und Datenpfade definieren
4. CouchDB-Container lokal starten
5. Zugang absichern
6. Reverse Proxy/HTTPS einrichten
7. LiveSync auf einem Gerät testen
8. dann weitere Geräte anbinden
9. Betriebsregeln für den Assistenten finalisieren
10. Backup/Monitoring ergänzen

---

## 17. Kurzfazit

Das Vorhaben ist **technisch sinnvoll und auf dem VPS grundsätzlich machbar**.

Die saubere Lösung ist:
- **Obsidian LiveSync statt Obsidian Sync**
- **CouchDB auf dem VPS**
- **sichere Exponierung**
- **vollständige Dokumentation und Rückbaubarkeit**

Für die Umsetzung sollten wir bewusst konservativ vorgehen:
- erst Baseline
- dann minimale Systemänderungen
- dann abgesicherte Datenbank
- dann Geräteanbindung
- dann Betriebsregeln

---

## 18. Zugehörige Dateien im Projekt

- `infrastructure/ObsidianLiveSync/README.md`
- `infrastructure/ObsidianLiveSync/docs/PLAN.md`
- `infrastructure/ObsidianLiveSync/docs/BASELINE.md`
- `infrastructure/ObsidianLiveSync/docs/MASTERPLAN.md`
- `infrastructure/ObsidianLiveSync/rollback/ROLLBACK.md`
- `infrastructure/ObsidianLiveSync/config/STATE.json`
