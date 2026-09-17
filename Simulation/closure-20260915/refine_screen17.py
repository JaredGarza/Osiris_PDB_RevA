"""Independent finer-time-step reversal check and LTC4368 divider-pin stress."""
from pathlib import Path
import json
import develop_protection as d

def main():
 s=(d.S/'screen17_transients.cir').read_text().replace('.tran 0 600m 0 5u','.tran 0 600m 0 1u')
 s=s.replace('.end','''.meas TRAN UV_MAX MAX V(XPDB:N_UV)
.meas TRAN SHDN_MAX MAX V(XPDB:SHDN_LTC)
.meas TRAN UV_NEG_CURRENT MAX if(V(XPDB:N_UV)<-.3,abs(V(XPDB:VBAT_FUSED,XPDB:N_UV)/226k+V(GP,XPDB:N_UV)/22Meg-V(XPDB:N_UV)/11.8k),0)
.meas TRAN OV_NEG_CURRENT MAX if(V(XPDB:N_OV)<-.3,abs(V(XPDB:VBAT_FUSED,XPDB:N_OV)/2Meg-V(XPDB:N_OV)/54.9k),0)
.meas TRAN SHDN_NEG_CURRENT MAX if(V(XPDB:SHDN_LTC)<-.3,abs(V(XPDB:VBAT_FUSED,XPDB:SHDN_LTC)/680k-V(XPDB:SHDN_LTC)/200k),0)
.end''')
 p=d.S/'screen17_transients_fine.cir';p.write_text(d.save_measured(s))
 checks={**d.PIN_LIMITS,'uv_max':(-40,80),'u1_ov_max':(-40,20),'shdn_max':(-40,80),
         'uv_neg_current':(0,.001),'ov_neg_current':(0,.001),'shdn_neg_current':(0,.001)}
 d.v.limits=lambda name:checks
 r=d.v.run(p,Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 report={'result':r,'sha256':d.hashes(p),'scope':'Screening only; resistor KCL checks apply to this candidate topology.'}
 coarse=json.loads((d.H/'screen17-results.json').read_text())
 base=next(x for x in coarse['results'] if x['deck']=='screen17_transients.cir')
 report['time_step_comparison']={}
 for name in ('u1_vin_min','q1_vds','q2_vds','d4_reverse','d4_energy','damp_energy'):
  a=base['measurements'].get(name,[]);b=r['measurements'].get(name,[])
  if len(a)==len(b) and a:
   report['time_step_comparison'][name]={'coarse':a,'fine':b,'maximum_relative_change':max(abs(x-y)/max(abs(x),1e-12) for x,y in zip(a,b))}
 (d.H/'screen17-fine.json').write_text(json.dumps(report,indent=2))
 print(r['status'],r['seconds'],r['errors'],report['time_step_comparison'],flush=True)
 return int(r['status']=='FAIL')

if __name__=='__main__':raise SystemExit(main())
