from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
backup = root / 'audit' / 'original-files'
files = list(root.glob('*.cir')) + list(root.glob('*/*.lib')) + list(root.glob('*/*.cir'))
files += [root / 'verify_all.sh', root / 'model_manifest.json', root / 'README.md', root / 'FINDINGS.md', root / 'REVB-PROPOSAL.md']
for p in files:
    if 'audit' in p.relative_to(root).parts:
        continue
    out = backup / p.relative_to(root)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        shutil.copy2(p, out)

p = root / 'models/pdb_devices.lib'
s = p.read_text().replace('IQ   VS  GND  600u', 'BIQ  VS GND I=600u*limit(V(VS,GND)/2.7,0,1)')
s = s.replace('IQ   VCC GND 1u', 'BIQ  VCC GND I=1u*limit(V(VCC,GND)/0.8,0,1)')
s = s.replace('\n.end\n', '\n')
p.write_text(s)

p = root / 'pdb/pdb_ap2.lib'
s = p.read_text().replace('RJ1N GNDJ1 GND      {RXT60}\nVGJ1 GNDJ1 GND      0', '* Return/contact resistance is included in the top-level loop resistance.')
s = s.replace('VADJ ~ 1.240 V', 'VADJ = 1.275 V nominal').replace('1.240 * (1 + 1580/1000) = 3.199 V   <-- NOT 3.30 V, see notes', '1.275 * (1 + 1580/1000) = 3.2895 V nominal (before ADJ bias)')
p.write_text(s)

p = root / 'osiris/osiris_reva.lib'
s = p.read_text()
s = s.replace('TSS=2m', 'TSS=18.868m')
s = s.replace('BIN   IN GND I=V(IDEL) + {IQ}', 'BIN   IN GND I=V(IDEL) + {IQ}*limit(V(IN,GND)/2.0,0,1)')
s = s.replace('BOUT  0 OUT I=V(IDEL)', 'BOUT  GND OUT I=V(IDEL)')
s = s.replace('V=limit( (V(SS)-V(OUT))*1000 , 0 , {ILIM} )', 'V=V(GO)*limit( (min(V(SS),max(V(IN,GND)-0.1,0))-V(OUT,GND))*1000 , 0 , {ILIM} )')
s = s.replace('BIN   IN GND I=V(OUT)*V(IDEL)/{EFF}/max(V(IN),1) + V(GO)*{IQ}', 'BIN   IN GND I=max(V(OUT,GND),0)*V(IDEL)/{EFF}/max(V(IN,GND),1) + V(GO)*{IQ}')
s = s.replace('V=({IBASE} + {ISTEP}*0.5*(1+tanh((time-{TSTEP})/100u)))', 'V=({IBASE} + {ISTEP}*0.5*(1+tanh((time-{TSTEP})/100u)))*limit((V(RAIL,GND)-{VMIN}*0.5)/({VMIN}*0.5),0,1)')
s = s.replace('TRAMP=25m VMIN', 'TRAMP=25m VMIN')
s = '* Reviewed model: 100 nF SS => 18.868 ms by AP64501 DS41980 Rev 5-2 Eq.7.\n* Regulator current ceilings/efficiency and smooth UVLO remain screening assumptions.\n* Supply-dependent loads stop drawing at zero supply; boot ramps reset on collapse.\n' + s
p.write_text(s)

for p in [*root.glob('*.cir'), *root.glob('pdb/*.cir')]:
    s = p.read_text()
    s = s.replace('FROM 900m TO 1.1', 'FROM 899.9m TO 1.1')
    s = s.replace('FROM 300m TO 1.2', 'FROM 299.9m TO 1.2')
    if p.name == 'revb_regression.cir':
        s = s.replace('.end', '.meas TRAN SH_I2T INTEG I(RBATT)*I(RBATT) FROM 899.9m TO 1.1\n.end')
    p.write_text(s)

# Exact current schematic population: use actual designators, no unused feedback paths.
s = (root / 'pdb/pdb_ap2_revb.lib').read_text()
start = s.index('.subckt')
s = s[start:].replace('PDB_AP2_REVB', 'PDB_CURRENT')
s = s.replace('RUVB  N_UV', 'R2    N_UV').replace('RHG   GP', 'R14   GP')
s = s.replace('R2    VBAT_FUSED', 'R3    VBAT_FUSED').replace('R3    N_OV', 'R13   N_OV')
s = '\n'.join(line for line in s.splitlines() if not line.startswith(('RHO ', 'RH3 ', '*')))
s = s.replace('RPUF ', 'R15  ').replace('RPUA ', 'R16  ').replace('RPUC ', 'R17  ').replace('RPUD ', 'R18  ')
s = '* Current KiCad population; see audit/current.net.xml and check_connectivity.py.\n* Kelvin force stubs, fuse, FETs and IC models retain documented approximations.\n' + s + '\n'
(root / 'pdb/pdb_current.lib').write_text(s)
for src, dst in [('combined_startup.cir','current_startup.cir'), ('revb_regression.cir','current_faults.cir'), ('combined_reverse.cir','current_reverse.cir'), ('revb_uvstate.cir','current_uvstate.cir')]:
    s = (root / src).read_text().replace('pdb_ap2_revb.lib','pdb_current.lib').replace('pdb_ap2.lib','pdb_current.lib').replace('PDB_AP2_REVB','PDB_CURRENT').replace('PDB_AP2','PDB_CURRENT')
    (root / dst).write_text(s)
