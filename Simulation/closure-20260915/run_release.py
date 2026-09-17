"""Run the selected schematic population with explicit screening limits."""
from pathlib import Path
import re,json,time,sys,concurrent.futures
import develop_protection as d
S=d.S;H=d.H
checks_by_name={}
def prepare(kind):
 if kind in ('transients','transients_fine','filter_mismatch'):
  s=(S/'selected_transients.cir').read_text()
  if kind=='transients_fine':s=s.replace('.tran 0 600m 0 5u','.tran 0 600m 0 1u')
  if kind=='filter_mismatch':s=s.replace('PDB_CURRENT\n','PDB_CURRENT PARAMS: CFILM=1 CMISMATCH=1.1\n')
  checks={**d.v.PIN_STRESS,'q1_vds':(0,60),'q2_vds':(0,60),'vout_final':(16,16.8),'v3v3_max':(0,3.6)}
 else:
  s=(S/('final_'+kind+'.cir')).read_text()
  checks=dict(d.BASE_LIMITS('final_'+kind))
  s=s.replace('.inc pdb',r'.lib C:\Users\jared\AppData\Local\LTspice\lib\sub\LTC4359.sub'+'\n.inc pdb')
 s=s.replace('pdb_selected.lib','pdb_release.lib').replace('pdb_final.lib','pdb_release.lib').replace('models\\pdb_devices.lib','models\\pdb_screen17_devices.lib')
 extras={
 'INP_MIN':'MIN V(XPDB:INA_IN_P)','INN_MIN':'MIN V(XPDB:INA_IN_N)','VBUS_MIN':'MIN V(XPDB:INA_VBUS)',
 'INP_MAX':'MAX V(XPDB:INA_IN_P)','INN_MAX':'MAX V(XPDB:INA_IN_N)','VBUS_MAX':'MAX V(XPDB:INA_VBUS)',
 'Q3_VDS':'MAX ABS(V(XPDB:VBAT_FUSED,XPDB:IDEAL_IN))','Q3_VGS':'MAX ABS(V(XPDB:IDEAL_GATE,XPDB:IDEAL_IN))',
 'U5_IN_MIN':'MIN V(XPDB:IDEAL_IN,XPDB:IDEAL_VSS)','U5_IN_MAX':'MAX V(XPDB:IDEAL_IN,XPDB:IDEAL_VSS)',
 'U5_OUT_MIN':'MIN V(XPDB:VBAT_FUSED,XPDB:IDEAL_VSS)','U5_OUT_MAX':'MAX V(XPDB:VBAT_FUSED,XPDB:IDEAL_VSS)',
 'U5_GS_MIN':'MIN V(XPDB:IDEAL_GATE,XPDB:IDEAL_IN)', 'U5_GS_MAX':'MAX V(XPDB:IDEAL_GATE,XPDB:IDEAL_IN)',
 'C11_STRESS':'MAX ABS(V(XPDB:VBAT_FUSED,XPDB:IDEAL_VSS))','C16_STRESS':'MAX ABS(V(XPDB:INPUT_DAMP))',
 'INA_DIFF':'MAX ABS(V(XPDB:INA_IN_P,XPDB:INA_IN_N))'}
 for name,expr in extras.items():
  if not re.search(r'^\.meas TRAN '+name+r'\s',s,re.M|re.I):s=s.replace('.end',f'.meas TRAN {name} {expr}\n.end')
 checks.update({x:(-.3,85) for x in ('inp_min','inn_min','vbus_min','inp_max','inn_max','vbus_max')})
 checks.update(q3_vds=(0,100),q3_vgs=(0,20),u5_in_min=(-40,100),u5_in_max=(-40,100),u5_out_min=(-2,100),u5_out_max=(-2,100),u5_gs_min=(-.3,15),u5_gs_max=(-.3,15),c11_stress=(0,63),c16_stress=(0,63),ina_diff=(0,40))
 p=S/('release_'+kind+'.cir');p.write_text(d.save_measured(s));checks_by_name[p.stem]=checks;return p

def main():
 kinds=sys.argv[1:] or ['transients','corners','lowtrip','temperature','faults','faults_fine','reverse','reverse25','filter_mismatch','transients_fine']
 decks=[prepare(k) for k in kinds]
 d.v.limits=lambda name:checks_by_name[name]
 report={'timestamp':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'scope':'A-P4 selected circuit, screening only. No PCB or thermal qualification.','results':[],'sha256':{}}
 for p in decks:report['sha256'].update(d.hashes(p))
 out=H/'release-results.json'
 if out.exists():(H/('release-results-'+time.strftime('%Y%m%d-%H%M%S')+'.json')).write_bytes(out.read_bytes())
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  tasks={pool.submit(d.v.run,p,Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),600):p for p in decks}
  for future in concurrent.futures.as_completed(tasks):
   r=future.result();report['results'].append(r);out.write_text(json.dumps(report,indent=2));print(r['deck'],r['status'],r['seconds'],r['errors'],flush=True)
 return int(any(r['status']=='FAIL' for r in report['results']))

if __name__=='__main__':raise SystemExit(main())
