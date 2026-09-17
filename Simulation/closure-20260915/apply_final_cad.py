"""Apply selected A-P4 hardware once, preserving existing circuit placement."""
from cad_tools import *
import shutil
p=R/'Osiris_PDB_RevA.kicad_sch';s=p.read_text()
assert '(rev "A-P3-DRAFT")' in s,'Unexpected revision or already applied'
shutil.copy2(p,H/'before-A-P4.kicad_sch')
sheetid=re.search(r'\(uuid "([^"]+)"',s)[1]
s=s.replace('(paper "A4")','(paper "A3")').replace('(rev "A-P3-DRAFT")','(rev "A-P4-DRAFT")').replace('(date "2026-09-15")','(date "2026-09-17")')
s=s.replace('Parts planning only; new Osiris Rev B power interface pending','Selected components; original Osiris hardware retained')
s=s.replace('Design review draft - see DESIGN-SPEC.md for open validation items','Electrical design draft - PCB and bench validation required')

film={'Value':'1u','Footprint':'Capacitor_THT:C_Rect_L7.2mm_W4.5mm_P5.00mm','Manufacturer':'TDK','MPN':'B32529C0105J189','Datasheet':'https://product.tdk.com/en/search/capacitor/film/rfi_general/info?part_no=B32529C0105J189','Description':'63V film 5%','Selection_Status':'Selected: 1 uF 63 V 5% polyester film. SPICE uses 0.9 uF minimum effective capacitance; verify mounted pulse and temperature behavior.'}
res19={'Value':'1k','Footprint':'Resistor_SMD:R_2512_6332Metric','Manufacturer':'Vishay','MPN':'CRCW25121001FKEGHP','Datasheet':'https://www.vishay.com/docs/20043/crcwhpe3.pdf','Description':'Pulse-rated','Selection_Status':'Selected: 1k 1% CRCW-HP 2512 reference return. Keep close to U5.'}
res20={**res19,'Value':'1','MPN':'CRCW25121R00FKEGHP','Selection_Status':'Selected: 1 ohm 1% CRCW-HP 2512 input damping. Verify pulse energy in layout/bench tests.'}
res21={'Value':'100','Footprint':'Resistor_SMD:R_0805_2012Metric','Manufacturer':'Yageo','MPN':'RC0805FR-07100RL','Datasheet':'https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-07100RL','Description':'1%','Selection_Status':'Selected: VBUS filter with C14. Allow 1 ms settling before valid measurements.'}
diode={'Value':'STPST10H100SB','Footprint':'PDB_Footprints:STPST10H100SB_DPAK','Manufacturer':'STMicroelectronics','MPN':'STPST10H100SB-TR','Datasheet':'https://www.st.com/resource/en/datasheet/stpst10h100sb.pdf','Description':'100V 10A','Selection_Status':'Selected power clamp. Connect both anode leads to GND and cathode tab to PDB_VOUT. Pulse/thermal validation required.'}
for b in blocks(s,'symbol'):
 if props(b).get('Reference')=='D3':
  q=b
  for k,v in diode.items():q=prop(q,k,v)
  s=s.replace(b,q,1)
for b in blocks(s,'label'):
 if '(at 44.45 24.13 0)' in b:s=s.replace(b,b.replace('VBAT_FUSED','IDEAL_IN'),1)
 if '(at 176.53 92.71 0)' in b:s=s.replace(b,b.replace('PDB_VOUT','INA_VBUS'),1)

# U5 MSOP8: physical pins match ADI LTC4359 Rev F pin configuration.
pins=[('1','GATE',17.78,0,180,'output'),('2','SOURCE',-17.78,0,0,'input'),('3','NC',-17.78,-10.16,0,'passive'),('4','IN',-17.78,5.08,0,'power_in'),('5','SHDN',-17.78,-5.08,0,'input'),('6','VSS',17.78,-5.08,180,'power_in'),('7','NC',17.78,-10.16,180,'passive'),('8','OUT',17.78,5.08,180,'input')]
u5='(symbol "LTC4359IMS8" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)\n'
for k,v in [('Reference','U'),('Value','LTC4359IMS8'),('Footprint','Package_SO:MSOP-8_3x3mm_P0.65mm'),('Datasheet','https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4359.pdf')]:
 u5+=f'(property {json.dumps(k)} {json.dumps(v)} (at 0 0 0) (effects (font (size 1.27 1.27))))\n'
