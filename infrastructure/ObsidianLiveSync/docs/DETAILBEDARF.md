# 🔍 ObsidianLiveSync — Punkte mit Detailbedarf

> Erstellt am 13.04.2026 | Obsidian (LIST)
> Diese Datei listet alle Planpunkte, die vor oder während der Umsetzung
> mit mehr Details versehen werden müssen.

---

## 1. OpenClaw-Zugriff auf den Vault

**Was fehlt:**
Konkrete technische Beschreibung, wie OpenClaw auf die Vault-Dateien zugreift.

**Zu klären:**
- Zugriff über Dateisystem (empfohlen) oder CouchDB-API?
- Welcher Systempfad wird OpenClaw bekannt gemacht?
- Lese- und Schreibrechte auf Dateiebene — wie gesetzt?
- Wird OpenClaw der Vault-Pfad als Umgebungsvariable übergeben oder fest konfiguriert?

---

## 2. Schreibregeln für OpenClaw

**Was fehlt:**
Konkrete, technisch erzwungene Schreibregeln — nicht nur dokumentierte Absichten.

**Zu klären:**
- In welche Ordner darf OpenClaw schreiben? (Vorschlag: nur `00 Inbox`)
- Darf OpenClaw bestehende Dateien ändern — und wenn ja, unter welchen Bedingungen?
- Wie wird verhindert, dass OpenClaw außerhalb erlaubter Pfade schreibt?
- Werden Schreibregeln über Dateisystemrechte (chmod/chown) oder über OpenClaw-Konfiguration umgesetzt?

---

## 3. Erstkopplung des echten Vaults

**Was fehlt:**
Schritt-für-Schritt-Plan für den initialen Sync zwischen Mac-Vault und VPS.

**Zu klären:**
- Welcher Stand ist führend? (Empfehlung: Mac-Vault)
- Was passiert mit dem vorbereiteten VPS-Vault beim ersten Sync?
- Wie wird LiveSync auf „Mac gewinnt" konfiguriert?
- Backup-Zeitpunkt: wann genau vor dem ersten Sync?
- Wie wird der erste Sync beobachtet und validiert?

---

## 4. Konfliktverhalten bei gleichzeitigen Änderungen

**Was fehlt:**
Konkrete Strategie für den Umgang mit LiveSync-Konflikten.

**Zu klären:**
- Wie erkennt man `_conflicted`-Dateien im Vault?
- Wer löst Konflikte auf — Dirk manuell oder automatische Regel?
- Gibt es eine Benachrichtigung bei Konflikten?
- Wie werden Konflikte zwischen OpenClaw-Schreibzugriffen und Dirks Änderungen verhindert?

---

## 5. Backup-Konzept

**Was fehlt:**
Konkreter, umsetzbarer Backup-Plan mit allen Details.

**Zu klären:**
- Was wird gesichert? (CouchDB-Volume, Vault-Dateipfad, Konfigurationsdateien)
- Wie oft? (Empfehlung: täglich)
- Wohin? (lokaler VPS-Pfad, externer Speicher, beides?)
- Wie wird zurückgespielt? (Schritt-für-Schritt-Anleitung)
- Wer prüft ob das Backup funktioniert?

---

## 6. Credential-Management

**Was fehlt:**
Konkretes Verfahren für Erstellung, Ablage und Rotation von Zugangsdaten.

**Zu klären:**
- Wo liegt die `.env`-Datei auf dem VPS? (Pfad, Rechte)
- Wie wird das CouchDB-Admin-Passwort generiert?
- Wer kennt das Passwort — und wo ist es sicher notiert (außerhalb des Servers)?
- Gibt es einen Plan für Passwort-Rotation?
- Wie wird sichergestellt, dass Secrets nie ins Git-Repo gelangen?

---

## 7. Reverse Proxy Konfiguration

**Was fehlt:**
Konkrete Konfiguration des Reverse Proxy für CouchDB.

**Zu klären:**
- Welcher Reverse Proxy wird genutzt? (Nginx, Caddy, vorhandener?)
- Welche Domain oder Subdomain wird verwendet?
- Wie wird HTTPS eingerichtet? (Let's Encrypt / Certbot?)
- Wird zusätzliche Zugangsbeschränkung eingerichtet? (IP-Filter, Basic Auth)
- Wie wird die Konfiguration dokumentiert und versioniert?

---

## 8. Monitoring und Betriebszustand

**Was fehlt:**
Plan für laufende Beobachtung des Systems nach Inbetriebnahme.

**Zu klären:**
- Wie wird geprüft ob CouchDB läuft?
- Wie wird geprüft ob der Sync aktiv ist?
- Gibt es Alerts bei Ausfall?
- Wie wird RAM- und Speicherverbrauch beobachtet?
- Wann gilt das System als „stabil in Betrieb"?

---

*Erstellt am 13.04.2026 | Obsidian (LIST)*
