"""Finish CAD presentation and create a separate, explicitly scoped Osiris change sheet."""
from pathlib import Path
import re,json,uuid
H=Path(__file__).resolve().parent;R=H.parents[1]
p=R/'Osiris_PDB_RevA.kicad_sch';s=p.read_text()
s=s.replace('(property "Description" "10 mOhm 1% 2 W four-terminal current shunt"','(property "Description" "1% 2W"')
s=s.replace('(property "Description" "22 nF 100 V C0G 5%"','(property "Description" "100V C0G 5%"')
p.write_text(s)
def block_at(t,start):
 depth=0;quoted=False;escaped=False
 for i in range(start,len(t)):
  c=t[i]
  if quoted:
   if escaped:escaped=False
   elif c=='\\':escaped=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if not depth:return t[start:i+1]
 raise ValueError('unbalanced')
lib=block_at(s,s.index('(symbol "Device:C"'))
uid=lambda:str(uuid.uuid4())
sheetid=uid()
out=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{sheetid}") (paper "A4")\n(title_block (title "Osiris - eFuse slew control change sheet") (date "2026-09-15") (rev "ECO-1-DRAFT"))\n(lib_symbols {lib})\n'
for ref,target,x in [('C901','U21',50.8),('C902','U22',127.0),('C903','U4',203.2)]:
 out+=f'(symbol (lib_id "Device:C") (at {x} 76.2 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid "{uid()}")\n'
 for k,v,dy,hide in [('Reference',ref,-2.54,False),('Value','3n3',0,False),('Footprint','Capacitor_SMD:C_0603_1608Metric',0,True),('Datasheet','https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608C0G1H332J080AA',0,True),('MPN','C1608C0G1H332J080AA',0,True),('Manufacturer','TDK',0,True)]:
  out+=f'(property {json.dumps(k)} {json.dumps(v)} (at {x+5.08} {76.2+dy} 0) '+('(hide yes)' if hide else '')+' (effects (font (size 1.27 1.27)) (justify left)))\n'
 out+=f'(pin "1" (uuid "{uid()}")) (pin "2" (uuid "{uid()}")) (instances (project "Osiris_Power_Input_ECO" (path "/{sheetid}" (reference "{ref}") (unit 1)))))\n'
 for name,y in [(target+'_DVDT_PIN7',72.39),('GND',80.01)]:
  out+=f'(label "{name}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid()}"))\n'
 for text,y in [(target+' LM73100RPWR',55.88),('50 V C0G, 5%',91.44)]:
  out+=f'(text "{text}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{uid()}"))\n'
notes='CHANGE SHEET ONLY - integrate into the original Osiris Altium design.\nConnect each upper terminal directly to the named IC DVDT pin 7.\nConnect each lower terminal to that IC ground pin 8 with a short, quiet return.\nRemove the corresponding no-connect marker. Verify reference numbers on integration.\n\nThese three capacitors are required by the combined ECO simulation.\nThey have not been installed in the original Altium schematic or PCB.\nSee OSIRIS-ECO.md for the source pin mapping and verification limits.'
out+=f'(text {json.dumps(notes)} (at 25.4 114.3 0) (effects (font (size 1.5 1.5)) (justify left top)) (uuid "{uid()}"))\n)\n'
(H/'Osiris_Power_Input_ECO.kicad_sch').write_text(out)
print('Shortened overlapping component description; created explicit Osiris ECO change sheet.')
