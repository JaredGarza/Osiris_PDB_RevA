"""Reproduce the September 15 desk review. Does not approve hardware or edit CAD.

Run kicad-cli sch export netlist --format kicadxml to final.net.xml here first.
current.net.xml is the original and after.net.xml the metadata-only snapshot.
Threshold bounds include 1% initial resistor tolerance and specified comparator
threshold/leakage corners, but not resistor TCR, aging, noise or PCB parasitics.
"""
from pathlib import Path
import csv
import hashlib
import itertools
import json
import math
import os
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
tree = ET.parse(HERE / 'final.net.xml').getroot()
parts = {c.get('ref'): c for c in tree.findall('components/comp')}
nets = {n.get('name'): sorted((p.get('ref'), p.get('pin')) for p in n.findall('node'))
        for n in tree.findall('nets/net')}
owner = {p: name for name, pins in nets.items() for p in pins}
before = ET.parse(HERE / 'current.net.xml').getroot()
before_nets = {n.get('name'): sorted((p.get('ref'), p.get('pin')) for p in n.findall('node'))
               for n in before.findall('nets/net')}
before_owner = {p:name for name,pins in before_nets.items() for p in pins}
for pin,name in before_owner.items():
    if pin not in [('U3','2'),('U3','3'),('U3','7')]:
        assert owner[pin] == name, ('Unexpected electrical change', pin, name, owner[pin])
assert set(nets['/PDB_LDO_ADJ']) == {('U3','2'),('R11','2'),('R12','1'),('C10','2')}
for pin in [('R11','1'),('C10','1')]: assert owner[pin]=='/PDB_3V3'
assert owner[('R12','2')]=='GND'
oldparts={c.get('ref'):c for c in before.findall('components/comp')}
assert set(parts)-set(oldparts)=={'R11','R12','C10'}
assert not (set(oldparts)-set(parts))
for ref,c in oldparts.items():
    if ref!='U3':
        for field in ['value','footprint']:
            assert c.findtext(field)==parts[ref].findtext(field),(ref,field)

def net(ref, pin, expected):
    assert owner[(ref, str(pin))] == expected, (ref, pin, owner[(ref, str(pin))])

for ref, pin, expected in [
    ('J1', 1, 'GND'), ('J1', 2, '/VBAT_RAW'),
    ('J3', 1, 'GND'), ('J3', 2, '/PDB_VOUT'),
    ('J2', 2, '/PDB_I2C_SCL'), ('J2', 3, '/PDB_I2C_SDA'), ('J2', 4, 'GND'),
    ('U2', 1, 'GND'), ('U2', 2, 'GND'),
    ('U2', 8, '/PDB_VOUT'), ('U3', 8, '/PDB_VOUT'), ('U3', 5, '/PDB_VOUT'),
    ('R5', 1, '/PDB_PROTECTED'), ('R5', 4, '/PDB_VOUT'),
    ('R5', 2, '/SHUNT_HI'), ('R5', 3, '/SHUNT_LO'),
    ('U1', 9, '/SHUNT_HI'), ('U1', 8, '/SHUNT_LO'),
    ('D2', 1, '/GATE_PIN'), ('D2', 2, '/GATE_FET'),
    ('D3', 1, '/PDB_VOUT'), ('D3', 2, 'GND')]:
    net(ref, pin, expected)
assert owner[('J2', '1')].startswith('unconnected-')

# Confirm input values are still the values used by this review.
for ref, value in {'R1':'2M0', 'R2':'43k2', 'R3':'56k2', 'R5':'5m',
                   'C1':'5n6', 'C3':'100n', 'U3':'LT3010EMS8E',
                   'R11':'1k58','R12':'1k0','C10':'100n'}.items():
    assert parts[ref].findtext('value') == value, ref
rows = {r['Reference']: r for r in csv.DictReader((ROOT/'BOM.csv').open(encoding='utf-8-sig'))}
assert set(rows) == set(parts)
purchasing = {r['Reference']:r for r in csv.DictReader((ROOT/'BOM_purchasing.csv').open(encoding='utf-8-sig'))}
assert set(purchasing)==set(rows)|{'F1-holder'}
assert purchasing['F1-holder']['MPN']=='3568'
for ref,row in rows.items():
    for field in row:
        assert row[field]==purchasing[ref][field],(ref,field,'purchasing drift')
mpn_exceptions = []
for ref, c in parts.items():
    assert rows[ref]['Value'] == c.findtext('value'), ref
    assert rows[ref]['Footprint'] == c.findtext('footprint'), ref
    fields = {f.get('name'): f.text or '' for f in c.findall('fields/field')}
    if rows[ref]['MPN'] != fields.get('MPN', ''):
        raise AssertionError((ref, fields.get('MPN'), rows[ref]['MPN']))
    lib, fp = c.findtext('footprint').split(':')
    directory = (ROOT/'Libraries'/f'{lib}.pretty' if lib.startswith('PDB_')
                 else Path(os.environ.get('KICAD_FOOTPRINT_DIR','C:/Program Files/KiCad/10.0/share/kicad/footprints'))/f'{lib}.pretty')
    assert (directory/f'{fp}.kicad_mod').is_file(), (ref, fp)

