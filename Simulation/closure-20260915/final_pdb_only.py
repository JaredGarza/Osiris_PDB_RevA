"""Finalize a PDB-only candidate for the established Osiris 7 W Jetson budget."""
from pathlib import Path
import re,json,shutil
H=Path(__file__).resolve().parent;R=H.parents[1];S=H.parent/'combined-20260915'
model=(S/'pdb/pdb_only_5m.lib').read_text().replace('R1V=249k','R1V=237k').replace('RHV_GP=4.99Meg','RHV_GP=22Meg')
model=model.replace('standard 10 mOhm shunt','standard 5 mOhm shunt')
(S/'pdb/pdb_final.lib').write_text(model)
for source,name in [('pdb5_corners','final_corners'),('pdb5_lowtrip','final_lowtrip')]:
 s=(S/(source+'.cir')).read_text().replace('pdb_only_5m.lib','pdb_final.lib')
 s=s.replace('* Battery -> PDB (A-P2-DRAFT)', '* Battery -> PDB (A-P3-DRAFT)')
 s=s.replace('* 300..2000 V/s is a sensitivity range, not a vendor guaranteed range.', '* 12.14..60 V/ms eFuse sensitivity; 60 V/ms is an assumed stress value.')
 s=s.replace('.end','.meas TRAN INRUSH_I2T INTEG I(RBATT)*I(RBATT) FROM 0 TO 100m\n.meas TRAN POUT_STEP AVG V(PDBOUT)*I(LCBL) FROM 700m TO 890m\n.end')
 (S/(name+'.cir')).write_text(s)
for source,name in [('eco_faults','final_faults'),('eco_faults_fine','final_faults_fine'),('eco_reverse','final_reverse'),('eco_reverse25','final_reverse25'),('eco_transients','final_transients'),('eco_weak_source','final_weak_source')]:
 s=(S/(source+'.cir')).read_text().replace('pdb_eco.lib','pdb_final.lib').replace('osiris_eco.lib','osiris_reva.lib')
 s=s.replace('+ PARAMS: SR21=1200\n','')
 (S/(name+'.cir')).write_text(s)
s=(S/'final_corners.cir').read_text().replace('.step param CASE list 1 2 3 4 5 6 7 8','.step param CASE list 1 2 3 4 5 6 7 8\n.step temp list 0 60')
(S/'final_temperature.cir').write_text(s)
schematic=R/'Osiris_PDB_RevA.kicad_sch';s=schematic.read_text()
shutil.copy2(schematic,H/'before-pdb-only.kicad_sch')
changes={
 'R1':{'Value':'237k','MPN':'RC0805FR-07237KL','Datasheet':'https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-07237KL','Selection_Status':'1% 0805 UV divider. Selected for cold-start threshold margin at 12 V; see A-P3 calculation report.'},
 'R14':{'Value':'22M','MPN':'RC0805JR-0722ML','Datasheet':'https://yageogroup.com/component-documentation/download/specsheet/RC0805JR-0722ML','Selection_Status':'22 MOhm 5% gate feedback. Manufacturer order code verified; tolerance included in divider calculation.'},
 'R5':{'Value':'5m','MPN':'FC4L64R005FER','Selection_Status':'5 mOhm 1% 2 W four-terminal. Nominal breaker 10 A; normal-condition range 7.92-12.12 A. F1 remains 4 A; conductor/fuse coordination required.'},
 'C1':{'Selection_Status':'22 nF 5% C0G in series with R4 from GATE_PIN to GND. PDB-only candidate; original Osiris eFuse configuration retained.'}
}
for m in list(re.finditer(r'^\t\(symbol\n.*?^\t\)',s,re.M|re.S)):
 b=m[0];ref=re.search(r'\(property "Reference" "([^"]+)"',b)[1]
 if ref not in changes:continue
 q=b
 for k,v in changes[ref].items():
  pat=r'(\(property "'+re.escape(k)+r'" )"(?:\\.|[^"\\])*"'
  assert re.search(pat,q),(ref,k)
  q=re.sub(pat,lambda m:m[1]+json.dumps(v),q,count=1)
 s=s.replace(b,q,1)
s=s.replace('R5=10 mOhm; 50 uA/LSB: SHUNT_CAL=6554.','R5=5 mOhm; 50 uA/LSB: SHUNT_CAL=3277.')
s=s.replace('Osiris U21/U22/U4 require DVDT capacitors;\\nsee Simulation/closure-20260915/OSIRIS-ECO.md.', 'Existing Osiris input circuitry retained.\\nLoad model includes the planned 7 W Jetson mode.')
schematic.write_text(s)
parts=[]
for m in re.finditer(r'^\t\(symbol\n.*?^\t\)',s,re.M|re.S):
 p={a:json.loads('"'+b+'"') for a,b in re.findall(r'\(property "([^"]+)" "((?:\\.|[^"\\])*)"',m[0])}
 if p['Reference'].startswith('#'):continue
 p['DNP']='(dnp yes)' in m[0];parts.append(p)
(S/'audit/components.json').write_text(json.dumps(parts,indent=2))
check=H/'check_eco.py';t=check.read_text().replace('pdb/pdb_eco.lib','pdb/pdb_final.lib').replace("params['RSHUNT']=='10m'","params['RSHUNT']=='5m'")
check.write_text(t)
builder=S/'audit/reconcile_bom.mjs';t=builder.read_text().replace('10 mOhm, 1%, 2 W four-terminal','5 mOhm, 1%, 2 W four-terminal')
t=t.replace("if(/^R1[3-8]$/.test(p.Reference))", "if(/^R1[3-8]$/.test(p.Reference))")
t=t.replace("if(p.DNP)row", "if(p.Reference==='R14')row[header.indexOf('Specification')]='22 MOhm, 5%, 0805';\n  if(p.DNP)row")
builder.write_text(t)
print('Applied final PDB-only candidate; Osiris hardware and default model retained.')
