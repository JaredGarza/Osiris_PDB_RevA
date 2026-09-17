"""Fresh LTspice runs. PASS is a screening check, never hardware qualification."""
from pathlib import Path
import argparse, hashlib, json, math, os, re, subprocess, sys, time
ROOT = Path(__file__).resolve().parent
NUMBER = r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'

def measurements(log):
    result, current = {}, None
    for line in log.splitlines():
        m = re.match(r'Measurement:\s*(\w+)', line, re.I)
        if m:
            current = m[1].lower()
            result[current] = []
            continue
        if current:
            m = re.match(r'\s+\d+\s+('+NUMBER+r')(?:\s|$)', line)
            if m: result[current].append(float(m[1]))
        m = re.match(r'(\w+):.*?(?:=\s*|\bAT\s+)('+NUMBER+r')\s*(?:FROM|at|$)', line, re.I)
        if m: result[m[1].lower()] = [float(m[2])]
        timing = re.match(r'(\w+):.*\bAT\s+('+NUMBER+r')\s*$', line, re.I)
        if timing: result[timing[1].lower()] = [float(timing[2])]
    return result

# Absolute maximum ratings, not deratings. LTC4368 Rev C p.4 and Infineon
# BSC070N10NS5 rev 2.3. UV/OV/RETRY/SHDN/FAULT may sit below -0.3 V provided
# the pin current stays under 1 mA (LTC4368 Note 3), so those pins are checked
# by current in post-processing rather than by voltage here.
PIN_STRESS = {
    'u1_vin_min': (-40, 100), 'u1_vin_max': (-40, 100),
    'u1_vout_min': (-10, 80), 'u1_vout_max': (-10, 80),
    'u1_sense_min': (-10, 80), 'u1_sense_max': (-10, 80),
    'u1_vout_sense_abs': (0, 10),
    'u1_vin_vout_min': (-60, 100), 'u1_vin_vout_max': (-60, 100),
    'u1_gate_min': (-40, 100), 'u1_gate_vin_max': (-40, 14),
    'u1_retry_min': (-0.3, 5), 'u1_retry_max': (-0.3, 5),
    'q1_vds': (0, 100), 'q2_vds': (0, 100),
    'vgs_max': (0, 20),
    'inp_min': (-0.3, 100), 'inn_min': (-0.3, 100), 'vbus_min': (-0.3, 100),
}

