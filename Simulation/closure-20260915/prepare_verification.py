"""Build the explicit ECO test set; historical experiments remain unchanged."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'combined-20260915'
p=(root/'pdb/pdb_coordinated.lib').read_text()
p=p.replace('* Current KiCad population; see audit/current.net.xml and check_connectivity.py.',
 '* A-P3-DRAFT ECO: direct gate drive, series RC branch, standard 10 mOhm shunt.')
p=p.replace('RFUSE=17.75m','RFUSE=23.48m').replace('RSHUNT=8m','RSHUNT=10m')
p=p.replace('VGF GP GF 0','RGF GP GF 1m ; gate copper parasitic, not a fitted component')
p=p.replace('R17  SCL V3V3 4.7k','* R17 DNP; host owns pull-up.').replace('R18  SDA V3V3 4.7k','* R18 DNP; host owns pull-up.')
(root/'pdb/pdb_eco.lib').write_text(p)
o=(root/'osiris/osiris_reva.lib').read_text()
o=o.replace('SR21=28100 TD21=100u','SR21=610 TD21=2.35m')
o=o.replace('REFERENCE CAD AS-BUILT','REFERENCE CAD WITH PROPOSED DVDT ECO')
start=o.index('* THIS IS Rev A.')
end=o.index('* Connectivity traced',start)
o=o[:start]+'* ADDENDUM REQUIRED: 3.3 nF from pin 7 to GND at U21, U22 and U4.\n* See ../../closure-20260915/OSIRIS-ECO.md. Original Altium files unchanged.\n*\n'+o[end:]
o=o.replace('* No AP64501 SPICE model or datasheet exists in this tree. This is a',
 '* AP64501 switching/control-loop behavior is not represented. This is a')
start=o.index('* ** U21 DVDT')
end=o.index('\nR58 ',start)
o=o[:start]+'* ECO: 3.3 nF C0G at DVDT pin 7; 610 V/s and 2.35 ms typical at 12 V.\n* Sweep slew and delay separately; these are not guaranteed production bounds.\n'+o[end:]
(root/'osiris/osiris_eco.lib').write_text(o)
for source,name in [('coord12_corners','eco_corners'),('coord12_lowtrip','eco_lowtrip'),('coordinated_faults','eco_faults'),('current_reverse','eco_reverse')]:
 s=(root/(source+'.cir')).read_text()
 import re
 s=re.sub(r'\.inc pdb\\pdb_\w+\.lib',r'.inc pdb\\pdb_eco.lib',s)
 s=s.replace('osiris_reva.lib','osiris_eco.lib')
 s=s.replace('RSHUNT=12.12m','RSHUNT=10.1m').replace('RSHUNT=15.15m','RSHUNT=12.625m')
 s=s.replace('+ PARAMS: RHV_GP=20Meg\n','')
 s=s.replace('740m 9.0  750m 14.8','690m 9.0  700m 14.8').replace('TO 735m','TO 685m')
 s=s.replace('RSHUNT=10.1m CDERATE','RSHUNT=10.1m CDERATE')
 s=s.replace('* 60000 V/s is an assumed stress case, not a vendor maximum.',
 '* 300..2000 V/s is a sensitivity range, not a vendor guaranteed range.')
 s=s.replace('* Rev-B regression: everything that worked on the as-built board must still\n* work. Same timeline as combined_faults.cir so results are directly\n* comparable against the as-built numbers in FINDINGS.md.',
 '* A-P3-DRAFT combined fault screen; surrogate loads and power devices.')
 s=re.sub(r'^\* Startup -- compare.*$', '* Startup measurements',s,flags=re.M)
 if name=='eco_reverse':s=s.replace('list -14.8 -16.8 -25.0','list -14.8 -16.8')
 (root/(name+'.cir')).write_text(s)
s=(root/'eco_corners.cir').read_text().replace('SR21={table(CASE,1,300,2,300,3,610,4,610,5,1200,6,1200,7,2000,8,2000)}',
 'SR21=2000 TD21={table(CASE,1,100u,2,100u,3,1m,4,1m,5,2.35m,6,2.35m,7,5m,8,5m)}')
(root/'eco_delay.cir').write_text(s)
s=(root/'eco_faults.cir').read_text().replace('.tran 0 3.0 0 20u','.tran 0 3.0 0 1u')
(root/'eco_faults_fine.cir').write_text(s)
s=(root/'verify_all.py').read_text()
s=s.replace("'coord12_lowtrip'):","'coord12_lowtrip', 'eco_corners', 'eco_lowtrip', 'eco_delay'):")
s=s.replace("'coordinated_faults'):","'coordinated_faults', 'eco_faults', 'eco_faults_fine'):")
s=s.replace("'eco_faults'):","'eco_faults', 'eco_faults_fine'):")
s=s.replace("'closure_reverse'):","'closure_reverse', 'eco_reverse'):")
(root/'verify_all.py').write_text(s)
print('Prepared explicit ECO model and five screening decks.')
