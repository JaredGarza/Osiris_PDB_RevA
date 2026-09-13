from pathlib import Path
import re, uuid

root = Path(__file__).resolve().parents[1]
path = root / 'Osiris_PDB_RevA.kicad_sch'
text = path.read_text(encoding='utf-8')
original = text
pattern = re.compile(r'^\t\(symbol\n.*?^\t\)', re.M | re.S)
tdk = 'https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no='
caps = {
 'C1': ('C2012C0G2A562J125AA','0805_2012','TDK', '100V C0G/NP0'),
 'C2': ('C2012X7R1H105K125AB','0805_2012','TDK', '50V X7R'),
 'C3': ('C0603C104K4RACTU','0603_1608','KEMET', '16V X7R'),
 'C4': ('C3216X7R1H106K160AC','1206_3216','TDK', '50V X7R'),
 'C5': ('C0603C104K4RACTU','0603_1608','KEMET', '16V X7R'),
 'C6': ('C2012X7R1A106K125AC','0805_2012','TDK', '10V X7R'),
 'C7': ('C1608X7R1H104K080AA','0603_1608','TDK', '50V X7R'),
 'C8': ('C0603C104K4RACTU','0603_1608','KEMET', '16V X7R'),
}
def quoted(s):
 return '"' + s.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n') + '"'
def prop(block, key, value):
 pat = r'(\(property "'+re.escape(key)+r'" )"(?:\\.|[^"\\])*"'
 if re.search(pat, block):
  return re.sub(pat, lambda m: m[1]+quoted(value), block, count=1)
 at = re.search(r'\(at ([\d.-]+) ([\d.-]+)',block)
 item = f'\n\t\t(property {quoted(key)} {quoted(value)} (at {at[1]} {at[2]} 0) (effects (font (size 1.27 1.27)) (hide yes)))'
 return block[:-3] + item + '\n\t)'
def edit(m):
 b=m[0]
 ref=re.search(r'\(property "Reference" "([^"]+)"',b)[1]
 if ref in caps:
  mpn, size, maker, spec=caps[ref]
  fields={'Footprint':f'Capacitor_SMD:C_{size}Metric','MPN':mpn,'Manufacturer':maker,'Description':spec,
   'Datasheet':tdk+mpn if maker=='TDK' else 'https://search.kemet.com/component-documentation/download/specsheet/'+mpn,
   'Selection_Status':'Nominal specification verified; DC-bias and circuit validation pending'}
 elif ref.startswith('R') and ref!='R5':
  fields={'Footprint':'Resistor_SMD:R_0805_2012Metric','Selection_Status':'Package assigned; MPN and power/tolerance validation pending'}
 elif ref.startswith('TP'):
  fields={'Footprint':'TestPoint:TestPoint_Pad_D1.5mm','Selection_Status':'Bare copper test pad; no fitted part required'}
 elif ref in ['J1','J2','J3','F1']:
  fields={'Selection_Status':'Pending current budget and mating/mechanical requirements' if ref!='J2' else 'Pending Osiris mating connector and cable pinout'}
 else:
  return b
 for k,v in fields.items(): b=prop(b,k,v)
 return b
text=pattern.sub(edit,text)
wire='(xy 146.05 128.27) (xy 146.05 133.35)'
assert text.count(wire)==1, 'Unexpected C8 wire geometry'
text=text.replace(wire,'(xy 146.05 125.73) (xy 146.05 133.35)')
note='I²C pull-ups reside on Osiris;\nINA_ALERT_N and PDB_FAULT_N each require\na 10 kΩ pull-up to Osiris +3V3.'
assert 'I²C pull-ups reside on Osiris' not in text
text=text.rstrip()[:-1]+f'\n\t(text {quoted(note)} (at 222 109 0) (effects (font (size 1 1)) (justify left top)) (uuid "{uuid.uuid4()}"))\n)\n'
assert re.findall(r'\(uuid "([^"]+)"',original)==re.findall(r'\(uuid "([^"]+)"',text)[:-1]
shunt=lambda s: next(m[0] for m in pattern.finditer(s) if '(property "Reference" "R5"' in m[0])
assert shunt(text)==shunt(original)
for b in pattern.finditer(text):
 fp=re.search(r'\(property "Footprint" "([^"]*)"',b[0])[1]
 if fp:
  lib, name=fp.split(':',1)
  base=root/'Libraries'/f'{lib}.pretty' if lib=='PDB_Footprints' else Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')/f'{lib}.pretty'
  assert (base/f'{name}.kicad_mod').exists(),fp
path.write_text(text,encoding='utf-8',newline='\n')
print('Updated capacitor selections, passive footprints, pull-up note, and C8 wire; shunt unchanged.')
