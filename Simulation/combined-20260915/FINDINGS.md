# Historical 42-component simulation

The original findings have been superseded by [REVIEW.md](REVIEW.md).
The source population remains available in `pdb/pdb_ap2.lib`; the active
schematic is modeled by `pdb/pdb_current.lib`.

The old report used a 2 ms buck soft-start instead of the capacitor-derived
18.868 ms, started short-circuit energy integration after the initial fault
pulse, and included supply-independent current sinks. Its precise timing,
energy, low-voltage behavior and thermal conclusions must not be reused.
The original text is retained in `audit/original-files/FINDINGS.md` for traceability.

The budget comparison was an arithmetic consistency check using shared assumed
loads, not an independent validation against hardware measurements. The weak-pack
retry mechanism remains visible in corrected historical-population simulations.
