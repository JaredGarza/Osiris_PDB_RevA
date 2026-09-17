from pathlib import Path
import re, json, shutil, xml.etree.ElementTree as E
root = Path(__file__).resolve().parents[3]
audit = Path(__file__).resolve().parent
p = root/'Osiris_PDB_RevA.kicad_sch'
s = p.read_text()
s = s.replace('2.2k pull-ups on Osiris FMU 3.3 V only.', 'R17/R18: 4.7k pull-ups to local PDB_3V3.')
s = s.replace('U2 address 0x40; ADCRANGE=0, 5 mOhm shunt.', 'U2: 0x40, ADCRANGE=0, 8 mOhm shunt.\\n50 uA/LSB: SHUNT_CAL=5243; check on bench.')
s = s.replace('F1 remains provisional 4 A;', 'F1 remains provisional 5 A;')
status = {
 'F1':'Provisional 5 A. Conductor, holder, fault-current and thermal coordination not qualified.',
 'R5':'8 mOhm candidate. 6.25 A nominal breaker; 4.95-7.58 A with 1% shunt and 40-60 mV controller limits. Verify exact order code and pulse rating.',
 'R14':'20 MOhm gate-to-UV feedback. Exact order code, tolerance, leakage and temperature corners require qualification.',
 'R17':'Local 4.7k I2C pull-up. Account for host pull-ups and mixed-power backfeed before connection.',
 'R18':'Local 4.7k I2C pull-up. Account for host pull-ups and mixed-power backfeed before connection.'}
def edit(m):
 b=m[0]; ref=re.search(r'\(property "Reference" "([^"]+)"',b)[1]
 if ref=='F1': b=b.replace('4 A, 32 VDC MINI', '5 A, 32 VDC MINI')
 if ref=='R5': b=b.replace('5 mOhm', '8 mOhm')
 if ref in status:
  b=re.sub(r'(\(property "Selection_Status" ")[^"]*',lambda m:m[1]+status[ref],b)
 # The former divider resistor's datasheet must follow its new value/order code.
 if ref in ('R1','R2','R3','R13'):
  mpn=re.search(r'\(property "MPN" "([^"]+)"',b)[1]
  b=re.sub(r'(\(property "Datasheet" ")[^"]*',lambda m:m[1]+'https://yageogroup.com/component-documentation/download/specsheet/'+mpn,b)
 return b
s=re.sub(r'^\t\(symbol\n.*?^\t\)',edit,s,flags=re.M|re.S)
p.write_text(s)
for name in ('README.md','DESIGN-SPEC.md'):
 p=root/name; s=p.read_text().replace('42-component','48-component').replace('42 components','48 components')
 s=s.replace('provisional 4 A F1','provisional 5 A F1').replace('5 mΩ shunt','8 mΩ shunt')
 s=s.replace('Nominal UV/OV thresholds: 10.56/18.68 V. Nominal electronic breaker: 10 A.', 'Gate-feedback UV thresholds require corner validation; nominal OV is about 18.7 V. Nominal electronic breaker: 6.25 A.')
 s=s.replace('\n\n', '\n\nCurrent simulation/design audit: [review](Simulation/combined-20260915/REVIEW.md). This supersedes earlier population and simulation claims.\n\n',1)
 p.write_text(s)
p=root.parent.parent/'README.md'
s=p.read_text().replace('42-component','48-component'); p.write_text(s)

# Source data for the BOM editor, extracted from actual symbol instances.
components=[]
for b in re.findall(r'^\t\(symbol\n.*?^\t\)',(root/'Osiris_PDB_RevA.kicad_sch').read_text(),re.M|re.S):
 props=dict(re.findall(r'\(property "([^"]+)" "([^"]*)"',b))
 if props['Reference'].startswith('#'): continue
 components.append(props)
(audit/'components.json').write_text(json.dumps(components,indent=2))
for name in ('BOM.csv','BOM_purchasing.csv'):
 dest=audit/('before-'+name)
 if not dest.exists(): shutil.copy2(root/name,dest)
