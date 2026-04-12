# WhatsAppAssistant – Verlauf

## 2026-04-11

- WhatsAppAssistant als Entwurfs-Assistent angelegt
- Startmodus festgelegt: Nutzer beschreibt Nachricht, Assistent formuliert sie
- Kein autonomer Versand
- Stilbindung über zentralen Skill `Dirk-Kommunikationsstil`
- Skill absichtlich kanalübergreifend angelegt (E-Mail, WhatsApp, Teams, Telegram)

### Planung: WhatsApp Deep-Link (vorbefüllter Text)
- Dirk wollte: formulierter Text erscheint direkt im WhatsApp-Chat, er klickt nur Senden
- Direkt in bestehenden Chat schreiben = fragil/inoffiziell → nicht empfohlen
- Sauberer Weg wäre: WhatsApp Deep-Link mit vorbefülltem Text (nur Einzelkontakte)
- Kontakt-Nummer-Problem: Gmail-Anbindung gibt keinen Zugriff auf Google-Adressbuch
- Optionen besprochen: manuelle Nummern / Google Contacts API / Repo-Kontaktliste
- **Entscheidung (2026-04-12): vorerst bei der aktuellen Entwurfslösung bleiben**
- Deep-Link und Kontakte-Integration geparkt — kann später aufgenommen werden
