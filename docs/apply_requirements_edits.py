"""Apply the decisions recorded in docs/osiris-power-audit/requirements-20260910.md.

D1 F1 -> 4 A, D2 gate network to LTC4368 Figure 11, D3 J2 -> 4-way GH matching
Osiris J28, D4 U3 fed from VBAT_FUSED, D5 bidirectional input TVS.

Idempotent: refuses to run twice. Deterministic UUIDs so re-runs after a restore
produce byte-identical output.
"""
from pathlib import Path
import re, shutil, uuid

root = Path(__file__).resolve().parents[1]
sch = root / 'Osiris_PDB_RevA.kicad_sch'
KSYM = Path('C:/Program Files/KiCad/10.0/share/kicad/symbols')
SHEET = '/6f58a31e-2d20-46d6-8900-dedce2deebb4'
NS = uuid.UUID('b9b6d4c2-0f7a-4a1e-9d1c-6f0e2a7c5311')

assert not (root / '~Osiris_PDB_RevA.kicad_sch.lck').exists(), 'Close the schematic editor first'
backup = root / 'requirements-backup-20260910'
assert not backup.exists(), 'Review or remove the existing backup before repeating'

raw = sch.read_bytes()
assert raw.count(b'\r\n') and b'\n' not in raw.replace(b'\r\n', b''), 'Expected pure CRLF source'
s = raw.decode('utf-8').replace('\r\n', '\n')
before = s

backup.mkdir()
for p in [sch, root / 'BOM.csv', root / 'BOM_purchasing.csv']:
    if p.exists():
        shutil.copy2(p, backup / p.name)

uid = lambda k: str(uuid.uuid5(NS, k))
SYMPAT = re.compile(r'^\t\(symbol\n.*?^\t\)', re.M | re.S)


def quote(t):
    return '"' + t.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'


def prop(block, key, val):
    """Set an existing property, or append a hidden one."""
    pat = r'(\(property "' + re.escape(key) + r'" )"(?:\\.|[^"\\])*"'
    if re.search(pat, block):
        return re.sub(pat, lambda m: m[1] + quote(val), block, count=1)
    at = re.search(r'\(at ([\d.-]+) ([\d.-]+)', block)
    new = (f'\n\t\t(property {quote(key)} {quote(val)}\n'
           f'\t\t\t(at {at[1]} {at[2]} 0)\n\t\t\t(hide yes)\n\t\t\t(show_name no)\n'
           f'\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n'
           f'\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)')
    return block[:-3] + new + '\n\t)'


# ---------------------------------------------------------------- lib_symbols
def system_symbol(libname, name):
    """Extract a top-level symbol block from a system .kicad_sym, re-indented."""
    text = (KSYM / f'{libname}.kicad_sym').read_text(encoding='utf-8')
    start = text.index(f'\t(symbol "{name}"\n')
    i, depth = start, 0
    while True:
        if text[i] == '"':                      # skip string literals
            i += 1
            while text[i] != '"':
                i += 2 if text[i] == '\\' else 1
        elif text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                break
        i += 1
    block = text[start:i + 1]
    block = block.replace(f'(symbol "{name}"', f'(symbol "{libname}:{name}"', 1)
    return '\n'.join('\t' + ln if ln.strip() else ln for ln in block.split('\n'))


wanted = [('Connector_Generic', 'Conn_01x04'), ('Device', 'D_TVS'), ('Device', 'D_Schottky')]
add_libs = ''
for lib, name in wanted:
    assert f'(symbol "{lib}:{name}"' not in s, f'{lib}:{name} already present'
    add_libs += system_symbol(lib, name) + '\n'
s = s.replace('\t(lib_symbols\n', '\t(lib_symbols\n' + add_libs, 1)

