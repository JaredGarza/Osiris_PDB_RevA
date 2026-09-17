"""Reproducible instrumented passive-protection screen; no CAD changes.

Run with optional test names: transients corners faults reverse25 temperature nominal.
Reports are independent of the existing final and HV experiments.
"""
from pathlib import Path
import sys, json, hashlib, time, re
H=Path(__file__).resolve().parent
S=H.parent/'combined-20260915'
sys.path.insert(0,str(S))
import verify_all as v

BASE_LIMITS=v.limits
PIN_LIMITS={**v.PIN_STRESS,'q1_vds':(0,60),'q2_vds':(0,60),
 'inp_min':(-.3,85),'inn_min':(-.3,85),'vbus_min':(-.3,85),
 'inp_max':(-.3,85),'inn_max':(-.3,85),'vbus_max':(-.3,85),
 'ina_diff_abs':(0,40),'v3v3_max':(0,3.6),'vout_final':(15,16.8),
 'd4_reverse':(0,100),'d3_reverse':(0,100)}

def limits(name):
 if not name.startswith('screen17_'):return BASE_LIMITS(name)
 kind=name.removeprefix('screen17_')
 if kind=='transients':return PIN_LIMITS
 result=dict(BASE_LIMITS('final_'+('corners' if kind=='nominal' else kind)))
 if kind=='nominal':result.update({'iin_ss':(0,2.5),'pout_nominal':(0,25)})
 result.update({k:PIN_LIMITS[k] for k in ('inp_min','inn_min','vbus_min','inp_max','inn_max','vbus_max','ina_diff_abs','d4_reverse','d3_reverse')})
 return result

def save_measured(s):
 nodes=set();currents=set()
 for line in s.splitlines():
  if not line.lower().startswith('.meas'):continue
  for match in re.finditer(r'\bV\(([^)]+)\)',line,re.I):nodes.update(x.strip() for x in match[1].split(','))
  currents.update(re.findall(r'\bI\(([^)]+)\)',line,re.I))
 s=re.sub(r'^\.save[^\n]*\n','',s,flags=re.M|re.I)
 return s.replace('.end','.save '+' '.join('V('+x+')' for x in sorted(nodes))+' '+' '.join('I('+x+')' for x in sorted(currents))+'\n.end')

def prepare(kind):
 if kind=='transients':
  s=(S/'hvd_transients.cir').read_text().replace('pdb_hvd.lib','pdb_screen17.lib')
  s=re.sub(r'^\.meas TRAN TVS_.*\n','',s,flags=re.M)
  s=s.replace('* 100 V FET protection candidate, variant D. Screening only.','* Passive blocking candidate with original 60 V FETs. Screening only.')
 else:
  s=(S/('final_'+('corners' if kind=='nominal' else kind)+'.cir')).read_text().replace('pdb_final.lib','pdb_screen17.lib')
  if kind=='nominal':
   s=s.replace('osiris_reva.lib','osiris_screen17_nominal.lib')
   s=s.replace('.end','.meas TRAN POUT_NOMINAL AVG V(PDBOUT)*I(LCBL) FROM 400m TO 500m\n.end')
  for name,node in [('INP','INA_IN_P'),('INN','INA_IN_N'),('VBUS','INA_VBUS')]:
   s=s.replace('.end',f'.meas TRAN {name}_MIN MIN V(XPDB:{node})\n.end')
 for name,node in [('INP','INA_IN_P'),('INN','INA_IN_N'),('VBUS','INA_VBUS')]:
  s=s.replace('.end',f'.meas TRAN {name}_MAX MAX V(XPDB:{node})\n.end')
 s=s.replace('.end','''.meas TRAN INA_DIFF_ABS MAX ABS(V(XPDB:INA_IN_P,XPDB:INA_IN_N))
.meas TRAN D4_REVERSE MAX V(XPDB:VBAT_FUSED,XPDB:DIODE_IN)
.meas TRAN D3_REVERSE MAX V(XPDB:D3_REVERSE)
.meas TRAN D4_IPEAK MAX ABS(V(XPDB:D4_CURRENT))
.meas TRAN D3_IPEAK MAX ABS(V(XPDB:D3_CURRENT))
.meas TRAN D4_ENERGY INTEG V(XPDB:D4_POWER)
.meas TRAN D3_ENERGY INTEG V(XPDB:D3_POWER)
.meas TRAN DAMP_ENERGY INTEG V(XPDB:DAMP_POWER)
.end''')
 if kind in ('corners','temperature','nominal'):
  s=s.replace('.end','.meas TRAN D4_POWER_SS AVG V(XPDB:D4_POWER) FROM 400m TO 500m\n.meas TRAN D4_POWER_STEP AVG V(XPDB:D4_POWER) FROM 700m TO 890m\n.end')
 s=s.replace('models\\pdb_devices.lib','models\\pdb_screen17_devices.lib')
 p=S/('screen17_'+kind+'.cir');p.write_text(save_measured(s));return p

