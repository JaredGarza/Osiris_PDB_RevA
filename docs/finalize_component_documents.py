from pathlib import Path
import csv, json, xml.etree.ElementTree as E

p=Path(__file__).resolve().parents[1]
r=E.parse(p/'docs/fuse-connectors.net.xml').getroot()
nets={(x.get('ref'),x.get('pin')):n.get('name') for n in r.findall('./nets/net') for x in n.findall('node')}
assert nets['J3','1']=='GND'
assert nets['J3','2']=='/PDB_VOUT'
assert nets['J1','1']=='GND'
assert nets['J1','2']=='/VBAT_RAW'
assert [nets['J2',str(i)] for i in range(1,6)]==['GND','/PDB_I2C_SDA','/PDB_I2C_SCL','/INA_ALERT_N','/PDB_FAULT_N']
rows=list(csv.DictReader((p/'BOM.csv').open(newline='',encoding='utf-8-sig')))
assert len(rows)==33 and all(x['Footprint'] for x in rows)
fields=list(rows[0]); fields.insert(1,'Quantity'); fields.append('BOM Role')
for row in rows: row.update(Quantity='1',**{'BOM Role':'Schematic component'})
f1=next(x for x in rows if x['Reference']=='F1')
row={k:'' for k in fields}
row.update(Reference='F1-holder',Quantity='1',Value='MINI fuse holder',Specification='Keystone 3568; separate purchased holder for F1',Footprint=f1['Footprint'],Manufacturer='Keystone Electronics',MPN='3568',Datasheet='${KIPRJMOD}/Datasheets/Keystone_catalog.pdf',**{'Selection Status':'Holder assigned; retention, access and vibration review pending','BOM Role':'F1 holder; same physical assembly, not an additional PCB footprint'})
rows.append(row)
with (p/'BOM_purchasing.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fields); w.writeheader(); w.writerows(rows)
sources=json.loads((p/'Datasheets/sources.json').read_text())
lines=['# Component datasheets','', 'Downloaded PDFs are stored beside this index. Sources that blocked downloading remain available as links in the schematic. The Keystone catalog is a manufacturer catalog rather than a dedicated part drawing.','', '| Document | Local file / status | Manufacturer source |','|---|---|---|']
for x in sources:
 status=f"[{x['file']}]({x['file']})" if x['status']=='downloaded' else 'Online link; PDF download unavailable'
 lines.append(f"| {x['file']} | {status} | [Source]({x['source']}) |")
lines+=['','Existing project PDFs: [LTC4368](LTC4368%20%28Rev%20C%29.pdf) and [ISC015N06NM5LF2](Datasheet%20ISC015N06NM5LF2.pdf).','','TDK links refer to characteristic sheets; the schematic retains manufacturer product pages for each selected capacitor.','']
(p/'Datasheets/README.md').write_text('\n'.join(lines),encoding='utf-8')
print('Verified J1/J3 polarity, J2 mapping, 33 assigned footprints, and 34 purchasing BOM rows.')
print('New local PDFs:',sum(x['status']=='downloaded' for x in sources))
