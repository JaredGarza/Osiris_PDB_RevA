"""Compare the live A-P4 KiCad source/BOMs with the release SPICE population."""
from pathlib import Path
import csv, json, re, shutil, subprocess, xml.etree.ElementTree as E

audit=Path(__file__).resolve().parent
root=audit.parents[2]
schematic=root/'Osiris_PDB_RevA.kicad_sch'
live=audit/'live.net.xml'
kicad=shutil.which('kicad-cli') or r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
subprocess.run([kicad,'sch','export','netlist','--format','kicadxml','-o',str(live),str(schematic)],check=True)
new=E.parse(live).getroot()
components={c.get('ref'):c for c in new.findall('components/comp')}
assert len(components)==59, f'expected 59 live symbols, found {len(components)}'

for name in ('BOM.csv','BOM_purchasing.csv'):
 rows={r['Reference']:r for r in csv.DictReader((root/name).open(encoding='utf-8-sig'))}
 for ref,c in components.items():
  props={f.get('name'):f.text or '' for f in c.findall('fields/field')}
  for field,expected in [('Value',c.findtext('value')),('Footprint',c.findtext('footprint')),('MPN',props.get('MPN',''))]:
   assert rows[ref][field]==expected,(name,ref,field,rows[ref][field],expected)

netmap={'GND':'GND','/LTC_UV':'N_UV','/LTC_OV':'N_OV','Net-(U1-RETRY)':'N_RETRY',
 '/GATE_PIN':'GP','/GATE_FET':'GF','/GATE_RC':'GATE_RC','/SW_COMMON':'COMMON',
 '/PDB_VOUT':'VOUT','/PDB_3V3':'V3V3','/PDB_FAULT_N':'FAULT','/INA_ALERT_N':'ALERT',
 '/PDB_I2C_SCL':'SCL','/PDB_I2C_SDA':'SDA','/INA_IN_P':'INA_IN_P','/INA_IN_N':'INA_IN_N',
 '/INA_VBUS':'INA_VBUS','/IDEAL_IN':'IDEAL_IN','/IDEAL_GATE':'IDEAL_GATE',
 '/IDEAL_VSS':'IDEAL_VSS','/INPUT_DAMP':'INPUT_DAMP','/VBAT_FUSED':'VBAT_FUSED'}
pins={}
for n in new.findall('nets/net'):
 node=netmap.get(n.get('name'),n.get('name').lstrip('/'))
 for x in n.findall('node'): pins[(x.get('ref'),x.get('pin'))]=node.upper()

model=(audit.parent/'pdb/pdb_release.lib').read_text()
lines={l.split()[0]:l.split() for l in model.splitlines() if l and not l.startswith(('*','+','.'))}
params=dict(re.findall(r'(\w+)=([\w.]+)',model))

def val(s):
 s=s.strip('{}')
 if re.fullmatch(r'\d+M\d+',s):
  a,b=s.split('M'); return float(a+'.'+b)*1e6
 if re.fullmatch(r'[\d.]+M',s): return float(s[:-1])*1e6
 s=s.lower().replace('meg','e6')
 s=re.sub(r'^(\d+)([kmnu])(\d+)$',r'\1.\3\2',s)
 m=re.fullmatch(r'([\d.e+-]+)([kmnu]?)',s)
 assert m,s
 return float(m[1])*{'':1,'k':1e3,'m':1e-3,'u':1e-6,'n':1e-9}[m[2]]

checked=[]
dnp={'R17','R18'}
for ref,c in components.items():
 if ref in dnp or not ref.startswith(('R','C','D')) or ref=='R5': continue
 key='X'+ref if ref in {'D1','D3','D4'} else ref
 assert key in lines,(ref,'missing from release model')
 line=lines[key]
 expected=[pins[(ref,'1')],pins[(ref,'2')]]
 actual=[x.upper() for x in line[1:3]]
 if ref=='D3': assert line[3].upper()=='GND' and line[4]=='STPST10H100SB', 'D3 second anode/model mismatch'
 if ref=='D3': expected.reverse() # KiCad K=1/A=2; SPICE A,K.
 # D1/D4 are bidirectional TVSs; their textual orientation is immaterial.
 assert (actual==expected if ref=='D3' else sorted(actual)==sorted(expected)),(ref,actual,expected)
 if ref.startswith(('R','C')):
  token=line[3].strip('{}')
  base=token.split('*')[0].split('/')[0]
  if base in params: base=params[base]
  modeled=val(base); schematic_value=val(c.findtext('value'))
  assert abs(modeled-schematic_value)<max(abs(schematic_value)*1e-9,1e-15),(ref,modeled,schematic_value)
 checked.append(ref)

assert lines['RSH'][1:4]==['SHUNT_HI','SHUNT_LO','{RSHUNT}']
assert params['RSHUNT']=='5m'
assert lines['XU1'][1:11]==['VBAT_FUSED','N_UV','N_OV','N_RETRY','GND','SHDN_LTC','FAULT','SHUNT_LO','SHUNT_HI','GP']
assert lines['XU3'][1:9]==['V3V3','PDB_LDO_ADJ','NC3','GND','VOUT','NC6','NC7','VOUT']
assert lines['XU5'][1:7]==['VBAT_FUSED','IDEAL_GATE','IDEAL_IN','IDEAL_IN','IDEAL_IN','IDEAL_VSS']
report={'components':59,'bom_files_match':True,'live_netlist':str(live),
 'passive_connectivity_and_values_checked':checked,'dnp_not_instantiated':sorted(dnp),
 'shunt_ohms':0.005,'spice_model':'pdb/pdb_release.lib',
 'limitations':'IC behavior, connector resistance, Kelvin force stubs, SOA, fuse clearing, thermal behavior and Osiris load profiles remain separately qualified assumptions.'}
(audit/'connectivity.json').write_text(json.dumps(report,indent=2))
print('PASS: 59 live symbols; both BOMs match; A-P4 release-model passive nets/values and controller/LDO/ideal-diode pin order checked.')