# ------------------------------------------------------------------ new nodes
def label(name, x, y, ang, key):
    just = 'right bottom' if ang == 180 else 'left bottom'
    return (f'\t(label {quote(name)}\n\t\t(at {x} {y} {ang})\n\t\t(effects\n'
            f'\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {just})\n'
            f'\t\t)\n\t\t(uuid "{uid(key)}")\n\t)\n')


def no_connect(x, y, key):
    return f'\t(no_connect\n\t\t(at {x} {y})\n\t\t(uuid "{uid(key)}")\n\t)\n'


def symbol(lib_id, ref, x, y, ang, props, pins, mirror=None, text_ang=0):
    """props entries are (key, value) for hidden fields, or (key, value, px, py, justify)
    for visible ones. Visible text is positioned explicitly, and text_ang compensates for
    the symbol rotation: KiCad adds the two, so a rotated body needs text_ang = -ang to
    keep its reference and value horizontal instead of running down the sheet."""
    out = [f'\t(symbol\n\t\t(lib_id {quote(lib_id)})\n\t\t(at {x} {y} {ang})']
    if mirror:
        out.append(f'\t\t(mirror {mirror})')
    out += ['\t\t(unit 1)', '\t\t(body_style 1)', '\t\t(exclude_from_sim no)',
            '\t\t(in_bom yes)', '\t\t(on_board yes)', '\t\t(in_pos_files yes)',
            '\t\t(dnp no)', f'\t\t(uuid "{uid(ref)}")']
    for entry in props:
        k, v = entry[0], entry[1]
        shown = len(entry) == 5
        px, py, just = entry[2:] if shown else (x, y, None)
        pang = text_ang if shown else 0
        out.append(f'\t\t(property {quote(k)} {quote(v)}\n\t\t\t(at {round(px,4)} {round(py,4)} {pang})')
        if not shown:
            out.append('\t\t\t(hide yes)')
        out.append('\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n'
                   '\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)'
                   + (f'\n\t\t\t\t(justify {just})' if shown else '') + '\n\t\t\t)\n\t\t)')
    for p in pins:
        out.append(f'\t\t(pin "{p}"\n\t\t\t(uuid "{uid(ref + ".pin" + p)}")\n\t\t)')
    out.append(f'\t\t(instances\n\t\t\t(project "Osiris_PDB_RevA"\n\t\t\t\t(path "{SHEET}"\n'
               f'\t\t\t\t\t(reference "{ref}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)')
    return '\n'.join(out) + '\n\t)\n'


def gnd(ref, x, y, ang):
    return symbol('power:GND', ref, x, y, ang, [
        ('Reference', ref), ('Value', 'GND'), ('Footprint', ''), ('Datasheet', ''),
        ('Description', 'Power symbol creates a global label with name "GND" , ground'),
    ], ['1'])


DS = '${KIPRJMOD}/Datasheets/'
new = ''

# D5 - bidirectional input clamp on VBAT_FUSED (pin A1 up, A2 down at rot 270)
new += symbol('Device:D_TVS', 'D1', 50.8, 34.29, 270, [
    ('Reference', 'D1', 55.88, 33.02, 'left'), ('Value', 'SMAJ24CA', 55.88, 35.56, 'left'),
    ('Footprint', 'Diode_SMD:D_SMA'), ('Datasheet', DS + 'Bourns_SMAJ_TVS.pdf'),
    ('Description', 'Bidirectional 400 W TVS; 24 V standoff, 26.7 V min breakdown, 38.9 V clamp'),
    ('Manufacturer', 'Bourns'), ('MPN', 'SMAJ24CA'),
    ('Selection_Status', 'Bidirectional so reverse-battery blocking is preserved; breakdown clears the 19.33 V worst-case OV corner and the clamp stays below the 60 V MOSFET rating'),
], ['1', '2'], text_ang=90)
new += label('VBAT_FUSED', 50.8, 30.48, 0, 'D1.k')
new += gnd('#PWR017', 50.8, 38.1, 0)

