"""Read freshly exported KiCad XML; no changes to source design or BOM."""
from pathlib import Path
import xml.etree.ElementTree as ET
import json, csv, os

here = Path(__file__).resolve().parent
root = here.parents[1]
system_footprints = Path(os.environ.get('KICAD_FOOTPRINT_DIR',
    'C:/Program Files/KiCad/10.0/share/kicad/footprints' if os.name == 'nt'
    else '/usr/share/kicad/footprints'))
def read(name):
    tree = ET.parse(here / name).getroot()
    comps = {c.get('ref'): {'value': c.findtext('value'), 'footprint': c.findtext('footprint'), 'fields': {f.get('name'): f.text for f in c.findall('fields/field')}} for c in tree.findall('components/comp')}
    nets = {n.get('name'): sorted((x.get('ref'), x.get('pin')) for x in n.findall('node')) for n in tree.findall('nets/net')}
    return comps, nets
c, n = read('current.net.xml')
owner = {tuple(pin): name for name, pins in n.items() for pin in pins}
checks = []
def pins(net, expected):
    assert set(map(tuple,n[net])) == set(expected), (net,n[net])
    checks.append(net)
pins('/GATE_PIN', [('U1','10'),('C1','1'),('R4','2'),('D2','1')])
pins('/GATE_FET', [('Q1','4'),('Q2','4'),('R4','1'),('D2','2')])
for pin in [('U3','8'),('U3','5'),('C4','2'),('D3','1'),('J3','2')]:
    assert owner[pin] == '/PDB_VOUT', (pin,owner[pin])
for pin in [('D3','2'),('J1','1'),('J3','1'),('J2','4'),('U2','1'),('U2','2')]:
    assert owner[pin] == 'GND', pin
pins('/PDB_I2C_SCL', [('J2','2'),('U2','5')])
pins('/PDB_I2C_SDA', [('J2','3'),('U2','4')])
assert owner[('J2','1')].startswith('unconnected-')
assert owner[('R5','1')] == '/PDB_PROTECTED'
assert owner[('R5','4')] == '/PDB_VOUT'
assert owner[('R5','2')] == owner[('U1','9')] == '/SHUNT_HI'
assert owner[('R5','3')] == owner[('U1','8')] == '/SHUNT_LO'
assert owner[('F1','1')] == owner[('J1','2')] == '/VBAT_RAW'
assert owner[('D1','1')] == owner[('F1','2')] == '/VBAT_FUSED'
assert owner[('D1','2')] == 'GND'
assert 'PROVISIONAL' in c['F1']['fields']['Selection_Status']
rows = {r['Reference']: r for r in csv.DictReader((root/'BOM.csv').open(encoding='utf-8-sig'))}
assert set(rows) == set(c), (set(rows)^set(c))
for ref, comp in c.items():
    assert rows[ref]['Value'] == comp['value'], ref
    assert rows[ref]['Footprint'] == comp['footprint'], ref
    assert rows[ref]['MPN'] == comp['fields'].get('MPN',''), ref
    lib, fp = comp['footprint'].split(':')
    base = root/'Libraries'/f'{lib}.pretty' if lib.startswith('PDB_') else system_footprints/f'{lib}.pretty'
    assert (base/f'{fp}.kicad_mod').exists(), ref
diffs = {}
for name in ['archive','v1']:
    old, nets = read(name+'.net.xml')
    diffs[name] = {'parts':len(old), 'added':sorted(set(c)-set(old)), 'removed':sorted(set(old)-set(c)), 'changed':{r:{'old':old[r], 'current':c[r]} for r in c.keys() & old.keys() if old[r]!=c[r]}, 'changed_nets':{k:{'old':nets.get(k), 'current':n.get(k)} for k in nets.keys()|n.keys() if nets.get(k)!=n.get(k)}}
result = {'parts':len(c),'nets':len(n),'connectivity_checks':'PASS','BOM_and_footprint_files':'PASS','versions':diffs}
(here/'design-checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(f'PASS: {len(c)} parts, {len(n)} nets; critical power/gate/Kelvin/I2C connectivity; BOM values, MPNs and footprint file availability.')
for name,d in diffs.items():
    print(name, 'parts',d['parts'],'added',d['added'],'removed',d['removed'],'changed parts',list(d['changed']),'changed nets',len(d['changed_nets']))