def limits(name):
    # A-P4 release decks are the live 59-symbol KiCad population. Reuse the
    # established A-P3 functional bounds and add the new front-end stresses.
    if name.startswith('release_'):
        suffix=name.removeprefix('release_')
        base=dict(limits('final_'+suffix))
        if suffix in ('transients','transients_fine','filter_mismatch'):
            base.update(PIN_STRESS)
            # Live Q1/Q2 remain 60 V parts, unlike the historical HV candidate.
            base.update({'q1_vds':(0,60), 'q2_vds':(0,60),
                         'v3v3_max':(0,3.6), 'vout_final':(12,16.8)})
        base.update({
            'inp_min':(-0.3,85), 'inn_min':(-0.3,85), 'vbus_min':(-0.3,85),
            'inp_max':(-0.3,85), 'inn_max':(-0.3,85), 'vbus_max':(-0.3,85),
            'q3_vds':(0,100), 'q3_vgs':(0,20),
            'u5_in_min':(-40,100), 'u5_in_max':(-40,100),
            'u5_out_min':(-0.3,100), 'u5_out_max':(-0.3,100),
            'u5_gs_min':(-1,20), 'u5_gs_max':(-1,20),
            'c11_stress':(0,63), 'c16_stress':(0,63),
            # INA228 absolute differential rating is +/-40 V (datasheet 6.1).
            # The +/-163.84 mV ADC range is a measurement range, not damage.
            'ina_diff':(0,40),
        })
        return base
    if re.fullmatch(r'hv[a-z]_transients', name):
        return PIN_STRESS
    # Protection-candidate decks reuse the corresponding final_* limits, plus
    # the INA228 analog pin floor that the earlier fault decks never checked.
    m = re.fullmatch(r'hv[a-z]_(\w+)', name)
    if m:
        base = limits('final_' + m[1])
        if 'faults' in m[1]:
            base = {**base, 'inp_min': (-0.3, 100), 'inn_min': (-0.3, 100),
                    'vbus_min': (-0.3, 100)}
        return base
    if name=='final_i2c':
        return {'rise_time':(0,1e-6), 'low_level':(0,.4), 'high_level':(2.52,3.6), 'sink_current':(0,.003)}
    if name in ('final_corners','final_lowtrip','final_temperature'):
        return {'v5_ss':(5,5.3), 'v3_ss':(3.1,3.5), 'v5p_ss':(4.9,5.3), 'v3v3_pdb':(3.1,3.5), 'iin_peak':(0,7.5), 'iin_lowv':(0,5.8), 'iin_step':(0,2.5), 't_3v3':(0.03,0.25)}
    if name == 'final_faults_fine':
        return {'sh_vosin':(-0.3,0.5), 'sh_i2t':(1e-6,1), 'uv_rec_v3':(3.1,3.5)}
    if name == 'final_faults':
        return {'rec_v5':(5,5.3), 'rec_v3':(3.1,3.5), 'uv_rec_v5':(5,5.3), 'uv_rec_v3':(3.1,3.5), 'ov_rec_v5':(5,5.3), 'sh_vosin':(-0.3,0.5), 'sh_i2t':(1e-6,1), 't_rec_v3':(1.1,2.9)}
    if name in ('final_reverse','final_reverse25'):
        return {'rec_v5':(5,5.3), 'rec_v3':(3.1,3.5), 'rev_vosin':(-0.3,0.1), 'rev_iin':(0,0.002), 'rev_v5':(-0.05,0.1), 'rev_v3':(-0.05,0.1)}
    if name in ('eco_corners','eco_lowtrip','eco_delay','eco_zeroout','eco_temperature'):
        return {'v5_ss':(5,5.3), 'v3_ss':(3.1,3.5), 'v5p_ss':(4.9,5.3), 'v3v3_pdb':(3.1,3.5), 'iin_peak':(0,2.9), 'iin_step':(0,2.5), 't_3v3':(0.03,0.25)}
    if name in ('eco_faults','eco_faults_fine'):
        return {'rec_v5':(5,5.3), 'rec_v3':(3.1,3.5), 'uv_rec_v5':(5,5.3), 'uv_rec_v3':(3.1,3.5), 'ov_rec_v5':(5,5.3), 'sh_vosin':(-0.3,0.5), 'sh_i2t':(1e-6,1), 't_rec_v3':(1.1,2.9)}
    if name == 'eco_reverse25':
        return {'rec_v5':(5,5.3), 'rec_v3':(3.1,3.5), 'rev_vosin':(-0.3,0.1), 'rev_iin':(0,0.002), 'rev_v5':(-0.05,0.1), 'rev_v3':(-0.05,0.1)}
    if name in ('combined_startup', 'current_startup', 'current_corners', 'slowgate_corners', 'closure_corners', 'closure_lowtrip', 'gatefix_corners', 'gatefix_lowtrip', 'gate470_corners', 'gate470_lowtrip', 'coordinated_corners', 'coordinated_lowtrip', 'coord12_corners', 'coord12_lowtrip', 'eco_corners', 'eco_lowtrip', 'eco_delay'):
        return {'v5_ss':(5,5.3), 'v3_ss':(3.1,3.5), 'v5p_ss':(4.9,5.3), 'v3v3_pdb':(3.1,3.5), 'iin_peak':(0,4.9), 't_3v3':(0.03,0.25)}
    if name in ('revb_regression', 'current_faults', 'combined_faults', 'closure_faults', 'gatefix_faults', 'gate470_faults', 'coordinated_faults', 'eco_faults', 'eco_faults_fine'):
        return {'rec_v5':(5,5.3), 'rec_v3':(3.1,3.5), 'sh_vosin':(-0.3,0.5), 'sh_i2t':(1e-6,1), 't_rec_v3':(1.1,2.9)}
    if name in ('combined_reverse','current_reverse','closure_reverse', 'eco_reverse'):
        return {'rec_v5':(5,5.3), 'rec_v3':(3.1,3.5), 'rev_vosin':(-0.3,0.1), 'rev_iin':(0,0.002), 'rev_v5':(-0.05,0.1), 'rev_v3':(-0.05,0.1)}
    if name == 'current_faults_fine': return {'sh_vosin':(-0.3,0.5), 'sh_i2t':(1e-6,1)}
    if name == 'pdb_smoke': return {'vout_final':(14,14.8), 'v3v3_final':(3.1,3.5)}
    if name == 'osiris_smoke': return {'v5_final':(5,5.3), 'v3_final':(3.1,3.5), 'v5p_final':(4.9,5.3)}
    if name == 'model_sanity': return {'dead_min':(-0.001,0.001), 'ldo_min':(-0.001,0.001), 'disabled_delivery':(0,1e-6), 'boot_early':(0,0.15), 'boot_late':(0.9,1.01)}
    return {}

