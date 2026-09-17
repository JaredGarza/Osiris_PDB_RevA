"""Failure-injection checks for the verification runner (no LTspice required)."""
import importlib.util
from pathlib import Path
import subprocess, tempfile, unittest
from unittest.mock import patch
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('runner',root/'verify_all.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
class RunnerTests(unittest.TestCase):
 def run_case(self,log,code=0,timeout=False):
  with tempfile.TemporaryDirectory(dir=root/'audit') as folder:
   deck=Path(folder)/'pdb_smoke.cir'
   deck.write_text('.meas TRAN VOUT_FINAL AVG V(OUT)\n.meas TRAN V3V3_FINAL AVG V(V3)\n')
   deck.with_suffix('.log').write_text('stale successful result')
   class FakeProc:
    pid=123
    def __init__(self):self.waits=0
    def wait(self,timeout=None):
     self.waits+=1
     if timeout and self.waits==1 and self_timeout:raise subprocess.TimeoutExpired('LTspice',1)
     return code
    def kill(self):pass
   self_timeout=timeout
   def engine(*args,**kwargs):
    self.assertFalse(deck.with_suffix('.log').exists())
    if not timeout:deck.with_suffix('.log').write_text(log)
    return FakeProc()
   with patch.object(runner.subprocess,'Popen',side_effect=engine), \
        patch.object(runner.subprocess,'run',return_value=subprocess.CompletedProcess([],0)):
    return runner.run(deck,Path('fake'),1)
 good='Total elapsed time: 1 seconds.\nvout_final: AVG(V(OUT))=14.7 FROM 0 TO 1\nv3v3_final: AVG(V(V3))=3.28 FROM 0 TO 1\n'
 def test_valid(self):self.assertEqual(self.run_case(self.good)['status'],'PASS')
 def test_bad_return_code(self):self.assertEqual(self.run_case(self.good,code=1)['status'],'FAIL')
 def test_timeout(self):self.assertEqual(self.run_case('',timeout=True)['status'],'FAIL')
 def test_missing_measurement(self):self.assertEqual(self.run_case(self.good.split('v3v3_final')[0])['status'],'FAIL')
 def test_electrical_failure(self):self.assertEqual(self.run_case(self.good.replace('=14.7','=0.1'))['status'],'FAIL')
 def test_floating(self):self.assertEqual(self.run_case(self.good+'Node OUT is floating\n')['status'],'FAIL')
 def test_timing_parser(self):self.assertEqual(runner.measurements('t_3v3: V(V3)=3.1 AT 0.117\n')['t_3v3'],[0.117])
 def test_missing_stepped_row(self):
  log='Total elapsed time: 1 seconds.\n.step x=1\n.step x=2\nMeasurement: vout_final\n  step value FROM TO\n  1 14.7 0 1\nMeasurement: v3v3_final\n  1 3.28 0 1\n  2 3.28 0 1\n'
  self.assertEqual(self.run_case(log)['status'],'FAIL')
if __name__=='__main__':unittest.main()