u5+='(symbol "LTC4359IMS8_0_1" (rectangle (start -12.7 10.16) (end 12.7 -15.24) (stroke (width 0.254) (type default)) (fill (type background))))\n(symbol "LTC4359IMS8_1_1"\n'
for n,name,x,y,a,kind in pins:
 u5+=f'(pin {kind} line (at {x} {y} {a}) (length 5.08) (name "{name}" (effects (font (size 1.27 1.27)))) (number "{n}" (effects (font (size 1.27 1.27)))))\n'
u5+='))'
libpath=R/'Libraries/PDB_Symbols.kicad_sym';local=libpath.read_text()
q3=block_at(local,local.index('(symbol "ISC015N06NM5LF2"')).replace('ISC015N06NM5LF2','BSC070N10NS5')
q3=prop(q3,'Footprint','Package_TO_SOT_SMD:TDSON-8-1')
q3=prop(q3,'Datasheet','https://www.infineon.com/part/BSC070N10NS5')
for oldname in ('LTC4359IMS8','BSC070N10NS5'):
 marker='(symbol "'+oldname+'"'
 if marker in local:
  oldblock=block_at(local,local.index(marker));local=local.replace(oldblock,'',1)
libpath.write_text(local.rstrip()[:-1]+'\n'+u5+'\n'+q3+'\n)\n')
libblock=block_at(s,s.index('(lib_symbols'))
newlib=libblock[:-1]+'\n'+u5.replace('(symbol "LTC4359IMS8"','(symbol "PDB_Symbols:LTC4359IMS8"',1)+'\n'+q3.replace('(symbol "BSC070N10NS5"','(symbol "PDB_Symbols:BSC070N10NS5"',1)+'\n)'
s=s.replace(libblock,newlib,1)

added=[]
def symbol(ref,lib,x,y,a,fields,nums):
 b=f'\t(symbol (lib_id "{lib}") (at {x} {y} {a}) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid "{uid()}")\n'
 fields={'Reference':ref,**fields}
 for k,v in fields.items():
  visible=k in ('Reference','Value')
  px=x+5.08 if lib.startswith('Device:') else x
  py=y+({'Reference':-2.54,'Value':0}.get(k,0)) if lib.startswith('Device:') else y-20.32+({'Reference':0,'Value':2.54}.get(k,0))
  b+=f'(property {json.dumps(k)} {json.dumps(v)} (at {px:.2f} {py:.2f} 0) '+('' if visible else '(hide yes) ')+f'(effects (font (size 1.27 1.27))'+(' (justify left)' if lib.startswith('Device:') else '')+'))\n'
 for n in nums:b+=f'(pin "{n}" (uuid "{uid()}"))\n'
 b+=f'(instances (project "Osiris_PDB_RevA" (path "/{sheetid}" (reference "{ref}") (unit 1)))))\n'
 added.append(b)
def label(net,x,y,angle=0):
 added.append(f'\t(label "{net}" (at {x:.2f} {y:.2f} {angle}) (effects (font (size 1.27 1.27)) (justify '+('right bottom' if angle==180 else 'left bottom')+f')) (uuid "{uid()}"))\n')
def passive(ref,lib,x,y,fields,top,bottom):
 symbol(ref,lib,x,y,0,fields,['1','2'])
 label(top,x,y-3.81);label(bottom,x,y+3.81)
def text(t,x,y,size=1.5):
 added.append(f'\t(text {json.dumps(t)} (at {x} {y} 0) (effects (font (size {size} {size})) (justify left)) (uuid "{uid()}"))\n')

symbol('U5','PDB_Symbols:LTC4359IMS8',335.28,48.26,0,{'Value':'LTC4359IMS8','Footprint':'Package_SO:MSOP-8_3x3mm_P0.65mm','Manufacturer':'Analog Devices','MPN':'LTC4359IMS8#TRPBF','Datasheet':'https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4359.pdf','Description':'Reverse-current blocker','Selection_Status':'Selected: LTC4359 100 V ideal-diode controller; SHDN tied to IN. VSS return uses R19.'},[str(i) for i in range(1,9)])
netpins={'1':'IDEAL_GATE','2':'IDEAL_IN','4':'IDEAL_IN','5':'IDEAL_IN','6':'IDEAL_VSS','8':'VBAT_FUSED'}
for n,name,x,y,a,kind in pins:
 gx=335.28+x;gy=48.26-y
 if n in netpins:label(netpins[n],gx,gy,180 if x<0 else 0)
 else:added.append(f'\t(no_connect (at {gx:.2f} {gy:.2f}) (uuid "{uid()}"))\n')
