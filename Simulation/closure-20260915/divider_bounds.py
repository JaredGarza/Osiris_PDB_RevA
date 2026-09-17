"""Algebraic divider corners supplement the nominal encrypted SPICE controller."""
from pathlib import Path
import itertools,json
H=Path(__file__).resolve().parent
# 1% + 0.8% engineering temperature allowance; 5% + 0.8% for R14.
# 0.8% bounds 200 ppm/C over 40 C from the reference temperature.
uv_on=[];uv_off=[];ov=[]
for r1,r2,r14,leak in itertools.product([237e3*.982,237e3*1.018],[11.8e3*.982,11.8e3*1.018],[22e6*.942,22e6*1.058],[-10e-9,10e-9]):
 conductance=1/r1+1/r2+1/r14
 for threshold,g_off in itertools.product([.4925+.020,.5075+.032],[-1,0]):
  uv_on.append(r1*(threshold*conductance-g_off/r14+leak))
 for threshold,boost in itertools.product([.4925,.5075],[7,13.1]):
  uv_off.append((threshold*conductance-boost/r14+leak)/(1/r1+1/r14))
for rt,rb,threshold,leak in itertools.product([2e6*.982,2e6*1.018],[54.9e3*.982,54.9e3*1.018],[.4925,.5075],[-10e-9,10e-9]):
 ov.append(threshold*(1+rt/rb)+leak*rt)
r1,r2,r14=237e3,11.8e3,22e6
nom_on=.525*(1+r1/r2+r1/r14)
nom_off=(.5*(1+r1/r2+r1/r14)-11*r1/r14)/(1+r1/r14)
out={'uv_on_cold_v':[min(uv_on),max(uv_on)],'uv_off_conditional_v':[min(uv_off),max(uv_off)],'ov_trip_v':[min(ov),max(ov)],'nominal_uv_on_v':nom_on,'nominal_uv_off_v_assuming_11v_gate_boost':nom_off,'cold_start_margin_at_12v':12-max(uv_on),'normal_current_trip_a':[.040/.00505,.060/.00495],'zero_output_min_trip_a':.030/.00505,'nominal_shunt_loss_2p5a_w':2.5**2*.005,'shunt_cal_50ua_lsb':round(13107.2e6*50e-6*.005),'assumptions':['Cold gate -1..0 V is an explicit boundary assumption, not a guaranteed encrypted-model parameter.','UV off assumes gate boost 7..13.1 V; load-dependent gate drive is not guaranteed by this calculation.','Temperature allowance is a conservative independent resistor sensitivity, not a supplier batch correlation.','Leakage +/-10 nA, UV/OV reference .4925..5075 V, UV hysteresis20..32 mV from LTC4368 datasheet.','UV thresholds are system cutoffs, not cell-level battery protection.']}
assert out['cold_start_margin_at_12v']>0.1
(H/'divider-bounds.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