# D2 - Schottky across R4 so the fast gate pull-down bypasses it (K down, A up at rot 90)
new += symbol('Device:D_Schottky', 'D2', 50.8, 120.65, 90, [
    ('Reference', 'D2', 45.72, 119.38, 'right'), ('Value', 'MBR0540', 45.72, 121.92, 'right'),
    ('Footprint', 'Diode_SMD:D_SOD-123'), ('Datasheet', DS + 'onsemi_MBR0540.pdf'),
    ('Description', '40 V 0.5 A Schottky across R4; cathode to the U1 GATE side'),
    ('Manufacturer', 'onsemi'), ('MPN', 'MBR0540T1G'),
    ('Selection_Status', 'Required by the LTC4368 Figure 11 gate network; without it fault turn-off degrades from 8 us to about 300 us'),
], ['1', '2'], text_ang=270)
new += label('GATE_FET', 50.8, 116.84, 0, 'D2.a')
new += label('GATE_PIN', 50.8, 124.46, 0, 'D2.k')

# C9 - output bulk on PDB_VOUT, replacing the role C4 had before D4 moved it
new += symbol('Device:C', 'C9', 205.74, 102.87, 0, [
    ('Reference', 'C9', 209.55, 101.6, 'left'), ('Value', '10u', 209.55, 104.14, 'left'),
    ('Footprint', 'Capacitor_SMD:C_1206_3216Metric'),
    ('Datasheet', 'https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3216X7R1H106K160AC'),
    ('Description', '50V X7R', 201.93, 102.87, 'right'),
    ('Manufacturer', 'TDK'), ('MPN', 'C3216X7R1H106K160AC'),
    ('Selection_Status', 'Local bulk at the output connector; keeps total load capacitance at the value used in the inrush calculation'),
], ['1', '2'])
new += label('PDB_VOUT', 205.74, 99.06, 0, 'C9.1')
new += gnd('#PWR018', 205.74, 106.68, 0)

# TP6/TP7 - the two status lines J2 no longer carries
for ref, y, net in [('TP6', 58.42, 'INA_ALERT_N'), ('TP7', 68.58, 'PDB_FAULT_N')]:
    new += symbol('Connector:TestPoint', ref, 233.68, y, 180, [
        # justify matches TP1-TP5: with the symbol at 180 degrees KiCad flips the
        # justification, so 'right' renders left-aligned and clears the pad circle.
        ('Reference', ref, 236.22, y + 3.81, 'right'),
        ('Value', 'TestPoint', 236.22, y + 6.35, 'right'),
        ('Footprint', 'TestPoint:TestPoint_Pad_D1.5mm'), ('Datasheet', ''),
        ('Description', 'test point'),
        ('Selection_Status', 'Bare copper test pad; no fitted part required'),
    ], ['1'])
    new += label(net, 233.68, y, 180, ref + '.1')

# D3 - J2 pin 1 is the Osiris +5V0_PROT contact and stays unconnected
new += no_connect(261.62, 72.39, 'J2.1nc')
new += gnd('#PWR019', 261.62, 80.01, 270)

# ------------------------------------------------------------- label rewrites
renames = [
    ((157.48, 34.29), 'GATE_DRV', 'GATE_PIN'),    # U1.10
    ((33.02, 87.63), 'GATE_DRV', 'GATE_FET'),     # Q1.4
    ((60.96, 87.63), 'GATE_DRV', 'GATE_FET'),     # Q2.4
    ((33.02, 95.25), 'GATE_DRV', 'GATE_FET'),     # R4.1, now the FET-side end
    ((29.21, 143.51), 'PDB_VOUT', 'VBAT_FUSED'),  # D4: U3 IN/EN + C4
    ((261.62, 77.47), 'INA_ALERT_N', 'PDB_I2C_SDA'),
]
deletions = [((261.62, 72.39), 'PDB_I2C_SDA'), ((261.62, 80.01), 'PDB_FAULT_N')]
LABPAT = re.compile(r'^\t\(label "([^"]+)"\n\t\t\(at ([\d.-]+) ([\d.-]+) ([\d.-]+)\).*?^\t\)\n',
                    re.M | re.S)


