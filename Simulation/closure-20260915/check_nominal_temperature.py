"""Check the planned 7 W load, without the extra 50% Jetson overload, at 0/60 C."""
from pathlib import Path
import json
import develop_protection as d

def main():
 s=(d.S/'screen17_nominal.cir').read_text().replace('.step param CASE list 1 2 3 4 5 6 7 8','.step param CASE list 1 2 3 4 5 6 7 8\n.step temp list 0 60')
 p=d.S/'screen17_nominal_temperature.cir';p.write_text(s)
 d.v.limits=lambda name:d.limits('screen17_nominal')
 r=d.v.run(p,Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 (d.H/'screen17-nominal-temperature.json').write_text(json.dumps({'result':r,'sha256':d.hashes(p),'scope':'Model temperature sweep; not self-heating or process qualification.'},indent=2))
 print(r['status'],r['seconds'],r['errors'],flush=True)
 return int(r['status']=='FAIL')

if __name__=='__main__':raise SystemExit(main())
