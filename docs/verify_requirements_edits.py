"""Verify the requirements edits against the exported netlist, then regenerate the
purchasing BOM and the datasheet index. Fails loudly rather than reporting success."""
from pathlib import Path
import csv, json, hashlib, re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
KFP = Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')

net = ET.parse(root / 'docs/requirements.net.xml').getroot()
nets = {}
for n in net.find('nets'):
    nets[n.get('name')] = {(x.get('ref'), x.get('pin')) for x in n.findall('node')}
owner = {}
for name, nodes in nets.items():
    for node in nodes:
        owner[node] = name

def on(ref, pin):
    return owner.get((ref, pin))

# --- D2: LTC4368 Figure 11 gate network -----------------------------------
assert nets['/GATE_PIN'] == {('U1', '10'), ('C1', '1'), ('R4', '2'), ('D2', '1')}, nets['/GATE_PIN']
assert nets['/GATE_FET'] == {('Q1', '4'), ('Q2', '4'), ('R4', '1'), ('D2', '2')}, nets['/GATE_FET']
assert on('C1', '2') == 'GND'
# D2 pin 1 is the cathode: it must sit on the GATE-pin side so the fast pull-down
# bypasses R4. Pin 2 is the anode, on the MOSFET-gate side.
assert on('D2', '1') == '/GATE_PIN' and on('D2', '2') == '/GATE_FET'

# --- D4: U3 supply moved ahead of the MOSFETs ------------------------------
assert on('U3', '8') == '/PDB_VOUT' and on('U3', '5') == '/PDB_VOUT'
assert on('C4', '2') == '/PDB_VOUT' and on('C4', '1') == 'GND'   # TPS7A16 CIN
assert ('U3', '8') not in nets['/VBAT_FUSED']

assert on('D3', '1') == '/PDB_VOUT' and on('D3', '2') == 'GND'

# --- D5: bidirectional clamp across the fused input ------------------------
assert on('D1', '1') == '/VBAT_FUSED' and on('D1', '2') == 'GND'

# --- output node keeps local bulk -----------------------------------------
assert on('C9', '1') == '/PDB_VOUT' and on('C9', '2') == 'GND'
assert nets['/PDB_VOUT'] == {('J3', '2'), ('R5', '4'), ('TP4', '1'), ('U2', '8'), ('C9', '1'), ('U3', '8'), ('U3', '5'), ('C4', '2'), ('D3', '1')}

# --- D3: J2 mates 1:1 with Osiris J28 (1 +5V0_PROT, 2 SCL, 3 SDA, 4 GND) ---
assert on('J2', '1') == 'unconnected-(J2-Pin_1-Pad1)', on('J2', '1')
assert on('J2', '2') == '/PDB_I2C_SCL' and on('J2', '3') == '/PDB_I2C_SDA'
assert on('J2', '4') == 'GND'
assert ('J2', '5') not in owner and ('J2', '6') not in owner, 'J2 must have only 4 pins'
assert nets['/PDB_I2C_SCL'] == {('J2', '2'), ('U2', '5')}
assert nets['/PDB_I2C_SDA'] == {('J2', '3'), ('U2', '4')}
# INA228 address pins both grounded -> 0x40, distinct from Osiris IC11 at 0x45
assert on('U2', '1') == 'GND' and on('U2', '2') == 'GND'

# --- the two orphaned status lines land on test points --------------------
assert nets['/INA_ALERT_N'] == {('U4', '4'), ('TP6', '1')}
assert nets['/PDB_FAULT_N'] == {('U1', '7'), ('TP7', '1')}

# --- unchanged: thresholds, Kelvin sensing, power path, J1/J3 polarity -----
assert nets['Net-(U1-UV)'] == {('R1', '2'), ('R2', '1'), ('U1', '2')}
assert nets['Net-(U1-OV)'] == {('R2', '2'), ('R3', '1'), ('U1', '3')}
assert nets['/SHDN_LTC'] == {('R6', '1'), ('R7', '2'), ('U1', '6')}
assert on('R1', '1') == '/VBAT_FUSED' and on('R3', '2') == 'GND'
# SENSE on the upstream sense pad, VOUT on the downstream one: forward-positive
assert on('R5', '1') == '/PDB_PROTECTED' and on('R5', '4') == '/PDB_VOUT'
assert on('R5', '2') == '/SHUNT_HI' and on('U1', '9') == '/SHUNT_HI'
assert on('R5', '3') == '/SHUNT_LO' and on('U1', '8') == '/SHUNT_LO'
assert on('C2', '1') == '/SHUNT_LO' and on('C2', '2') == 'GND'   # LTC4368 needs >=1uF
assert on('J1', '1') == 'GND' and on('J1', '2') == '/VBAT_RAW'
assert on('J3', '1') == 'GND' and on('J3', '2') == '/PDB_VOUT'
assert on('F1', '1') == '/VBAT_RAW' and on('F1', '2') == '/VBAT_FUSED'

