"""Reproducible planning calculations; no schematic or PCB mutations."""
from pathlib import Path
import math, json, itertools, hashlib, zipfile

ROOT = Path(__file__).resolve().parent
ZIP = Path(r'C:\Users\jared\Downloads\OsirisRevA (1).zip')
pads = json.loads((ROOT/'zip-pcb-pad-nets.json').read_text(encoding='utf-8'))
byref = {x['ref']: x for x in pads}
def net(ref, pin):
    return next(p['net'] for p in byref[ref]['pads'] if p['pin']==pin)
assert net('J16','1') == net('R55','1') == 'VBATT_IN'
assert net('R55','2') == net('J15','1') == net('U21','5') == 'VBATT_OUT'
assert net('U21','6') == net('U1','2') == net('U2','2') == 'VIN'
assert net('L1','2') == net('P1','251') == net('U4','5') == '+5V0'
assert net('L2','2') == net('U10','C1') == '+3V3'
assert net('U4','6') == net('J36','2') == '+5V0_PROT'

v5 = .8*(1+12000/2200)
v3 = .8*(1+47000/15000)
jetson_w = 7.0
efficiency = .85  # Planning assumption, not measured/guaranteed
rail5_a, rail3_a = 2.5, 2.0  # Conditional total-load ceilings, not measured loads
pdb_aux_w = .10  # Allowance
path_r = .075  # Ohms: planning aggregate incl. contacts/wire; not measured
rail_w = v5*rail5_a + v3*rail3_a
input_w = rail_w/efficiency + pdb_aux_w
def input_a(v, power):
    return 2*power/(v+math.sqrt(v*v-4*path_r*power))
uv = .5*(2e6+43200+56200)/(43200+56200)
ov = .5*(2e6+43200+56200)/56200
corners=[]
for a,b,c,ref in itertools.product([.99,1.01],[.99,1.01],[.99,1.01],[.4925,.5075]):
    rs=[2e6*a,43200*b,56200*c]
    corners.append((ref*sum(rs)/(rs[1]+rs[2]),ref*sum(rs)/rs[2]))
table=[]
for v in [16.8,14.8,12.0,uv]:
    i=input_a(v,input_w)
    table.append({'battery_v':v,'battery_a':i,'battery_w':v*i,
                  'path_drop_v':i*path_r,'path_loss_w':i*i*path_r})
# Conservative ripple sensitivity: -30% L and min frequency with further -6% FSS.
def ripple(vo, L, f): return vo*(1-vo/16.8)/(L*f)
inductors=[]
for vo,load in [(v5,rail5_a),(v3,rail3_a)]:
    di=ripple(vo,3.3e-6,570e3)
    dw=ripple(vo,3.3e-6*.7,510e3*.94)
    inductors.append({'vout':vo,'load_a':load,'nominal_ripple_app':di,
        'sensitivity_ripple_app':dw,'sensitivity_peak_a':load+dw/2,
        'sensitivity_rms_a':math.sqrt(load**2+dw**2/12)})
# Count only direct net-to-GND capacitors, not capacitors merely touching a rail.
def cap_value(s):
    import re
    m=re.fullmatch(r'(\d+)([pnum])(\d*)',s.strip())
    if not m:return 0.0
    return float(m[1]+('.'+m[3] if m[3] else ''))*{'p':1e-12,'n':1e-9,'u':1e-6,'m':1e-3}[m[2]]
caps={}
for rail in ['VIN','+5V0','+5V0_PROT','+3V3']:
    fs=[f for f in pads if f['ref'].startswith('C') and
        {rail,'GND'}.issubset({p['net'] for p in f['pads']})]
    caps[rail]={'uf':sum(cap_value(f['value']) for f in fs)*1e6,
                'refs':[f['ref'] for f in fs]}
manifest=[]
with zipfile.ZipFile(ZIP) as z:
    for f in (ROOT/'zip-source').iterdir():
        assert f.read_bytes()==z.read(f.name)
        manifest.append({'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
out={'assumptions':{'jetson_w':jetson_w,'efficiency':efficiency,'path_r':path_r,
      'rail5_ceiling_a':rail5_a,'rail3_ceiling_a':rail3_a,'pdb_aux_w':pdb_aux_w},
      'v5_nominal':v5,'v3_nominal':v3,'jetson_rail_a':jetson_w/v5,
      'rail_w':rail_w,'converted_input_w':input_w,'battery_table':table,
      'pdb_uv':uv,'pdb_ov':ov,'pdb_uv_1pct_corners':[min(x[0] for x in corners),max(x[0] for x in corners)],
      'pdb_ov_1pct_corners':[min(x[1] for x in corners),max(x[1] for x in corners)],
      'osiris_uv_on':1.2*554/84,'osiris_uv_off':1.09*554/84,
      'osiris_ov_off':1.2*554/24,'osiris_ov_recover':1.09*554/24,
      'inductors':inductors,'direct_caps':caps,
      'gate_ramp_v_per_s_typ':35e-6/5.6e-9,
      'gate_ramp_v_per_s_max_assumed':60e-6/(5.6e-9*.95),
      'pdb_capacitive_inrush_typ_a':(caps['VIN']['uf']+11)*1e-6*35e-6/5.6e-9,
      'source_manifest':manifest}
(ROOT/'calculations.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ['source_manifest','direct_caps']},indent=2))
print('Verified ZIP source bytes and six key power-path assertions.')