def run(deck, engine, timeout):
    logpath = deck.with_suffix('.log')
    logpath.unlink(missing_ok=True)
    start, errors = time.time(), []
    try:
        # Avoid inherited pipes: an LTspice child can hold them after a timeout,
        # turning a 180 s timeout into an hour-long block. The .log is canonical.
        proc = subprocess.Popen([str(engine), '-b', '-Run', str(deck)], cwd=deck.parent,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        try:
            code=proc.wait(timeout=timeout)
            if code: errors.append(f'engine exit {code}')
        except subprocess.TimeoutExpired:
            errors.append(f'timeout after {timeout}s')
            if os.name=='nt':
                subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            else:
                proc.kill()
            proc.wait(timeout=15)
    except subprocess.TimeoutExpired: errors.append(f'timeout after {timeout}s')
    log = logpath.read_text(errors='replace') if logpath.exists() else ''
    if not log or 'Total elapsed time:' not in log: errors.append('missing completed fresh log')
    for line in log.splitlines():
        if re.search(r'^Error|Fatal|timestep too small|singular matrix|is floating|tolerance relaxed|unknown subcircuit|could not open|not found', line, re.I): errors.append(line.strip())
    data = measurements(log)
    expected = re.findall(r'^\.meas\s+\w+\s+(\w+)', deck.read_text(), re.I|re.M)
    optional = {'extra_t'} if deck.stem in ('revb_thresholds','revb_fbnode') else set()
    steps = max(1, len(re.findall(r'^\.step\s', log, re.M|re.I)))
    for name in expected:
        values = data.get(name.lower(), [])
        if name.lower() in optional:
            if values: errors.append(f'{name}: unexpected extra transition')
            continue
        if len(values) != steps or not all(math.isfinite(v) for v in values): errors.append(f'{name}: expected {steps} finite values, got {len(values)}')
    checks = limits(deck.stem)
    for name, (low, high) in checks.items():
        values = data.get(name, [])
        if not values or any(not low <= v <= high for v in values): errors.append(f'{name}: {values} outside [{low}, {high}]')
    return dict(deck=str(deck.relative_to(ROOT)), status='FAIL' if errors else ('PASS' if checks else 'RUN_OK'), seconds=round(time.time()-start,2), errors=errors, measurements=data, limits=checks)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('decks', nargs='*')
    parser.add_argument('--engine', default=os.environ.get('LTSPICE_EXE',r'C:\Program Files\ADI\LTspice\LTspice.exe'))
    parser.add_argument('--timeout', type=int, default=300)
    parser.add_argument('--all-experiments', action='store_true', help='Include historical populations and rejected experiments')
    args = parser.parse_args()
    engine = Path(args.engine)
    if not engine.exists(): parser.error(f'LTspice executable not found: {engine}')
    if args.decks: decks = [ROOT / p for p in args.decks]
    elif args.all_experiments: decks = sorted([*ROOT.glob('*.cir'),*ROOT.glob('pdb/*.cir'),*ROOT.glob('osiris/*.cir')])
    else: decks = [ROOT/p for p in json.loads((ROOT/'active_decks.json').read_text())]
    results = []
    for deck in decks:
        result = run(deck, engine, args.timeout)
        results.append(result)
        print(f"{result['status']:7s} {result['deck']} ({result['seconds']}s)", flush=True)
        for error in result['errors'][:12]: print('  '+error, flush=True)
    sources = sorted(set(decks + list(ROOT.glob('*/*.lib')) + [ROOT.parent/'models/U21_SCREEN.lib']))
    dependencies=set(sources)
    queue=list(sources)
    while queue:
        source=queue.pop()
        for included in re.findall(r'^\s*\.(?:inc|include|lib)\s+([^\r\n]+)',source.read_text(errors='replace'),re.M|re.I):
            path=Path(included.strip().strip('"'))
            if not path.is_absolute():path=(source.parent/path).resolve()
            if path.exists() and path.is_file() and path not in dependencies:
                dependencies.add(path);queue.append(path)
    sources=sorted(dependencies)
    report = {'timestamp':time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'scope':'Model screening, not hardware qualification', 'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}, 'results':results}
    (ROOT/'audit/verification.json').write_text(json.dumps(report,indent=2))
    return int(any(r['status']=='FAIL' for r in results))
if __name__ == '__main__': sys.exit(main())
