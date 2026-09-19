"""Combine preserved vendor-model runs only while their source hashes still match."""
from pathlib import Path
import hashlib
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
reports = [
    ROOT / 'audit/verification-infineon-first-full.json',
    ROOT / 'audit/verification-infineon-temperature-transients.json',
    ROOT / 'audit/verification-infineon-isolated-transients.json',
]
active = json.loads((ROOT / 'active_decks.json').read_text())
selected, hashes = {}, {}
for path in reports:
    report = json.loads(path.read_text())
    for name, expected in report['sha256'].items():
        source = Path(name)
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise SystemExit(f'Stale evidence: {name}')
        hashes[name] = expected
    for result in report['results']:
        if result['deck'] in active:
            selected[result['deck']] = dict(result, evidence_report=str(path.relative_to(ROOT)))
missing = set(active) - selected.keys()
if missing:
    raise SystemExit(f'Missing results: {sorted(missing)}')
output = {
    'timestamp': datetime.now().astimezone().isoformat(),
    'scope': 'Consolidated electrical screening only; not hardware qualification',
    'source_reports': [str(p.relative_to(ROOT)) for p in reports],
    'sha256': hashes,
    'results': [selected[name] for name in active],
}
(ROOT / 'audit/verification-current-vendor.json').write_text(json.dumps(output, indent=2))
passed = sum(r['status'] == 'PASS' for r in selected.values())
print(f'{passed}/{len(active)} active decks pass; all recorded source hashes match.')
raise SystemExit(0 if passed == len(active) else 1)
