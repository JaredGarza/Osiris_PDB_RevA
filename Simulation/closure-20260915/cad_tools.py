from pathlib import Path
import re,json,uuid
H=Path(__file__).resolve().parent;R=H.parents[1]
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
def blocks(s,kind):
 return [block_at(s,m.start()+1) for m in re.finditer(r'^\t\('+kind+r'(?:\s|\n)',s,re.M)]
def props(b):return {a:json.loads('"'+v+'"') for a,v in re.findall(r'\(property "([^"]+)" "((?:\\.|[^"\\])*)"',b)}
def prop(b,k,v):
 pat=r'(\(property "'+re.escape(k)+r'" )"(?:\\.|[^"\\])*"'
 assert re.search(pat,b),(k,v)
 return re.sub(pat,lambda m:m[1]+json.dumps(v),b,count=1)
uid=lambda:str(uuid.uuid4())
if __name__=='__main__':
 s=(R/'Osiris_PDB_RevA.kicad_sch').read_text()
 for b in blocks(s,'symbol'):
  if props(b).get('Reference') in ('F1','U2','D3','Q1'):
   print(props(b)['Reference'],re.search(r'\(at ([^)]+)\)',b)[1],re.search(r'\(lib_id ([^)]+)\)',b)[1])
 for b in blocks(s,'label'):
  if any(x in b for x in ['VBAT_FUSED','PDB_VOUT']):print(b.splitlines()[:2])
