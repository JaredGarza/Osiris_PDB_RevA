from pathlib import Path
import re, uuid
p=Path(__file__).resolve().parents[2]/'Osiris_PDB_RevA.kicad_sch'
s=p.read_text(encoding='utf-8')
assert '(label "PDB_LDO_ADJ" (at 81.28 153.67 0)' in s
s=s.replace('(label "PDB_LDO_ADJ" (at 81.28 153.67 0)', '(label "PDB_LDO_ADJ" (at 83.82 166.37 0)',1)
s=s.replace('(label "GND" (at 121.92 182.88 0)','(label "GND" (at 121.92 185.42 0)',1)
added=''
for xy in [(81.28,153.67,83.82,153.67),(83.82,153.67,83.82,166.37),(121.92,182.88,121.92,185.42)]:
    a,b,c,d=xy
    added+=f'\t(wire (pts (xy {a} {b}) (xy {c} {d})) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))\n'
s=s.rstrip()[:-1]+added+')\n'
def edit(m):
    b=m[0]
    if '(property "Reference" "C6"' in b:
        places={'Reference':(96.52,149.86,0),'Value':(96.52,152.4,0),'Description':(96.52,154.94,0)}
    elif '(property "Reference" "D3"' in b:
        places={'Reference':(116.84,152.4,270),'Value':(116.84,154.94,270)}
    else:return b
    for key,(x,y,a) in places.items():
        pat=r'(\(property "'+key+r'" "[^"]*"\n\s*)\(at [^)]*\)'
        b,n=re.subn(pat,lambda m:m[1]+f'(at {x} {y} {a})',b,count=1)
        assert n==1
    if '(property "Reference" "D3"' in b:
        b=b.replace('(justify right)','(justify left)')
    return b
s=re.sub(r'^\t\(symbol\n.*?^\t\)',edit,s,flags=re.M|re.S)
notes=[
 'J2: 1 NC, 2 SCL, 3 SDA, 4 GND.\nNew Osiris pin mapping and cable fit unverified.\n\nPROPOSED: 100 kHz, <=200 pF total I2C bus;\n2.2k pull-ups on Osiris FMU 3.3 V only.\nU2 address 0x40; ADCRANGE=0, 5 mOhm shunt.\n\nINA_ALERT_N / PDB_FAULT_N: TP6/TP7 only.\nNo alert wires or power feed through J2.\n\nSee docs/PDB-INTERFACE-PROPOSAL-20260915.md.\nFinal loads and mechanical fit are undecided.',
 'PROPOSED: raw 4S avionics feed, 12-16.8 V normal.\nJ3 load <=25 W AND <=2.5 A; not a tested rating.\nTotal startup capacitance <=220 uF worst-case.\n\nU3 LT3010 + R11/R12/C10: nominal 3.29 V.\nReverse-input/current protection added.\n\nJ3: 1=GND, 2=PDB_VOUT; verify physical polarity.\n\nOPEN: INA228 negative-input clamp, real FET\nfault/retry SOA, TVS energy and source fault current.\nF1 remains provisional 4 A; interrupt rating 1000 A.\n\nA-P2-DRAFT is not a fabrication release.\nSee docs/PDB-ELECTRICAL-REVIEW-20260915.md.'
]
idx=iter(notes)
def note(m):
    text=next(idx).replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')
    return '\t(text "'+text+'"'
s,n=re.subn(r'^\t\(text "(?:\\.|[^"\\])*"',note,s,flags=re.M)
assert n==2
p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
