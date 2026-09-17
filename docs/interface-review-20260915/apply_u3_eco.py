"""One-time U3 ECO: LT3010 plus feedback divider and compensation capacitor.
Backs up source first. The electrical review still has other open release gates.
"""
from pathlib import Path
import csv,io,re,shutil,uuid
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
assert not list(ROOT.glob('*.lck')), 'Close KiCad first'
backup=HERE/'before-u3-eco'
assert not backup.exists(), 'Already applied'
backup.mkdir()
for n in ['Osiris_PDB_RevA.kicad_sch','BOM.csv','BOM_purchasing.csv','Libraries/PDB_Symbols.kicad_sym']:
    dst=backup/n; dst.parent.mkdir(exist_ok=True,parents=True); shutil.copy2(ROOT/n,dst)
sch=ROOT/'Osiris_PDB_RevA.kicad_sch'
s=sch.read_text(encoding='utf-8')
libpath=ROOT/'Libraries/PDB_Symbols.kicad_sym'
lib=libpath.read_text(encoding='utf-8')
NS=uuid.UUID('e46f4f8e-bc3c-4af5-8d59-fd3e9a326978')
uid=lambda key:str(uuid.uuid5(NS,key))
quote=lambda text:'"'+text.replace('\\','\\\\').replace('"','\\"')+'"'
def block_at(text,start):
    i=start; depth=0
    while i<len(text):
        if text[i]=='"':
            i+=1
            while text[i]!='"': i+=2 if text[i]=='\\' else 1
        elif text[i]=='(': depth+=1
        elif text[i]==')':
            depth-=1
            if depth==0:return text[start:i+1]
        i+=1
    raise ValueError('Unbalanced source')
def prop(block,key,val):
    pat=r'(\(property '+re.escape(quote(key))+r' )"(?:\\.|[^"\\])*"'
    assert re.search(pat,block),key
    return re.sub(pat,lambda m:m[1]+quote(val),block,count=1)
oldname='TPS7A1633DGNR'; newname='LT3010EMS8E'
fp='Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm'
url='https://www.analog.com/media/en/technical-documentation/data-sheets/lt3010-3010-5.pdf'
status='A-P2 engineering draft: reverse-input/current-protected LT3010; R11/R12/C10 set nominal 3.29 V. Verify startup, effective C6 and assembled rail transients.'
old=block_at(lib,lib.index('(symbol "'+oldname+'"'))
new=old.replace(oldname,newname)
for key,val in {'Footprint':fp,'Datasheet':url,'Description':'50 mA adjustable LDO with reverse-input and reverse-current protection','Manufacturer':'Analog Devices','MPN':'LT3010EMS8E#TRPBF'}.items():
    if re.search(r'\(property '+re.escape(quote(key))+r' ',new):new=prop(new,key,val)
# Preserve the drawing's pin positions but replace the electrical definitions.
for number,name,kind in [(2,'ADJ','input'),(3,'NC','no_connect'),(5,'SHDN','input'),(6,'NC','no_connect'),(7,'NC','no_connect')]:
    pins=[block_at(new,m.start()) for m in re.finditer(r'\(pin \w+ line',new)]
    found=[p for p in pins if re.search(r'\(number "'+str(number)+r'"',p)]
    assert len(found)==1
    p=found[0]
    q=re.sub(r'^\(pin \w+ line',f'(pin {kind} line',p)
    q=re.sub(r'\(name "[^"]+"',f'(name "{name}"',q,count=1)
    new=new.replace(p,q,1)
# Do not retain the previous package's filter in the new symbol.
new=re.sub(r'(\(property "ki_fp_filters" )"[^"]*"',r'\1"MSOP*3x3mm*P0.65mm*"',new)
lib=lib.rstrip()[:-1]+'\n\t'+new+'\n)\n'
libpath.write_bytes(lib.replace('\n','\r\n').encode('utf-8'))
cached=new.replace('(symbol "'+newname+'"','(symbol "PDB_Symbols:'+newname+'"',1)
cached='\t\t'+cached.replace('\n','\n\t')+'\n'
s=s.replace('\t(lib_symbols\n','\t(lib_symbols\n'+cached,1)
inst=re.search(r'^\t\(symbol\n.*?\(property "Reference" "U3".*?^\t\)',s,re.M|re.S)
# Match instances independently to avoid crossing from a preceding component.
matches=[m for m in re.finditer(r'^\t\(symbol\n.*?^\t\)',s,re.M|re.S) if '(property "Reference" "U3"' in m[0]]
assert len(matches)==1
block=matches[0][0]
repl=block.replace('PDB_Symbols:'+oldname,'PDB_Symbols:'+newname,1)
for key,val in {'Value':newname,'Footprint':fp,'Datasheet':url,'Description':'Reverse-protected local 3.3 V supply','Manufacturer':'Analog Devices','MPN':'LT3010EMS8E#TRPBF','Selection_Status':status}.items(): repl=prop(repl,key,val)
s=s.replace(block,repl,1)
ncs=[m for m in re.finditer(r'^\t\(no_connect\n.*?^\t\)\n',s,re.M|re.S) if '(at 81.28 153.67)' in m[0]]
assert len(ncs)==1
s=s.replace(ncs[0][0],'',1)