symbol('Q3','PDB_Symbols:BSC070N10NS5',342.9,88.9,270,{'Value':'BSC070N10NS5','Footprint':'Package_TO_SOT_SMD:TDSON-8-1','Manufacturer':'Infineon','MPN':'BSC070N10NS5ATMA1','Datasheet':'https://www.infineon.com/part/BSC070N10NS5','Description':'100V ideal diode MOSFET','Selection_Status':'Selected: 100 V low-charge MOSFET. Source IDEAL_IN, drain VBAT_FUSED, gate IDEAL_GATE.'},[str(i) for i in range(1,9)])
label('IDEAL_IN',332.74,93.98,180);label('VBAT_FUSED',347.98,93.98);label('IDEAL_GATE',340.36,83.82)
# D4's bidirectional terminals use the existing TVS library definition.
d1=next(b for b in blocks(s,'symbol') if props(b).get('Reference')=='D1')
d4lib=re.search(r'\(lib_id "([^"]+)"',d1)[1]
d4fields={k:v for k,v in props(d1).items() if k!='Reference'}
d4fields['Selection_Status']='Selected: local bidirectional clamp from IDEAL_IN to U5 reference IDEAL_VSS.'
symbol('D4',d4lib,312.42,124.46,90,d4fields,['1','2'])
label('IDEAL_IN',312.42,120.65);label('IDEAL_VSS',312.42,128.27)
passive('R19','Device:R',355.6,124.46,res19,'IDEAL_VSS','GND')
passive('C11','Device:C',312.42,156.21,film,'VBAT_FUSED','IDEAL_VSS')
passive('C15','Device:C',355.6,156.21,film,'VBAT_FUSED','IDEAL_VSS')
passive('R20','Device:R',312.42,191.77,res20,'IDEAL_IN','INPUT_DAMP')
passive('C16','Device:C',355.6,191.77,film,'INPUT_DAMP','GND')
for ref,x,net in [('C12',50.8,'INA_IN_P'),('C13',101.6,'INA_IN_N'),('C14',152.4,'INA_VBUS')]:passive(ref,'Device:C',x,238.76,film,net,'GND')
passive('R21','Device:R',203.2,238.76,res21,'PDB_VOUT','INA_VBUS')
# Explicit power flags on the MOSFET-fed bus and floating controller reference.
for ref,x,net in [('#FLG0101',307.34,'VBAT_FUSED'),('#FLG0102',365.76,'IDEAL_VSS'),('#FLG0103',254.0,'PDB_VOUT')]:
 symbol(ref,'power:PWR_FLAG',x,213.36,0,{'Value':'PWR_FLAG'},['1'])
 label(net,x,213.36)
text('LOW-LOSS REVERSE INPUT PROTECTION',302.26,15.24,1.8)
text('SENSOR INPUT FILTERS',25.4,218.44,1.8)
text('C11-C16: 1 uF, 63 V, 5% film. C11 + C15 provide 2 uF.\nPlace C12/C13 and R8/R9 symmetrically at U2.\nR21/C14: allow 1 ms settling before valid VBUS readings.\nKeep U5, Q3, D4 and C11/C15 loops short; R20/C16 at the input.',25.4,266.7,1.27)
s=s.rstrip()[:-1]+'\n'+''.join(added)+')\n'
s=s.replace('A-P3-DRAFT: not released for fabrication.','A-P4-DRAFT: PCB and bench validation required.')
s=s.replace('Pin stress, SOA and source coordination open.','U5/Q3 block reverse current; D3 clamps output.')
s=s.replace('See Simulation/closure-20260915/STATUS.md.','See Simulation/closure-20260915/RELEASE.md.')
p.write_text(s)

# ST DPAK: both physical outer leads are anode; tab is cathode.
source=Path('C:/Program Files/KiCad/10.0/share/kicad/footprints/Package_TO_SOT_SMD.pretty/TO-252-3_TabPin2.kicad_mod').read_text()
source=source.replace('TO-252-3_TabPin2','STPST10H100SB_DPAK')
source=re.sub(r'\(pad "([123])"',lambda m:'(pad "'+{'1':'2','2':'1','3':'2'}[m[1]]+'"',source)
(R/'Libraries/PDB_Footprints.pretty/STPST10H100SB_DPAK.kicad_mod').write_text(source)
parts=[]
for b in blocks(s,'symbol'):
 fields=props(b)
 if fields['Reference'].startswith('#'):continue
 fields['DNP']='(dnp yes)' in b;parts.append(fields)
(H.parent/'combined-20260915/audit/components.json').write_text(json.dumps(parts,indent=2))
print('A-P4 schematic:',len(parts),'component symbols')
