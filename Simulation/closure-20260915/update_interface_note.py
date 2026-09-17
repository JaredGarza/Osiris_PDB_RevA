from pathlib import Path
import re,json
H=Path(__file__).resolve().parent; R=H.parents[1]
p=R/'Osiris_PDB_RevA.kicad_sch';s=p.read_text()
s=s.replace('100 kHz maximum; 200 pF bus assumption.', '100 kHz; <=90 pF total with Osiris 12k pull-ups.')
s=s.replace('proposed Osiris 3.3 V pull-ups, 100 kHz, <=200 pF bus.', 'Osiris R74/R75 12k pull-ups to switched 3.3 V; 100 kHz, <=90 pF total bus capacitance.')
p.write_text(s)
parts=[]
for m in re.finditer(r'^\t\(symbol\n.*?^\t\)',s,re.M|re.S):
 d={a:json.loads('"'+b+'"') for a,b in re.findall(r'\(property "([^"]+)" "((?:\\.|[^"\\])*)"',m[0])}
 if d['Reference'].startswith('#'):continue
 d['DNP']='(dnp yes)' in m[0];parts.append(d)
(H.parent/'combined-20260915/audit/components.json').write_text(json.dumps(parts,indent=2))