def hashes(deck):
 pending=[deck];seen=set()
 while pending:
  p=pending.pop().resolve()
  if p in seen:continue
  seen.add(p)
  for inc in re.findall(r'^\s*\.(?:inc|include|lib)\s+([^\r\n]+)',p.read_text(errors='replace'),re.M|re.I):
   q=Path(inc.strip().strip('"'))
   if not q.is_absolute():q=p.parent/q
   if q.is_file():pending.append(q)
 return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(seen)}

def main():
 previous=H/'screen17-results.json'
 if previous.exists():
  (H/('screen17-results-'+time.strftime('%Y%m%d-%H%M%S')+'.json')).write_bytes(previous.read_bytes())
 devices=(S/'models/pdb_devices.lib').read_text()
 old='RINP INP GND  10Meg\nRINN INN GND  10Meg'
 assert old in devices,'Unexpected INA228 model; review before editing.'
 devices=devices.replace(old,'''* INA228 datasheet active-mode screening: bias max2.5nA, Rdiff typical92k.
* Previous10Meg shunts implied8.5uA at85V, inconsistent with the datasheet.
* Bias is power-gated for simulation; unpowered leakage is NOT validated.
BIP INP GND I=2.5n*limit(V(VS,GND)/2.7,0,1)
BIN INN GND I=2.5n*limit(V(VS,GND)/2.7,0,1)
BDIFF INP INN I=V(INP,INN)*limit(V(VS,GND)/2.7,0,1)/92k
RINP INP GND 1T
RINN INN GND 1T''')
 (S/'models/pdb_screen17_devices.lib').write_text(devices)
 osiris=(S/'osiris/osiris_reva.lib').read_text()
 assert 'ISTEP={IJET*0.5}' in osiris
 osiris=osiris.replace('ISTEP={IJET*0.5}','ISTEP=0')
 osiris='* Nominal 7 W Jetson load stimulus; identical Osiris hardware. No overload step.\n'+osiris
 (S/'osiris/osiris_screen17_nominal.lib').write_text(osiris)
 lib=(S/'pdb/pdb_passive.lib').read_text()
 lib=lib.replace('.ends PDB_CURRENT','''* Isolated behavioral voltage probes; no power-path loading.
BMON3 D3_CURRENT GND V=I(D3)
BMON4 D4_CURRENT GND V=I(D4)
BPOW3 D3_POWER GND V=V(GND,VOUT)*I(D3)
BPOW4 D4_POWER GND V=V(DIODE_IN,VBAT_FUSED)*I(D4)
BREV3 D3_REVERSE GND V=V(VOUT,GND)
BPOWR DAMP_POWER GND V=V(DIODE_IN,INPUT_DAMP)*V(DIODE_IN,INPUT_DAMP)
.ends PDB_CURRENT''')
 (S/'pdb/pdb_screen17.lib').write_text(lib)
 v.limits=limits
 report={'scope':'Simulation-only passive protection candidate; not represented in CAD or qualified for fabrication.',
 'limitations':['Diodes and MOSFETs are fitted models; current, pulse energy and dissipation are reported, not automatically qualified.',
 'TVS sharing and board parasitics are not established. Effective filter capacitance assumes minimum 1 uF.',
 'Osiris hardware unchanged. Current-step stimulus exceeds nominal 7 W Jetson load.'],
 'timestamp':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'results':[],'sha256':{}}
 for kind in sys.argv[1:] or ['nominal','transients','corners','faults','reverse25','temperature']:
  deck=prepare(kind)
  report['sha256'].update(hashes(deck))
  result=v.run(deck,Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
  report['results'].append(result)
  (H/'screen17-results.json').write_text(json.dumps(report,indent=2))
  print(kind,result['status'],result['seconds'],result['errors'],flush=True)
 return int(any(r['status']=='FAIL' for r in report['results']))

if __name__=='__main__':sys.exit(main())
