"""Read saved LTspice real waveforms, including incomplete runs for diagnosis only."""
from pathlib import Path
import struct,re,json,sys
p=Path(sys.argv[1]);b=p.read_bytes();head=b[:40000].decode('utf-16-le',errors='ignore').split('Binary:')[0]
assert 'Flags: real' in head and 'fastaccess' not in head.lower()
n=int(re.search(r'No. Variables:\s*(\d+)',head)[1])
names=re.findall(r'^\s*\d+\s+(\S+)\s+\S+',head,re.M)
i=b.find('Binary:'.encode('utf-16-le'));assert i>=0
start=b.find(b'\n\x00',i)+2;size=8+4*(n-1)
count=(len(b)-start)//size
mins=[float('inf')]*n;maxs=[-float('inf')]*n
for vals in struct.iter_unpack('<d'+'f'*(n-1),b[start:start+count*size]):
 for j,v in enumerate(vals):mins[j]=min(mins[j],v);maxs[j]=max(maxs[j],v)
print(json.dumps({'file':str(p),'records':count,'range':{name:[mins[i],maxs[i]] for i,name in enumerate(names)}},indent=2))