def thresholds(which, recovery=False):
    vals=[]
    for factors in itertools.product((.99,1.01), repeat=3):
        r1,r2,r3 = [a*b for a,b in zip((2e6,43.2e3,56.2e3),factors)]
        for threshold, iuv, iov in itertools.product((.4925,.5075),(-10e-9,10e-9),(-10e-9,10e-9)):
            for hyst in ((.020,.032) if recovery else (0,)):
                v = threshold + hyst if which=='uv' else threshold-hyst
                if which=='uv':
                    vu=v
                    vo=(vu/r2-iov)/(1/r2+1/r3)
                else:
                    vo=v
                    vu=vo+r2*(vo/r3+iov)
                vals.append(vu+r1*((vu-vo)/r2+iuv))
    return [min(vals),max(vals)]

rs_min,rs_max=.005*.99,.005*1.01
slew_min,slew_max=20e-6/(5.6e-9*1.05),60e-6/(5.6e-9*.95)
path_budget=.075
load_cases=[]
for v in (16.8,14.8,12,thresholds('uv')[0]):
    # 25 W at J3 plus separate 0.1 W housekeeping allowance.
    p=25.1
    i=(v-math.sqrt(v*v-4*path_budget*p))/(2*path_budget)
    load_cases.append({'battery_V':v,'input_A':i,'J3_V_approx':v-i*path_budget,'path_loss_W':i*i*path_budget})

result={
    'status':'DESK REVIEW ONLY; M1 proposed; M2 open; not a fabrication release',
    'parts':len(parts),'nets':len(nets),'connectivity':'PASS',
    'ECO_scope':'Only U3 replacement plus R11/R12/C10; all other original pin-to-net connections preserved',
    'BOM_values_footprint_files':'PASS','MPN_documented_exceptions':mpn_exceptions,
    'UV_falling_V':thresholds('uv'),'UV_recovery_V':thresholds('uv',True),
    'OV_rising_V':thresholds('ov'),'OV_recovery_V':thresholds('ov',True),
    'forward_trip_A_normal_conditions':[.040/rs_max,.060/rs_min],
    'forward_trip_A_Vout_zero_test_condition':[.030/rs_max,.070/rs_min],
    'reverse_trip_magnitude_A':[.042/rs_max,.058/rs_min],
    'gate_ramp_estimate_V_per_s':[slew_min,slew_max],
    'ramp_estimate_to_16p8_ms':[16.8/slew_max*1000,16.8/slew_min*1000],
    '220uF_capacitive_inrush_estimate_A':[220e-6*slew_min,220e-6*slew_max],
    'inrush_plus_2p5A_load_estimate_A':220e-6*slew_max+2.5,
    'capacitor_energy_220uF_16p8V_J':.5*220e-6*16.8**2,
    'load_cases_25W_plus_housekeeping':load_cases,
    'shunt_W_at_2p5A':2.5**2*rs_max,
    'shunt_W_at_14p142A':(.070/rs_min)**2*rs_max,
    'I2C_rise_us_2p2k_1pct_200pF':.8473*2200*1.01*200e-12*1e6,
    'I2C_sink_mA_3p6V_0p4V_2p2k_1pct':(3.6-.4)/(2200*.99)*1000,
    'INA228_proposed_CURRENT_LSB_A':.00005,
    'INA228_SHUNT_CAL_ADCRANGE0':round(13107.2e6*.00005*.005),
    'INA228_SHUNT_CAL_exact':13107.2e6*.00005*.005,
    'short_current_16p8V_min_loop_R_for_1000A_ohm':16.8/1000,
    'LT3010_nominal_output_V':1.275*(1+1580/1000)+50e-9*1580,
    'LT3010_initial_reference_and_1pct_divider_output_V':[1.237*(1+1580*.99/(1000*1.01)),1.313*(1+1580*1.01/(1000*.99))+100e-9*1580*1.01],
    'LT3010_C10_Xc_10kHz_90nF_ohm':1/(2*math.pi*10000*90e-9),
    'LT3010_feedback_load_min_A':1.237/(1000*1.01),
    'LT3010_5mA_dissipation_16p8V_plus_0p7mA_ground_W':(16.8-3.1)*.005+16.8*.0007,
    'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                     for name in ('Osiris_PDB_RevA.kicad_sch','Osiris_PDB_RevA.kicad_pro','BOM.csv','BOM_purchasing.csv','Libraries/PDB_Symbols.kicad_sym')}
}
(HERE/'calculations.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
