# Gate-feedback candidate: current implementation status

The proposed circuit was already present in KiCad when this review started.
The active schematic uses these actual designators:

| Function | Current population |
|---|---|
| UV divider | R1 1M0 from VBAT_FUSED to LTC_UV; R2 47k to GND |
| OV divider | R3 2M0 from VBAT_FUSED to LTC_OV; R13 54k9 to GND |
| Hysteresis | R14 20M from GATE_PIN to LTC_UV |
| Breaker shunt | R5 8 mOhm |
| Fuse | F1 5 A, 0297005.WXNV, provisional |
| Testpoint pull-ups | R15/R16 10k to PDB_3V3 |
| I2C pull-ups | R17/R18 4.7k to PDB_3V3 |

See [REVIEW.md](REVIEW.md) for results and unresolved electrical limits.
Lowering the electronic trip and raising fuse rating does not establish fuse,
cable or MOSFET coordination. A nominal sweep does not qualify the leakage-
sensitive 20 MOhm feedback network. The circuit does not contain a UV latch;
a settled off state can restart when source voltage changes.

Experimental `revb_*.cir` decks retain alternate feedback branches for comparison.
Use `current_*.cir` for the exact present resistor population.
Original proposal text is retained in `audit/original-files/REVB-PROPOSAL.md`.