def label(name,x,y,key):
    return f'\t(label {quote(name)} (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid(key)}"))\n'
def wire(x1,y1,x2,y2,key):
    return f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid(key)}"))\n'
def junction(x,y,key):
    return f'\t(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid(key)}"))\n'
def passive(ref,value,libid,x,y,footprint,manufacturer,mpn,description,datasheet):
    props={'Reference':ref,'Value':value,'Footprint':footprint,'Datasheet':datasheet,'Description':description,'Manufacturer':manufacturer,'MPN':mpn,'Selection_Status':'A-P2 U3 feedback network; layout and assembled transient verification required.'}
    out=f'\t(symbol (lib_id "{libid}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid "{uid(ref)}")\n'
    for key,val in props.items():
        visible=key in ('Reference','Value')
        px=x+3.81 if visible else x
        py=y+(-1.27 if key=='Reference' else 1.27) if visible else y
        out+=f'\t\t(property {quote(key)} {quote(val)} (at {px:.2f} {py:.2f} 0) '+('' if visible else '(hide yes) ')+ '(effects (font (size 1.27 1.27))'+(' (justify left)' if visible else '')+'))\n'
    for pin in ('1','2'):out+=f'\t\t(pin "{pin}" (uuid "{uid(ref+pin)}"))\n'
    out+=f'\t\t(instances (project "Osiris_PDB_RevA" (path "/6f58a31e-2d20-46d6-8900-dedce2deebb4" (reference "{ref}") (unit 1))))\n\t)\n'
    return out,props
newrows={}
added=label('PDB_LDO_ADJ',81.28,153.67,'adjpin')
for ref,value,libid,x,y,footprint,mfr,mpn,desc,ds in [
 ('R11','1k58','Device:R',121.92,163.83,'Resistor_SMD:R_0805_2012Metric','YAGEO','RC0805FR-071K58L','1% 0.125W; upper feedback resistor','https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-071K58L'),
 ('R12','1k0','Device:R',121.92,179.07,'Resistor_SMD:R_0805_2012Metric','YAGEO','RC0805FR-071KL','1% 0.125W; lower feedback resistor','https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-071KL'),
 ('C10','100n','Device:C',139.7,163.83,'Capacitor_SMD:C_0603_1608Metric','KEMET','C0603C104K4RACTU','16V X7R; LT3010 feedback compensation','${KIPRJMOD}/Datasheets/KEMET_C0603C104K4RACTU.pdf')]:
    node,props=passive(ref,value,libid,x,y,footprint,mfr,mpn,desc,ds)
    added+=node;newrows[ref]=props
added+=wire(121.92,160.02,139.7,160.02,'top')
added+=label('PDB_3V3',121.92,160.02,'vcc')
added+=wire(121.92,167.64,121.92,170.18,'fb1')
added+=wire(121.92,170.18,121.92,175.26,'fb2')
added+=wire(139.7,167.64,139.7,170.18,'fb3')
added+=wire(139.7,170.18,121.92,170.18,'fb4')
added+=junction(121.92,170.18,'jfb')
added+=label('PDB_LDO_ADJ',121.92,170.18,'fblabel')
added+=label('GND',121.92,182.88,'gnd')
s=s.rstrip()[:-1]+added+')\n'
s=s.replace('(title "Osiris PDB - procurement baseline")','(title "Osiris PDB - engineering draft")',1)
s=s.replace('(date "2026-09-14")','(date "2026-09-15")',1).replace('(rev "A-P1")','(rev "A-P2-DRAFT")',1)
sch.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
for name in ('BOM.csv','BOM_purchasing.csv'):
    path=ROOT/name
    raw=path.read_bytes(); prefix=b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    lines=raw.decode('utf-8-sig').splitlines(keepends=True); header=next(csv.reader([lines[0]])); out=[lines[0]]
    def rowline(row):
        buf=io.StringIO(newline='');csv.writer(buf,lineterminator='\r\n').writerow([row.get(k,'') for k in header]);return buf.getvalue()
    for line in lines[1:]:
        row=dict(zip(header,next(csv.reader([line]))))
        if row['Reference']=='U3':
            row.update(Value=newname,Footprint=fp,Datasheet=url,Manufacturer='Analog Devices',MPN='LT3010EMS8E#TRPBF',Specification='50mA adjustable LDO; reverse-input/current protection')
            row['Selection Status']=status;out.append(rowline(row))
        else:out.append(line)
    for ref,p in newrows.items():
        row={k:p.get(k,'') for k in header};row['Specification']=p['Description'];row['Selection Status']=p['Selection_Status'];row['Quantity']='1';row['BOM Role']='Schematic component';out.append(rowline(row))
    path.write_bytes(prefix+''.join(out).encode('utf-8'))
print('Applied U3 LT3010 ECO with R11/R12/C10; revision A-P2-DRAFT.')