def relabel(m):
    name, x, y = m[1], float(m[2]), float(m[3])
    for (lx, ly), old in deletions:
        if (x, y) == (lx, ly):
            assert name == old, (name, old)
            return ''
    for (lx, ly), old, newname in renames:
        if (x, y) == (lx, ly):
            assert name == old, f'expected {old} at {(lx, ly)}, found {name}'
            return m[0].replace(f'(label "{old}"', f'(label "{newname}"', 1)
    return m[0]


s, n = LABPAT.subn(relabel, s)
assert n == 42, n
# R4.2 / C1.1 become the U1 GATE-pin side of the network
new += label('GATE_PIN', 33.02, 105.41, 0, 'C1.1')
assert 'GATE_DRV' not in s, 'GATE_DRV should be fully renamed'

# remove the old J2 pin-6 no-connect and the old J2 pin-1 ground symbol
s, n = re.subn(r'^\t\(no_connect\n\t\t\(at 261\.62 82\.55\)\n\t\t\(uuid "[^"]+"\)\n\t\)\n',
               '', s, flags=re.M)
assert n == 1, 'old J2 pin 6 no_connect not found'
s, n = SYMPAT.subn(lambda m: '' if '"#PWR013"' in m[0] else m[0], s)
assert '#PWR013' not in s, 'old J2 ground symbol not removed'
s = re.sub(r'\n\n+', '\n', s)

# ----------------------------------------------------------- symbol properties
fuse_note = ('4 A, 32 VDC MINI blade fuse; backup protection for a fault the MOSFETs '
             'cannot interrupt')
updates = {
    'F1': {
        'Value': '4A MINI', 'MPN': '0297004.WXNV', 'Description': fuse_note,
        'Datasheet': DS + 'Littelfuse_297_MINI.pdf',
        'Selection_Status': 'FINAL 4 A per requirements D1: 3.00 A continuous at the 75% convention against a 2.22 A design maximum; 17 A2s let-through; 3000 A interrupting (.WXNV)',
    },
    'J2': {
        'Value': 'OSIRIS_I2C', 'MPN': 'BM04B-GHS-TBT(LF)(SN)',
        'Footprint': 'Connector_JST:JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical',
        'Description': 'JST GH 4-way I2C; 1 NC, 2 SCL, 3 SDA, 4 GND; mates 1:1 with Osiris J28 (FMU_I2C1)',
        'Mating_Housing': 'GHR-04V-S',
        'Selection_Status': 'Re-pinned per requirements D3 to match Osiris J28 with a stock 4-way GH cable; pin 1 faces Osiris +5V0_PROT and is left unconnected',
    },
    'C4': {'Selection_Status': 'Now the U3 input capacitor on VBAT_FUSED per requirements D4; 10 uF matches the TPS7A16 recommendation of 10 uF from IN to GND'},
    'R4': {'Selection_Status': 'RGATE in the LTC4368 Figure 11 series position per requirements D2; paired with D2 across it'},
    'C1': {'Selection_Status': 'CGATE at the U1 GATE pin per requirements D2; sets the 6.25 kV/s turn-on ramp'},
    'U3': {'Selection_Status': 'Input and enable moved to VBAT_FUSED per requirements D4 so telemetry survives a breaker trip'},
}
J2PINS = re.compile(r'\t\t\(pin "(\d)"\n\t\t\t\(uuid "([^"]+)"\)\n\t\t\)\n')