# --- every part has a resolving footprint and a resolving datasheet -------
rows = list(csv.DictReader((root / 'BOM.csv').open(newline='', encoding='utf-8-sig')))
assert len(rows) == 39, len(rows)
for row in rows:
    fp = row['Footprint']
    assert fp, row['Reference']
    lib, name = fp.split(':', 1)
    base = root / 'Libraries' / f'{lib}.pretty' if lib.startswith('PDB_') else KFP / f'{lib}.pretty'
    assert (base / f'{name}.kicad_mod').exists(), fp
    for field in ('Datasheet', 'Holder Datasheet'):
        val = row[field]
        if val.startswith('${KIPRJMOD}/'):
            assert (root / val.removeprefix('${KIPRJMOD}/')).exists(), (row['Reference'], val)

# --- purchasing BOM: schematic parts plus the separately bought fuse holder
fields = list(rows[0])
fields.insert(1, 'Quantity')
fields.append('BOM Role')
for row in rows:
    row.update(Quantity='1', **{'BOM Role': 'Schematic component'})
f1 = next(x for x in rows if x['Reference'] == 'F1')
holder = {k: '' for k in fields}
holder.update(
    Reference='F1-holder', Quantity='1', Value='MINI fuse holder',
    Specification='Keystone 3568; separate purchased holder for F1',
    Footprint=f1['Footprint'], Manufacturer='Keystone Electronics', MPN='3568',
    Datasheet='${KIPRJMOD}/Datasheets/Keystone_3568.pdf',
    **{'Selection Status': 'Holder assigned; retention, access and vibration review pending',
       'BOM Role': 'F1 holder; same physical assembly, not an additional PCB footprint'})
rows.append(holder)
with (root / 'BOM_purchasing.csv').open('w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fields)
    w.writeheader()
    w.writerows(rows)

# --- datasheet index ------------------------------------------------------
DSDIR = root / 'Datasheets'
sources = {x['file']: x for x in json.loads((DSDIR / 'sources.json').read_text(encoding='utf-8'))}
resolved = {
    'Littelfuse_297_MINI.pdf': ('https://www.ficcorp.com/content/297-datasheet.pdf', 'mirror'),
    'Ohmite_FC4L.pdf': ('https://www.tti.com/content/dam/ttiinc/manufacturers/ohmite/doc/ohmite-fc4l-series-current-sense-resistors-datasheet-and-specifications.pdf', 'mirror'),
    'Bourns_SMAJ_TVS.pdf': ('https://www.bourns.com/docs/product-datasheets/smaj.pdf', 'manufacturer'),
    'onsemi_MBR0540.pdf': ('https://cdn-reichelt.de/documents/datenblatt/A400/MBR0540T1-D.PDF', 'mirror'),
}
for name, (url, kind) in resolved.items():
    path = DSDIR / name
    assert path.exists(), name
    data = path.read_bytes()
    assert data.startswith(b'%PDF-'), name
    sources[name] = {'file': name, 'source': url, 'bytes': len(data),
                     'sha256': hashlib.sha256(data).hexdigest(),
                     'status': 'downloaded', 'origin': kind}
# retire the entries the resolved downloads replaced
for dead in ['Littelfuse_MINI_0297.pdf', 'Littelfuse_MINI_0297_selection_guide.pdf']:
    if dead in sources:
        sources[dead]['status'] = 'superseded'
        sources[dead]['reason'] = 'Ratings, I2t and derating data now archived in Littelfuse_297_MINI.pdf'
ordered = sorted(sources.values(), key=lambda x: x['file'])
(DSDIR / 'sources.json').write_text(json.dumps(ordered, indent=2) + '\n', encoding='utf-8')

lines = ['# Component datasheets', '',
         'Downloaded PDFs are stored beside this index. `origin` in `sources.json` records',
         'whether a PDF came from the manufacturer or a distributor mirror; mirrors were used',
         'where the manufacturer host returned HTTP 403. Entries still marked as unavailable',
         'keep a manufacturer link in the schematic instead.', '',
         '| Document | Local file / status | Source |', '|---|---|---|']
for x in ordered:
    if x['status'] == 'downloaded':
        state = f"[{x['file']}]({x['file']})" + (' (mirror)' if x.get('origin') == 'mirror' else '')
    elif x['status'] == 'superseded':
        state = 'Superseded by Littelfuse_297_MINI.pdf'
    else:
        state = 'Online link; PDF download unavailable'
    lines.append(f"| {x['file']} | {state} | [Source]({x['source']}) |")
lines += ['',
          'Existing project PDFs: [LTC4368](LTC4368%20%28Rev%20C%29.pdf) and '
          '[ISC015N06NM5LF2](Datasheet%20ISC015N06NM5LF2.pdf).', '',
          'TDK links refer to characteristic sheets; the schematic retains manufacturer',
          'product pages for each selected capacitor.', '']
(DSDIR / 'README.md').write_text('\n'.join(lines), encoding='utf-8')

live = sum(x['status'] == 'downloaded' for x in ordered)
print(f'Netlist verified: Figure 11 gate network, U3 on protected PDB_VOUT, bidirectional clamp,')
print(f'J2 4-way matching Osiris J28, TP6/TP7 status lines, thresholds and Kelvin taps unchanged.')
print(f'39 BOM rows, all footprints resolve, all local datasheet paths resolve.')
print(f'Datasheet index rewritten: {live} local PDFs.')
