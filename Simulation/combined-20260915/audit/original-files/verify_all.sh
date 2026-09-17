#!/usr/bin/env bash
# Re-run every deck against the FINAL model files and report pass/fail.
# Several decks were originally run before the DIGILOAD guard fix and the
# tanh smoothing, so this confirms the reported numbers still hold.
LT="C:/Program Files/ADI/LTspice/LTspice.exe"
cd "$(dirname "$0")" || exit 1

run() {
  local deck="$1" dir="$2"
  local base="${deck%.cir}"
  ( cd "$dir" && rm -f "$base.log" && timeout 1800 "$LT" -b -Run "$deck" >/dev/null 2>&1 )
  local log="$dir/$base.log"
  if [ ! -f "$log" ]; then
    printf '%-26s FAIL  no log produced\n' "$base"; return 1
  fi
  local err warn meas
  err=$(grep -ciE '^error|Node .* is floating|not found' "$log")
  warn=$(grep -c 'tolerance relaxed' "$log")
  meas=$(grep -cE '^[a-z0-9_]+:|^  step' "$log")
  if [ "$err" -gt 0 ]; then
    printf '%-26s FAIL  %s error(s)\n' "$base" "$err"
    grep -iE '^error|is floating|not found' "$log" | head -3 | sed 's/^/                             /'
    return 1
  fi
  if [ "$meas" -eq 0 ]; then
    printf '%-26s FAIL  no measurements returned\n' "$base"; return 1
  fi
  printf '%-26s pass  warnings=%-6s measurements=%s\n' "$base" "$warn" "$meas"
}

echo "=== PDB standalone ==="
run pdb_smoke.cir        pdb
run pdb_thresholds.cir   pdb
run pdb_overcurrent.cir  pdb
echo
echo "=== Osiris standalone ==="
run osiris_smoke.cir     osiris
echo
echo "=== Combined ==="
run combined_startup.cir   .
run combined_faults.cir    .
run combined_reverse.cir   .
run combined_brownout.cir  .
run combined_uvchatter.cir .
run combined_uvstate.cir   .
echo
echo "=== Rev-B candidate ==="
run revb_thresholds.cir  .
run revb_fbnode.cir      .
run revb_fbsweep.cir     .
run revb_overcurrent.cir .
run revb_regression.cir  .
