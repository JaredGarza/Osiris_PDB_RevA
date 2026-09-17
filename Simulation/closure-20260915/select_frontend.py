from pathlib import Path
import json,sys
import develop_protection as d
import build_hv_lib as hv

H=d.H;S=d.S
s=(S/'pdb/pdb_ideal.lib').read_text()
s=s.replace('MQ3 VBAT_FUSED IDEAL_GATE IDEAL_IN IDEAL_IN ISC015N06NM5LF2','MQ3 VBAT_FUSED IDEAL_GATE IDEAL_IN IDEAL_IN BSC070N10NS5')
s=s.replace('IDEAL_IN IDEAL_SHDN IDEAL_VSS LTC4359','IDEAL_IN IDEAL_IN IDEAL_VSS LTC4359')
s=s.replace('XU2  INA_IN_P INA_IN_N VOUT','XU2  INA_IN_P INA_IN_N INA_VBUS')
s=s.replace('D3   GND VOUT MBR0540','D3 GND VOUT STPST10H100_SCREEN')
s=s.replace('.ends PDB_CURRENT','''C12 INA_IN_P GND 1u Rser=30m
C13 INA_IN_N GND 1u Rser=30m
R21 VOUT INA_VBUS 100
C14 INA_VBUS GND 100n Rser=30m
.ends PDB_CURRENT''')
s+=hv.FET_MODEL+hv.DIODE_MODEL
(S/'pdb/pdb_selected.lib').write_text(s)
results=[]
for kind in sys.argv[1:] or ['transients','corners']:
 src='hvd_transients' if kind=='transients' else 'final_'+kind
 t=(S/(src+'.cir')).read_text().replace('pdb_hvd.lib','pdb_selected.lib').replace('pdb_final.lib','pdb_selected.lib')
 t=t.replace('models\\pdb_devices.lib','models\\pdb_screen17_devices.lib')
 t=t.replace('.inc pdb',r'.lib C:\Users\jared\AppData\Local\LTspice\lib\sub\LTC4359.sub'+'\n.inc pdb')
 import re
 t=re.sub(r'^\.meas TRAN TVS_.*\n','',t,flags=re.M)
 t=t.replace('.end','''.meas TRAN Q3_VDS MAX ABS(V(XPDB:VBAT_FUSED,XPDB:IDEAL_IN))
.meas TRAN Q3_VGS MAX ABS(V(XPDB:IDEAL_GATE,XPDB:IDEAL_IN))
.meas TRAN U5_IN_MIN MIN V(XPDB:IDEAL_IN,XPDB:IDEAL_VSS)
.meas TRAN U5_IN_MAX MAX V(XPDB:IDEAL_IN,XPDB:IDEAL_VSS)
.meas TRAN U5_OUT_MIN MIN V(XPDB:VBAT_FUSED,XPDB:IDEAL_VSS)
.meas TRAN U5_OUT_MAX MAX V(XPDB:VBAT_FUSED,XPDB:IDEAL_VSS)
.end''')
 p=S/('selected_'+kind+'.cir');p.write_text(d.save_measured(t))
 checks=dict(d.v.PIN_STRESS if kind=='transients' else d.BASE_LIMITS('final_'+kind))
 if kind=='transients':checks.update(q1_vds=(0,60),q2_vds=(0,60),vout_final=(16,16.8),v3v3_max=(0,3.6))
 checks.update(q3_vds=(0,100),q3_vgs=(0,20),u5_in_min=(-40,100),u5_in_max=(-40,100),u5_out_min=(-2,100),u5_out_max=(-2,100))
 d.v.limits=lambda name:checks
 r=d.v.run(p,Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 results.append(r);print(kind,r['status'],r['errors'],flush=True)
 (H/'selected-frontend.json').write_text(json.dumps(results,indent=2))
