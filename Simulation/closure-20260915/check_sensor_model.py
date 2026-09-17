"""Validate active-mode INA228 analog surrogate against its declared DC model."""
from pathlib import Path
import json
import develop_protection as d

def main():
 p=d.S/'screen17_sensor_dc.cir'
 d.v.limits=lambda name:dict(bias=(2.49e-9,2.60e-9),diff_error=(0,1e-10),bus_error=(0,1e-10),iq=(599e-6,601e-6))
 r=d.v.run(p,Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),30)
 r['sha256']=d.hashes(p)
 r['scope']='Active-mode analog surrogate only; 1 Tohm numerical shunts add up to 85 pA at 85 V.'
 (d.H/'screen17-sensor-dc.json').write_text(json.dumps(r,indent=2))
 print(r['status'],r['errors'])
 return int(r['status']=='FAIL')

if __name__=='__main__':raise SystemExit(main())
