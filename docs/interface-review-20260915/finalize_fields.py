from pathlib import Path
import csv,io,re
root=Path(__file__).resolve().parents[2]
p=root/'Osiris_PDB_RevA.kicad_sch'
s=p.read_text(encoding='utf-8')
updates={
 'D3':{'Description':'Negative-output clamp candidate: anode GND, cathode PDB_VOUT. INA228 negative-pin limits remain unqualified.',
       'Selection_Status':'OPEN: MBR0540 does not guarantee a -0.3 V clamp at INA228 IN+/IN-/VBUS. U3 now has separate reverse protection. See September 15 review.'},
 'C6':{'Selection_Status':'A-P2 LT3010 output capacitor: require >=1 uF effective over bias/temperature and ESR <=3 ohms. Confirm manufacturer bias curve and assembled stability.'}
}
def edit(m):
    b=m[0]
    ref=re.search(r'\(property "Reference" "([^"]+)"',b)
    if not ref or ref[1] not in updates:return b
    if ref[1]=='C6':
        b=b.replace('(justify left)','(justify right)')
        b=re.sub(r'(\(property "Description" "[^"]*"\n\s*)\(at [^)]*\)',lambda m:m[1]+'(at 101.6 154.94 0)',b,count=1)
    for k,v in updates[ref[1]].items():
        b,n=re.subn(r'(\(property "'+k+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+'"'+v+'"',b,count=1)
        assert n==1
    return b
s=re.sub(r'^\t\(symbol\n.*?^\t\)',edit,s,flags=re.M|re.S)
p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
for name in ('BOM.csv','BOM_purchasing.csv'):
    path=root/name;data=path.read_bytes();prefix=b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b''
    lines=data.decode('utf-8-sig').splitlines(keepends=True);header=next(csv.reader([lines[0]]));out=[lines[0]]
    for line in lines[1:]:
        row=dict(zip(header,next(csv.reader([line]))))
        if row['Reference'] in updates:
            for k,v in updates[row['Reference']].items():row[{'Description':'Specification','Selection_Status':'Selection Status'}[k]]=v
            b=io.StringIO(newline='');csv.writer(b,lineterminator='\r\n').writerow([row[k] for k in header]);out.append(b.getvalue())
        else:out.append(line)
    path.write_bytes(prefix+''.join(out).encode('utf-8'))