def edit(m):
    b = m[0]
    ref = re.search(r'\(property "Reference" "([^"]+)"', b)[1]
    if ref == 'J2':
        assert '"Connector_Generic:Conn_01x06"' in b
        b = b.replace('(lib_id "Connector_Generic:Conn_01x06")',
                      '(lib_id "Connector_Generic:Conn_01x04")')
        keep = {n: u for n, u in J2PINS.findall(b) if n in '1234'}
        assert len(keep) == 4, keep
        b = J2PINS.sub('', b)
        block = ''.join(f'\t\t(pin "{n}"\n\t\t\t(uuid "{keep[n]}")\n\t\t)\n' for n in '1234')
        b = b.replace('\t\t(instances\n', block + '\t\t(instances\n', 1)
    for k, v in updates.get(ref, {}).items():
        b = prop(b, k, v)
    return b


s = SYMPAT.sub(edit, s)

# ------------------------------------------------------------------ site notes
notes = {
    'I²C pull-ups reside on Osiris;\\nINA_ALERT_N and PDB_FAULT_N each require\\na 10 kΩ pull-up to Osiris +3V3.':
        'J2 mates 1:1 with Osiris J28 (FMU_I2C1).\\n'
        'Osiris carries the 12 kΩ I²C pull-ups to its +3V3;\\n'
        'do not fit pull-ups here.\\n'
        'U2 address is 0x40; Osiris IC11 is 0x45 on the\\n'
        'internal FMU_I2C4 bus, so there is no clash.\\n'
        'Osiris Rev A exposes no spare GPIO or +3V3 on any\\n'
        'GH connector, so INA_ALERT_N and PDB_FAULT_N go\\n'
        'to TP6/TP7 only. Add pull-ups at whatever consumes\\n'
        'them in a later revision.',
    'F1: 5 A provisional; Keystone 3568 holder.\\nValidate load, inrush and fuse coordination.\\nJ3: XT60PW-F; 1=GND, 2=VOUT.\\nCable to Osiris J16 (VBATT_IN); verify polarity.\\nJ2 requires a custom cable; pin 6 is NC.':
        'Design maximum input current 2.22 A at the 10.56 V UV trip.\\n'
        'F1: 4 A MINI (0297004.WXNV) in a Keystone 3568 holder.\\n'
        'Backup only - the 10 A LTC4368 breaker trips in 8 µs.\\n'
        'Gate network per LTC4368 Figure 11: C1 at the GATE pin,\\n'
        'R4 in series to the FETs, D2 across R4 for fast turn-off.\\n'
        'D1 is bidirectional; a unidirectional TVS would short a\\n'
        'reversed pack and defeat the reverse-battery protection.\\n'
        'J3: XT60PW-F; 1=GND, 2=VOUT. Cable to Osiris J16\\n'
        '(VBATT_IN); verify polarity physically before use.',
}
for old, repl in notes.items():
    assert s.count(quote(old.replace('\\n', '\n'))) == 1, old[:40]
    s = s.replace(quote(old.replace('\\n', '\n')), quote(repl.replace('\\n', '\n')))

# ------------------------------------------------------------------- new items
s = s.rstrip()
assert s.endswith(')')
s = s[:-1] + new + ')\n'

# ------------------------------------------------------------------ invariants
for tag in ['wire', 'junction']:
    pat = re.compile(r'^\t\(' + tag + r'\b.*?^\t\)', re.M | re.S)
    assert pat.findall(before) == pat.findall(s), f'{tag} geometry must be untouched'
for ref in ['R1', 'R2', 'R3', 'R5', 'R6', 'R7', 'C2', 'C3', 'Q1', 'Q2', 'U1', 'U2', 'J1', 'J3']:
    find = lambda t: next(m[0] for m in SYMPAT.finditer(t)
                          if f'(property "Reference" "{ref}"' in m[0])
    assert find(before) == find(s), f'{ref} must be untouched'

sch.write_bytes(s.replace('\n', '\r\n').encode('utf-8'))
print('Applied D1 fuse rating, D2 gate network, D3 J2 re-pin, D4 U3 supply, D5 input clamp.')
print('Added D1, D2, C9, TP6, TP7. Wires and junctions unchanged; thresholds unchanged.')
