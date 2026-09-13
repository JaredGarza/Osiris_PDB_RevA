from pathlib import Path
import re, uuid, shutil, json

root=Path(__file__).resolve().parents[1]
sch=root/'Osiris_PDB_RevA.kicad_sch'
lib=root/'Libraries/PDB_Symbols.kicad_sym'
assert not (root/'~Osiris_PDB_RevA.kicad_sch.lck').exists(), 'Close schematic editor first'
s=sch.read_text(encoding='utf-8'); old=s
l=lib.read_text(encoding='utf-8')
backup=root/'fuse-connector-backup-20260910'
assert not backup.exists(), 'Review existing backup before repeating'
backup.mkdir()
for path in [sch,lib,root/'BOM.csv']:
 shutil.copy2(path,backup/path.name)
pattern=re.compile(r'^\t\(symbol\n.*?^\t\)',re.M|re.S)
def quote(t): return '"'+t.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')+'"'
def prop(b,k,v):
 p=r'(\(property "'+re.escape(k)+r'" )"(?:\\.|[^"\\])*"'
 if re.search(p,b): return re.sub(p,lambda m:m[1]+quote(v),b,count=1)
 at=re.search(r'\(at ([\d.-]+) ([\d.-]+)',b)
 new=f'\n\t\t(property {quote(k)} {quote(v)} (at {at[1]} {at[2]} 0) (effects (font (size 1.27 1.27)) (hide yes)))'
 return b[:-3]+new+'\n\t)'
def ds(local,online):
 return '${KIPRJMOD}/Datasheets/'+local if (root/'Datasheets'/local).exists() else online
fpJ3='Connector_AMASS:AMASS_XT60PW-F_1x02_P7.20mm_Horizontal'
custom=re.search(r'\t\t\(symbol "Connector_Generic:Conn_01x02"\n.*?\n\t\t\)',s,re.S)[0]
custom=custom.replace('Connector_Generic:Conn_01x02','PDB_Symbols:XT60PW_F').replace('Conn_01x02','XT60PW_F')
custom=re.sub(r'\(number "([12])"',lambda m:'(number "'+('2' if m[1]=='1' else '1')+'"',custom)
custom=custom.replace('(name "Pin_1"','(name "+"').replace('(name "Pin_2"','(name "-"')
custom=prop(custom,'Footprint',fpJ3)
custom=prop(custom,'Description','AMASS XT60PW-F: pin 1 negative/GND; pin 2 positive; symbol upper contact is pin 2')
custom=prop(custom,'Datasheet',ds('AMASS_XT60PW-F.pdf','https://www.tme.eu/Document/1191bc2fa3aee3c446e5a895fd8f7983/XT60PW-F.pdf'))
assert 'PDB_Symbols:XT60PW_F' not in s
s=s.replace('\n\t(lib_symbols\n','\n\t(lib_symbols\n'+custom+'\n',1)
library_symbol='\n'.join(line[1:] if line.startswith('\t') else line for line in custom.splitlines()).replace('PDB_Symbols:XT60PW_F','XT60PW_F')
l=l.rstrip()[:-1]+library_symbol+'\n)\n'
updates={
 'F1':{'Value':'5A MINI','Manufacturer':'Littelfuse','MPN':'0297005.WXNV','Footprint':'Fuse:Fuseholder_Blade_Mini_Keystone_3568','Description':'5 A, 32 VDC MINI blade fuse; provisional rating','Holder_Manufacturer':'Keystone Electronics','Holder_MPN':'3568','Holder_Datasheet':ds('Keystone_3568.pdf','https://www.keyelco.com/product.cfm/product_id/306'),'Datasheet':ds('Littelfuse_MINI_0297_selection_guide.pdf','https://www.littelfuse.com/assetdocs/fuse-selection-guide?assetguid=1d99e3a6-f314-48d7-b124-9d5d56955f09'),'Selection_Status':'PROVISIONAL 5 A: validate input current, inrush, temperature, breaking capacity and protection coordination'},
 'J1':{'Value':'XT60PW-M','Manufacturer':'AMASS','MPN':'XT60PW-M','Footprint':'Connector_AMASS:AMASS_XT60PW-M_1x02_P7.20mm_Horizontal','Description':'Battery input; PCB right-angle XT60; pin 1 GND, pin 2 VBAT_RAW','Datasheet':ds('AMASS_XT60PW-M.pdf','https://www.tme.eu/Document/b13629717d44ae038681dba08d18c0b6/XT60PW-M.pdf'),'Selection_Status':'Assigned; verify cable mating, polarity and board-edge clearance'},
 'J2':{'Manufacturer':'JST','MPN':'BM06B-GHS-TBT(LF)(SN)','Footprint':'Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical','Description':'JST GH 6-way control; 1 GND, 2 SDA, 3 SCL, 4 INA_ALERT_N, 5 PDB_FAULT_N, 6 NC','Datasheet':ds('JST_GH.pdf','https://www.jst-mfg.com/product/pdf/eng/eGH.pdf'),'Mating_Housing':'GHR-06V-S','Mating_Contact':'SSHL-002T-P0.2','Selection_Status':'Assigned; Osiris I2C/GPIO endpoints and custom cable mapping still require verification'},
 'J3':{'Manufacturer':'AMASS','MPN':'XT60PW-F','Footprint':fpJ3,'Description':'Protected power output; pin 1 GND, pin 2 PDB_VOUT; cable to Osiris J16 VBATT_IN','Datasheet':ds('AMASS_XT60PW-F.pdf','https://www.tme.eu/Document/1191bc2fa3aee3c446e5a895fd8f7983/XT60PW-F.pdf'),'Selection_Status':'Assigned with dedicated symbol pin mapping; verify physical cable polarity and board-edge clearance'},
 'U1':{'Manufacturer':'Analog Devices','MPN':'LTC4368IMS-1#PBF','Datasheet':'${KIPRJMOD}/Datasheets/LTC4368 (Rev C).pdf'},
 'U2':{'Manufacturer':'Texas Instruments','MPN':'INA228AIDGSR','Datasheet':ds('INA228.pdf','https://www.ti.com/lit/ds/symlink/ina228.pdf')},
 'U3':{'Manufacturer':'Texas Instruments','MPN':'TPS7A1633DGNR','Datasheet':ds('TPS7A16.pdf','https://www.ti.com/lit/ds/symlink/tps7a16.pdf')},
 'U4':{'Manufacturer':'Nexperia','MPN':'74AUP1G07GW,125','Datasheet':ds('Nexperia_74AUP1G07.pdf','https://assets.nexperia.com/documents/data-sheet/74AUP1G07.pdf')},
 'R5':{'Manufacturer':'Ohmite','MPN':'FC4L64R005FER','Datasheet':ds('Ohmite_FC4L.pdf','https://www.ohmite.com/res-fc4l/')},
}
for ref in ['Q1','Q2']: updates[ref]={'Manufacturer':'Infineon','MPN':'ISC015N06NM5LF2'}
for m in pattern.finditer(s):
 b=m[0]; ref=re.search(r'\(property "Reference" "([^"]+)"',b)[1]
 if ref.startswith('C'):
  mpn=re.search(r'\(property "MPN" "([^"]+)"',b)
  if mpn:
   name=('KEMET_' if mpn[1].startswith('C0603') else 'TDK_')+mpn[1]+'.pdf'
   if (root/'Datasheets'/name).exists(): updates[ref]={'Datasheet':'${KIPRJMOD}/Datasheets/'+name}
