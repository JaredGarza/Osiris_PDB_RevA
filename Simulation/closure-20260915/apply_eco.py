"""Apply the reviewed gate and procurement ECO without moving unrelated objects."""
from pathlib import Path
import re,json,shutil
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sch=ROOT/'Osiris_PDB_RevA.kicad_sch'
s=sch.read_text()
assert '(rev "A-P2-DRAFT")' in s, 'ECO already applied or unexpected revision'
for name in ('BOM.csv','BOM_purchasing.csv'):
 shutil.copy2(ROOT/name,HERE/('before-'+name))
def prop(block,key,value):
 pat=r'(\(property "'+re.escape(key)+r'" )"(?:\\.|[^"\\])*"'
 if not re.search(pat,block):
  return block[:-1]+'\t(property '+json.dumps(key)+' '+json.dumps(value)+' (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))\n\t)'
 return re.sub(pat,lambda m:m[1]+json.dumps(value),block,count=1)
changes={
 'R1':{'Value':'249k','MPN':'RC0805FR-07249KL','Datasheet':'https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-07249KL','Selection_Status':'1% 0805; UV divider scaled down to reduce leakage sensitivity.'},
 'R2':{'Value':'11k8','MPN':'RC0805FR-0711K8L','Datasheet':'https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-0711K8L','Selection_Status':'1% 0805; lower UV divider resistor.'},
 'R14':{'Value':'4M99','MPN':'RC0805FR-074M99L','Datasheet':'https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-074M99L','Selection_Status':'1% 0805 candidate; confirm exact manufacturer order code before procurement. Gate-to-UV feedback.'},
 'R4':{'Description':'Series resistor in gate-to-ground timing branch','Selection_Status':'U1 GATE directly drives Q1/Q2. R4 is in series with C1 to ground, per LTC4368 Figure 7.'},
 'C1':{'Value':'22n','MPN':'C2012C0G2A223J125AC','Datasheet':'https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012C0G2A223J125AC','Description':'22 nF 100 V C0G 5%','Selection_Status':'Series with R4 from GATE_PIN to GND; requires downstream controlled slew. See A-P3 ECO report.'},
 'R5':{'Value':'10m','MPN':'FC4L64R010FER','Datasheet':'https://www.ohmite.com/res-fc4l/','Description':'10 mOhm 1% 2 W four-terminal current shunt','Selection_Status':'Standard series value; nominal breaker 5 A, normal threshold range 3.96-6.06 A including resistor tolerance. Pulse qualification pending.'},
 'F1':{'Value':'4A MINI','MPN':'0297004.WXNV','Selection_Status':'4 A 32 V MINI; load envelope 2.5 A maximum. Fuse, source and conductor coordination remains a release requirement.'},
 'R17':{'Description':'Optional SCL pull-up; do not populate','Selection_Status':'DNP: host owns pull-up to its switched 3.3 V rail. No local pull-up is allowed with an independently powered host.'},
 'R18':{'Description':'Optional SDA pull-up; do not populate','Selection_Status':'DNP: host owns pull-up to its switched 3.3 V rail. No local pull-up is allowed with an independently powered host.'},
}
blocks=list(re.finditer(r'^\t\(symbol\n.*?^\t\)',s,re.M|re.S))
seen=set()
for m in blocks:
 block=m[0]
 ref=re.search(r'\(property "Reference" "([^"]+)"',block)[1]
 if ref=='D2':s=s.replace(block+'\n','',1);continue
 if ref not in changes:continue
 q=block
 for key,value in changes[ref].items():q=prop(q,key,value)
 if ref in ('R17','R18'):q=q.replace('(dnp no)','(dnp yes)')
 s=s.replace(block,q,1);seen.add(ref)
assert seen==set(changes)
for m in list(re.finditer(r'^\t\(label .*?^\t\)',s,re.M|re.S)):
 b=m[0]
 if '(at 50.8 116.84 0)' in b or '(at 50.8 124.46 0)' in b:
  s=s.replace(b+'\n','',1);continue
 q=b.replace('"GATE_FET"','"GATE_PIN"')
 if '(at 33.02 105.41 0)' in b:q=q.replace('"GATE_PIN"','"GATE_RC"')
 s=s.replace(b,q,1)
texts=[
 'J2: 1 NC, 2 SCL, 3 SDA, 4 GND.\nR17/R18 DNP; host supplies 3.3 V pull-ups.\n100 kHz maximum; 200 pF bus assumption.\nVerify unpowered behavior and cable pinout.\n\nINA228: address 0x40, ADCRANGE=0.\nR5=10 mOhm; 50 uA/LSB: SHUNT_CAL=6554.\nCalibrate assembled board.\nFAULT / ALERT: TP7 / TP6 only.',
 '4S input: 12-16.8 V normal.\nProposed load: <=25 W AND <=2.5 A.\nStartup capacitance: <=220 uF worst-case.\n\nGATE directly drives Q1/Q2.\nR4 + C1 form a series branch to GND.\nOsiris U21/U22/U4 require DVDT capacitors;\nsee Simulation/closure-20260915/OSIRIS-ECO.md.\n\nA-P3-DRAFT: not released for fabrication.\nPin stress, SOA and source coordination open.\nSee Simulation/closure-20260915/STATUS.md.'
]
matches=list(re.finditer(r'^\t\(text "(?:\\.|[^"\\])*".*?^\t\)',s,re.M|re.S))
assert len(matches)==2
for m,t in zip(matches,texts):
 q=re.sub(r'^\t\(text "(?:\\.|[^"\\])*"',lambda _: '\t(text '+json.dumps(t),m[0],count=1)
 s=s.replace(m[0],q,1)
s=s.replace('(rev "A-P2-DRAFT")','(rev "A-P3-DRAFT")')
assert '"GATE_FET"' not in s
sch.write_text(s,encoding='utf-8',newline='\n')
parts=[]
for m in re.finditer(r'^\t\(symbol\n.*?^\t\)',s,re.M|re.S):
 p={a:json.loads('"'+b+'"') for a,b in re.findall(r'\(property "([^"]+)" "((?:\\.|[^"\\])*)"',m[0])}
 if p['Reference'].startswith('#'):continue
 p['DNP']='(dnp yes)' in m[0]
 parts.append(p)
(ROOT/'Simulation/combined-20260915/audit/components.json').write_text(json.dumps(parts,indent=2))
print(f'Applied A-P3-DRAFT: {len(parts)} symbols, {sum(not p["DNP"] for p in parts)} populated.')
