# Baseline – Zustand vor Einrichtung

## Systemzustand bei Erstprüfung

- OS: Ubuntu 24.04.4 LTS
- Kernel: Linux 6.8
- CPU: 2 vCPU
- RAM: 3.7 GiB gesamt
- Frei/Verfügbar bei Prüfung: ca. 2.2 GiB verfügbar
- Swap: nicht vorhanden
- Root-Dateisystem: 38 GiB, davon ca. 31 GiB frei
- Docker: nicht installiert
- Podman: nicht installiert
- UFW: nicht installiert bzw. nicht aktiv
- Listening Ports sichtbar: SSH auf 22, OpenClaw Gateway lokal, LiteLLM lokal

## Bewertung

- Für Obsidian LiveSync grundsätzlich geeignet
- Engpass-Risiko eher bei RAM/fehlendem Swap
- Container-Laufzeit muss erst installiert werden
- Netzwerkfreigabe muss bewusst und sparsam erfolgen

## Noch keine Änderungen erfolgt

Zum Zeitpunkt dieser Baseline wurden noch keine systemverändernden Maßnahmen für ObsidianLiveSync durchgeführt.
