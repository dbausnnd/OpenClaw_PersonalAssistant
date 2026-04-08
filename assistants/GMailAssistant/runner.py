#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / 'config.json'
STATUS_PATH = BASE_DIR / 'STATUS.json'
TOKEN_PATH = Path('/root/.openclaw/gmail/token.json')
LOG_PATH = BASE_DIR / 'logs' / 'runner.log'


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def log(msg: str):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open('a', encoding='utf-8') as f:
        f.write(f"[{now_iso()}] {msg}\n")


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def refresh_token(token: dict):
    resp = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': token['client_id'],
        'client_secret': token['client_secret'],
        'refresh_token': token['refresh_token'],
        'grant_type': 'refresh_token',
    }, timeout=30)
    resp.raise_for_status()
    new = resp.json()
    token['token'] = new['access_token']
    token['expiry'] = now_iso()
    write_json(TOKEN_PATH, token)
    return token


def gmail_headers(token: dict):
    return {'Authorization': f"Bearer {token['token']}"}


def classify(fromv: str, subj: str, snippet: str) -> str:
    text = (fromv + ' ' + subj + ' ' + snippet).lower()
    if 'ds216+' in text or 'ds211j' in text or 'synology diskstation' in text:
        return '02 Systemmeldungen'
    if 'vitadock' in text or 'doreenbusmann@googlemail.com' in fromv:
        return '04 Wichtig / Persönlich'
    if any(x in text for x in ['lottery', 'crypto guaranteed', 'won prize']):
        return '01 Spam / Verdächtig'
    if any(x in text for x in ['invite', 'einladung', 'calendar', 'termin', 'meeting']):
        return '03 Termineinladungen'
    if ('github' in fromv and any(x in subj for x in ['verify', 'sudo', 'token', 'ssh authentication public key', 'google identity'])) or ('notion' in fromv and 'login code' in subj) or ('linkedin' in fromv and 'kontaktanfrage' in subj) or any(x in text for x in ['verification code', 'password reset', 'security alert', 'kontaktanfrage']):
        return '04 Wichtig / Persönlich'
    if ('über kleinanzeigen' in text or 'nutzer-anfrage zu deiner anzeige' in text or 'mail.kleinanzeigen.de' in fromv or 'ebay-kleinanzeigen.de' in fromv or 'amazon' in fromv or 'klarna' in fromv or 'klarmobil' in fromv or (('tm.openai.com' in fromv or 'tm1.openai.com' in fromv or 'openai.com' in fromv) and any(x in text for x in ['funded', 'charged', 'billing', 'receipt', 'invoice'])) or ('apple' in fromv and any(x in text for x in ['abo', 'rechnung', 'kauf', 'zahlung', 'bestellung', 'läuft ab'])) or 'rechnung' in subj or 'invoice' in subj or 'bestellung' in text or 'versendet' in subj or 'zustellung' in subj):
        return '05 Shopping'
    if any(x in text for x in ['openai', 'anthropic', 'claude', 'chatgpt', 'gpt', 'langdock', 'pictory', 'myclaw', 'reframe', 'artlist', 'gemini', 'ki', 'llm']):
        return '06 KI'
    if any(x in text for x in ['steam', 'epic games', 'playstation', 'xbox', 'nintendo', 'riot', 'blizzard', 'gaming', 'game']):
        return '07 Gaming'
    if ('linkedin' in fromv and ('job' in fromv or 'jobs' in fromv or 'messages-noreply' in fromv or 'profil besucht' in text or 'vernetzen' in text)):
        return '09 Unwichtig'
    return '08 Werbung / Newsletter'


def run():
    config = read_json(CONFIG_PATH)
    status = read_json(STATUS_PATH)
    if status.get('status') != 'active' or status.get('paused') or status.get('stopped'):
        status['lastRun'] = now_iso()
        status['lastRunResult'] = 'skipped: paused/stopped/inactive'
        status['lastUpdated'] = now_iso()
        write_json(STATUS_PATH, status)
        log('skipped run because assistant is not active')
        return

    token = read_json(TOKEN_PATH)
    auth = gmail_headers(token)
    base = 'https://gmail.googleapis.com/gmail/v1/users/me'

    def req(method, url, **kwargs):
        nonlocal token, auth
        headers = kwargs.pop('headers', {})
        merged = dict(auth)
        merged.update(headers)
        resp = requests.request(method, url, headers=merged, timeout=30, **kwargs)
        if resp.status_code == 401:
            token = refresh_token(token)
            auth = gmail_headers(token)
            merged = dict(auth)
            merged.update(headers)
            resp = requests.request(method, url, headers=merged, timeout=30, **kwargs)
        resp.raise_for_status()
        return resp

    labels = req('GET', f'{base}/labels').json()['labels']
    name_to_id = {x['name']: x['id'] for x in labels}
    our_label_ids = {lid for name, lid in name_to_id.items() if re.match(r'^0[1-9] ', name)}

    batch_size = int(config.get('batchSize', 50))
    msgs = req('GET', f'{base}/messages', params={'labelIds': 'INBOX', 'maxResults': batch_size}).json().get('messages', [])
    processed = 0
    archived = 0
    skipped = 0

    for m in msgs:
        d = req('GET', f'{base}/messages/{m['id']}', params={'format': 'metadata', 'metadataHeaders': ['From', 'Subject']}).json()
        current = set(d.get('labelIds', []))
        if config.get('processOnlyUnlabeled', True) and current & our_label_ids:
            skipped += 1
            continue
        hdr = {h['name'].lower(): h['value'] for h in d['payload'].get('headers', [])}
        fromv = hdr.get('from', '').lower()
        subj = hdr.get('subject', '').lower()
        label = classify(fromv, subj, d.get('snippet', ''))
        body = {'addLabelIds': [name_to_id[label]]}
        if label in set(config.get('autoArchiveLabels', [])) and 'INBOX' in current:
            body['removeLabelIds'] = ['INBOX']
            archived += 1
        req('POST', f'{base}/messages/{m['id']}/modify', headers={'Content-Type': 'application/json'}, data=json.dumps(body))
        processed += 1

    status['lastRun'] = now_iso()
    status['lastRunResult'] = f'processed={processed}, archived={archived}, skipped={skipped}'
    status['lastKnownAction'] = 'Automatischer 10-Minuten-Lauf ausgeführt'
    status['lastUpdated'] = now_iso()
    write_json(STATUS_PATH, status)
    log(status['lastRunResult'])


if __name__ == '__main__':
    run()
