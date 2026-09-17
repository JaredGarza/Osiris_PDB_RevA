"""Validate physical pins and unchanged wiring against the prior A-P3 netlist."""
from pathlib import Path
import xml.etree.ElementTree as ET,json
H=Path(__file__).resolve().parent
def pins(path):
 root=ET.parse(path).getroot()
 return {(n.get('ref'),n.get('pin')):net.get('name') for net in root.findall('nets/net') for n in net.findall('node')}
a=pins(H/'eco.net.xml');b=pins(H/'release.net.xml')
changes=[(ref,p,a[(ref,p)],net) for (ref,p),net in b.items() if (ref,p) in a and net!=a[(ref,p)]]
print('Changed prior pins:',changes)
for ref in ['U5','Q3','D4','C11','C15','C12','C13','C14','C16','R19','R20','R21']:
 print(ref,{p:n for (r,p),n in b.items() if r==ref})
expected={
 'U5':{'1':'IDEAL_GATE','2':'IDEAL_IN','4':'IDEAL_IN','5':'IDEAL_IN','6':'IDEAL_VSS','8':'VBAT_FUSED'},
 'Q3':{'1':'IDEAL_IN','2':'IDEAL_IN','3':'IDEAL_IN','4':'IDEAL_GATE','5':'VBAT_FUSED','6':'VBAT_FUSED','7':'VBAT_FUSED','8':'VBAT_FUSED'},
 'R19':{'1':'IDEAL_VSS','2':'GND'},'R20':{'1':'IDEAL_IN','2':'INPUT_DAMP'},'R21':{'1':'PDB_VOUT','2':'INA_VBUS'},
 'C11':{'1':'VBAT_FUSED','2':'IDEAL_VSS'},'C15':{'1':'VBAT_FUSED','2':'IDEAL_VSS'},
 'C12':{'1':'INA_IN_P','2':'GND'},'C13':{'1':'INA_IN_N','2':'GND'},'C14':{'1':'INA_VBUS','2':'GND'},'C16':{'1':'INPUT_DAMP','2':'GND'},
 'F1':{'2':'IDEAL_IN'},'U2':{'8':'INA_VBUS'},'D3':{'1':'PDB_VOUT','2':'GND'}}
for ref,ps in expected.items():
 for pin,net in ps.items():assert b[(ref,pin)].lstrip('/')==net,(ref,pin,net,b.get((ref,pin)))
assert {b[('D4',p)].lstrip('/') for p in ('1','2')}=={'IDEAL_IN','IDEAL_VSS'}
allowed={('F1','2'),('TP1','1'),('U2','8')}
for ref,p,old,new in changes:
 assert (ref,p) in allowed,(ref,p,old,new)
(H/'release-connectivity.json').write_text(json.dumps({'status':'PASS','changed_prior_pins':changes,'new_pin_maps':expected},indent=2))
print('PASS: selected input stage and sensor filters match intended pin maps.')
