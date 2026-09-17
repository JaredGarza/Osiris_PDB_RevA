"""Run the full active suite against the chosen protection candidate.

Mirrors every final_*.cir onto pdb_hvd.lib and adds INA228 analog pin-floor
measurements to the fault decks, which the original decks never instrumented.
Screening only -- PASS here is not hardware qualification.
"""
from pathlib import Path
import re
import sys, json

H = Path(__file__).resolve().parent
S = H.parents[0] / 'combined-20260915'
sys.path.insert(0, str(S))
import verify_all as v
import build_hv_lib

LTSPICE = Path(r'C:/Program Files/ADI/LTspice/LTspice.exe')
VARIANT = sys.argv[1] if len(sys.argv) > 1 else 'D'

SENSOR_MEAS = """.meas TRAN INP_MIN MIN V(XPDB:INA_IN_P)
.meas TRAN INN_MIN MIN V(XPDB:INA_IN_N)
.meas TRAN VBUS_MIN MIN V(XPDB:INA_VBUS)
"""
SENSOR_SAVE = '.save V(XPDB:INA_IN_P) V(XPDB:INA_IN_N) V(XPDB:INA_VBUS)\n'


def saves(text):
    """Build a .save block covering every signal the deck's .meas lines use.

    LTspice does not retain internal subcircuit nodes unless they are named in
    a .save, so measuring XPDB:INA_* requires one. But adding a .save also
    restricts the run to exactly what it lists, which would starve the deck's
    existing measurements -- so the list is derived from those measurements
    rather than guessed. A deck that already has .save only needs the new pins.
    """
    if '\n.save' in text:
        return SENSOR_SAVE
    nodes = {'XPDB:INA_IN_P', 'XPDB:INA_IN_N', 'XPDB:INA_VBUS'}
    currents = set()
    for line in text.splitlines():
        if not line.lower().startswith('.meas'):
            continue
        for m in re.finditer(r'\bV\(([^)]*)\)', line, re.I):
            nodes.update(p.strip() for p in m[1].split(','))
        for m in re.finditer(r'\bI\(([^)]*)\)', line, re.I):
            currents.add(m[1].strip())
    out = ' '.join(f'V({n})' for n in sorted(nodes) if n)
    out += ' ' + ' '.join(f'I({c})' for c in sorted(currents) if c)
    return f'.save {out.strip()}\n'

DECKS = ['final_corners', 'final_lowtrip', 'final_temperature',
         'final_faults', 'final_faults_fine', 'final_reverse',
         'final_reverse25', 'final_weak_source']


def main():
    lib = build_hv_lib.build(VARIANT)
    print('built', lib.name, flush=True)
    results, tag = [], VARIANT.lower()
    for base in DECKS:
        s = (S / f'{base}.cir').read_text()
        s = s.replace('pdb_final.lib', f'pdb_hv{tag}.lib')
        if 'INP_MIN' not in s:
            s = s.replace('\n.end', '\n' + SENSOR_MEAS + saves(s) + '.end')
        name = f'hv{tag}_{base[len("final_"):]}'
        (S / f'{name}.cir').write_text(s)
        r = v.run(S / f'{name}.cir', LTSPICE, 600)
        results.append(r)
        print(f"{name:<28} {r['status']:<8} {r['seconds']:>7}s", flush=True)
        for e in r['errors'][:8]:
            print('    ', e, flush=True)
        (H / f'hv{tag}-suite.json').write_text(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
