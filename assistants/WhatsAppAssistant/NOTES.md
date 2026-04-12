# WhatsAppAssistant – Gesprächsnotizen zur späteren Verarbeitung

## Aktueller Beschluss

Vorerst bleibt es bei der aktuellen Lösung:
- Dirk beschreibt Empfänger + Anliegen
- Der Assistent formuliert eine sendefertige Nachricht
- Dirk kopiert/sendet selbst

## Besprochene Erweiterung (geparkt)

### Zielbild
Der Assistent soll später optional einen WhatsApp-Deep-Link mit vorbefülltem Text erzeugen, damit Dirk nur noch den Chat öffnet und auf **Senden** klickt.

### Warum nicht sofort umgesetzt
- Direkt in bestehende private WhatsApp-Chats hineinschreiben ist technisch fragil und nicht empfehlenswert
- Die saubere Variante wäre ein Deep-Link mit vorbefülltem Text
- Dafür wird pro Einzelkontakt eine zuverlässige Telefonnummer benötigt

### Kontaktproblem
Die bestehende Gmail-Integration reicht dafür nicht aus:
- Gmail = Zugriff auf E-Mails
- Kein automatischer Zugriff auf Google Kontakte / Adressbuch
- Nummern aus Mail-Signaturen zu ziehen wäre unzuverlässig

## Besprochene Lösungswege

### Option A
Nummern manuell pflegen

### Option B
Google Kontakte / People API anbinden

### Option C
Kleine Kontaktliste im Repo pflegen

## Entscheidung Stand heute
- Deep-Link-Integration: **geparkt**
- Kontakte-Integration: **geparkt**
- Aktiver Modus bleibt: **draft-only**

## Wiederaufnahme später
Wenn das Thema wieder aufgenommen wird, als Nächstes entscheiden:
1. Woher kommen die Kontaktnummern? (A / B / C)
2. Nur Einzelkontakte oder später auch Gruppen?
3. Soll der Assistent Links nur erzeugen oder zusätzlich strukturierte Kontaktverwaltung bekommen?