def edit(m):
 b=m[0]; ref=re.search(r'\(property "Reference" "([^"]+)"',b)[1]
 if ref=='J3':
  b=b.replace('(lib_id "Connector_Generic:Conn_01x02")','(lib_id "PDB_Symbols:XT60PW_F")')
  b=re.sub(r'\(pin "([12])"',lambda m:'(pin "'+('2' if m[1]=='1' else '1')+'"',b)
 for k,v in updates.get(ref,{}).items(): b=prop(b,k,v)
 return b
s=pattern.sub(edit,s)
note='F1: 5 A provisional; Keystone 3568 holder.\nValidate load, inrush and fuse coordination.\nJ3: XT60PW-F; 1=GND, 2=VOUT.\nCable to Osiris J16 (VBATT_IN); verify polarity.\nJ2 requires a custom cable; pin 6 is NC.'
s=s.rstrip()[:-1]+f'\n\t(text {quote(note)} (at 202 126 0) (effects (font (size 1 1)) (justify left top)) (uuid "{uuid.uuid4()}"))\n)\n'
# All existing wires, labels, junctions and existing symbol locations are preserved.
for tag in ['wire','label','junction','no_connect']:
 pat=re.compile(r'^\t\('+tag+r'\b.*?^\t\)',re.M|re.S)
 assert pat.findall(old)==pat.findall(s),tag
for ref in ['R1','R2','R3','R6','R7']:
 find=lambda t:next(m[0] for m in pattern.finditer(t) if '(property "Reference" "'+ref+'"' in m[0])
 assert find(old)==find(s),ref
for m in pattern.finditer(s):
 b=m[0];ref=re.search(r'\(property "Reference" "([^"]+)"',b)[1]
 if ref.startswith('#'):continue
 fp=re.search(r'\(property "Footprint" "([^"]*)"',b)[1]
 assert fp,ref
 libname,fn=fp.split(':',1)
 base=root/'Libraries'/f'{libname}.pretty' if libname=='PDB_Footprints' else Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')/f'{libname}.pretty'
 assert (base/(fn+'.kicad_mod')).exists(),fp
lib.write_text(l,encoding='utf-8',newline='\n')
sch.write_text(s,encoding='utf-8',newline='\n')
print('Applied connector/fuse fields, J3 symbol, local datasheet links, and manufacturing note.')
print('All 33 board symbols have footprints. Threshold resistors and wires unchanged.')
