from cad_tools import *
p=R/'Osiris_PDB_RevA.kicad_sch';s=p.read_text()
for b in blocks(s,'symbol'):
 ref=props(b)['Reference'];q=b
 if ref in ('Q3','D4'):
  for key in ('Reference','Value'):
   start=q.index('(property "'+key+'"');old=block_at(q,start)
   new=re.sub(r'(\(at [\d.-]+ [\d.-]+) 0\)',r'\1 90)',old,count=1)
   if ref=='Q3':
    y=74.93 if key=='Reference' else 77.47
    new=re.sub(r'\(at [^)]+\)',f'(at 342.9 {y} 90)',new,count=1)
   q=q.replace(old,new,1)
 if ref.startswith('#FLG01'):
  x,y=map(float,re.search(r'\(at ([\d.-]+) ([\d.-]+)',q).groups())
  for key in ('Reference','Value'):
   start=q.index('(property "'+key+'"');old=block_at(q,start);new=old
   if key=='Reference':new=new.replace('(effects','(hide yes) (effects',1)
   else:new=re.sub(r'\(at [^)]+\)',f'(at {x} {y-2.54:.2f} 0)',new,count=1)
   q=q.replace(old,new,1)
 if q!=b:s=s.replace(b,q,1)
p.write_text(s)
