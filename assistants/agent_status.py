#!/usr/bin/env python3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def collect_assistants():
    assistants = []
    for assistant_dir in sorted([p for p in BASE_DIR.iterdir() if p.is_dir()]):
        status_path = assistant_dir / 'STATUS.json'
        config_path = assistant_dir / 'config.json'
        status = load_json(status_path) or {}
        config = load_json(config_path) or {}
        assistants.append({
            'name': assistant_dir.name,
            'status': status.get('status', 'unknown'),
            'paused': status.get('paused', False),
            'stopped': status.get('stopped', False),
            'intervalMinutes': config.get('intervalMinutes'),
            'mode': config.get('mode'),
            'lastRun': status.get('lastRun'),
            'lastRunResult': status.get('lastRunResult'),
            'lastKnownAction': status.get('lastKnownAction'),
        })
    return assistants


def render_text():
    assistants = collect_assistants()
    lines = ['AgentStatus', '']
    if not assistants:
        lines.append('- Keine Assistenten gefunden')
        return '\n'.join(lines)

    for a in assistants:
        flags = []
        if a['paused']:
            flags.append('paused')
        if a['stopped']:
            flags.append('stopped')
        flag_text = f" ({', '.join(flags)})" if flags else ''
        lines.append(f"- {a['name']}")
        lines.append(f"  Status: {a['status']}{flag_text}")
        if a['intervalMinutes'] is not None:
            lines.append(f"  Intervall: {a['intervalMinutes']} Minuten")
        if a['mode']:
            lines.append(f"  Modus: {a['mode']}")
        if a['lastRun']:
            lines.append(f"  Letzter Lauf: {a['lastRun']}")
        if a['lastRunResult']:
            lines.append(f"  Letztes Ergebnis: {a['lastRunResult']}")
        if a['lastKnownAction']:
            lines.append(f"  Letzte Aktion: {a['lastKnownAction']}")
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'


if __name__ == '__main__':
    print(render_text())
