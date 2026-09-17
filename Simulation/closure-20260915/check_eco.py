"""Independent CAD/BOM/model consistency check for the intentional A-P3 ECO."""
from pathlib import Path
import csv,json,re,xml.etree.ElementTree as ET
H=Path(__file__).resolve().parent;R=H.parents[1];S=H.parent/'combined-20260915'
old=ET.parse(S/'audit/final.net.xml').getroot()
new=ET.parse(H/'eco.net.xml').getroot()
def pinmap(t):
 return {(n.get('ref'),n.get('pin')):net.get('name') for net in t.findall('nets/net') for n in net.findall('node')}
a,b=pinmap(old),pinmap(new)
expected_changes={('Q1','4'):'/GATE_PIN',('Q2','4'):'/GATE_PIN',('R4','1'):'/GATE_PIN',('R4','2'):'/GATE_RC',('C1','1'):'/GATE_RC'}
for key,value in a.items():
 if key[0]=='D2':assert key not in b;continue
 assert b[key]==expected_changes.get(key,value),(key,value,b[key])
assert set(b)=={k for k in a if k[0]!='D2'}
components={c.get('ref'):c for c in new.findall('components/comp')}
assert len(components)==47 and 'D2' not in components
for name in ('BOM.csv','BOM_purchasing.csv'):
 rows={r['Reference']:r for r in csv.DictReader((R/name).open(encoding='utf-8-sig'))}
 assert 'D2' not in rows
 for ref,c in components.items():
  fields={f.get('name'):f.text or '' for f in c.findall('fields/field')}
  for field,value in [('Value',c.findtext('value')),('Footprint',c.findtext('footprint')),('MPN',fields.get('MPN',''))]:
   assert rows[ref][field]==value,(name,ref,field)
  if ref in ('R17','R18'):
   assert 'DNP' in rows[ref]['Selection Status']
   if 'Quantity' in rows[ref]:assert str(rows[ref]['Quantity'])=='0'
model=(S/'pdb/pdb_final.lib').read_text()
lines={l.split()[0]:l.split() for l in model.splitlines() if l and not l.startswith(('*','+','.'))}
params=dict(re.findall(r'(\w+)=([\w.]+)',model))
aliases={'GND':'GND','/LTC_UV':'N_UV','/LTC_OV':'N_OV','Net-(U1-RETRY)':'N_RETRY','/GATE_PIN':'GP','/GATE_RC':'GATE_RC','/SW_COMMON':'COMMON','/PDB_VOUT':'VOUT','/PDB_3V3':'V3V3','/PDB_FAULT_N':'FAULT','/INA_ALERT_N':'ALERT','/PDB_I2C_SCL':'SCL','/PDB_I2C_SDA':'SDA'}
def value(s):
 s=s.replace('Meg','M').replace('U','u').replace('N','n').replace('K','k')
 m=re.fullmatch(r'(\d+(?:\.\d+)?)([RrkmMnu]?)(\d*)',s)
 assert m,s
 mantissa=float(m[1]+('.'+m[3] if m[3] else ''))
 return mantissa*{'':1,'R':1,'r':1,'k':1e3,'m':1e-3,'M':1e6,'n':1e-9,'u':1e-6}[m[2]]
checked=[]
for ref,c in components.items():
 if not ref.startswith(('R','C','D')) or ref in ('R5','R17','R18'):continue
 line=lines['XD1' if ref=='D1' else ref]
 nets=[aliases.get(b[(ref,p)],b[(ref,p)].lstrip('/')).upper() for p in ('1','2')]
 if ref=='D3':nets.reverse()
 actual=[n.upper() for n in line[1:3]]
 assert (actual==nets if ref=='D3' else sorted(actual)==sorted(nets)),(ref,actual,nets)
 if ref[0] in 'RC':
  v=line[3].strip('{}')
  for k,p in params.items():v=v.replace(k,p)
  assert abs(value(v.split('*')[0])-value(c.findtext('value')))<max(value(c.findtext('value'))*1e-10,1e-15),ref
 checked.append(ref)
assert params['RSHUNT']=='5m'
assert 'D2' not in lines and 'R17' not in lines and 'R18' not in lines
assert lines['XU1'][1:11]==['VBAT_FUSED','N_UV','N_OV','N_RETRY','GND','SHDN_LTC','FAULT','SHUNT_LO','SHUNT_HI','GP']
assert lines['XU3'][1:9]==['V3V3','PDB_LDO_ADJ','NC3','GND','VOUT','NC6','NC7','VOUT']
before=(S/'osiris/osiris_reva.lib').read_text()
after=(S/'osiris/osiris_eco.lib').read_text()
def devices(s):
 return [l for l in s.splitlines() if l and l[0] not in '*+.']
assert devices(before)==devices(after),'Unexpected change to Osiris device network'
report={'status':'PASS','symbols':47,'populated':45,'intentional_pin_changes':{':'.join(k):v for k,v in expected_changes.items()},'other_pin_nets_preserved':True,'removed':'D2','DNP':['R17','R18'],'both_BOMs_match':True,'passives_checked':checked,'Osiris_device_network_preserved':True,'limitations':'SPICE IC behavior and PCB parasitics are not validated by connectivity checks.'}
(H/'connectivity.json').write_text(json.dumps(report,indent=2))
print('PASS: intentional gate ECO only; all other pin nets preserved; 47 symbols / 45 populated; both BOMs and model values match.')
