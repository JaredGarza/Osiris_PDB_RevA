# Osiris PDB Rev A — JLCPCB prototype manufacturing review

Prepared October 2, 2026. Source schematic revision: A-P6-PROTOTYPE.

**Status: package prepared for quotation and manufacturer DFM review. Order release remains pending parts matching, assembly-preview approval, and confirmation of stackup and panelization. The 60 A continuous / 100 A for 30 seconds ESC targets remain unqualified. No order has been submitted.**

## Completed

- Removed the redundant F.Cu PDB_VOUT zone contained within the existing F.Cu/B.Cu zone, then refilled and saved the board.
- Final ERC and PCB DRC report zero violations, zero unconnected items, and zero schematic parity issues. Warnings and exclusions were included. The only ignored PCB check concerns track-tuning profiles.
- Enabled 0.15 mm silkscreen clearance, 1.0 mm minimum text height, and 0.15 mm text stroke. Enlarged undersized reference text, thickened test-point labels, adjusted film-capacitor outlines, and removed duplicate IC markers. U2's crowded silk marker was removed; its fabrication-layer marker and the assembly drawing identify pin 1.
- Increased the two J4 plated mounting-slot pads from 0.9 × 2.0 mm to 1.2 × 2.3 mm. Their 0.6 × 1.7 mm drills are unchanged. End and side annular rings are now 0.30 mm. Saved this footprint in the local project library and updated the schematic library link.
- Added exact ordering codes for C18 (TDK C2012X7R1H105K125AB), C19 (KEMET C0805C104K5RACTU), and D5 (Bourns SMBJ24CA). These preserve the existing nominal values and footprints. Selection does not establish current JLCPCB inventory or transient qualification.
- Added the Keystone 3568 holder as the fitted F1 item in the JLCPCB BOM. The Littelfuse 029707.5WXNV blade fuse is listed separately for insertion after soldering.
- Generated 11 Gerber layers, separate plated/non-plated drill files, a Gerber job file, IPC-D-356 netlist, BOM, CPL, placement review, DNP list, assembly drawing, and fabrication notes.
- Validated agreement between the BOM and CPL for **56 fitted parts in 41 BOM groups**. R17/R18 are DNP; H1–H4 are bare mounting holes; TP1–TP7 are bare test pads. No bottom-side components are fitted in this build.
- Compared the edited PCB with the original Git revision: track/via geometry, footprint positions/orientations, pad nets, and drill sizes are unchanged. The only pad-size changes are the two documented J4 mounting-slot annular rings.
- Parsed all 13 Gerber/drill files with an independent reader and visually inspected copper, solder paste, and silkscreen exports. The reader accepts KiCad's drill files with a G90-header-order warning. KiCad's drill report gives 241 plated holes/slots and four non-plated mounting holes.

## Package use

Upload `Osiris_PDB_RevA_JLCPCB_Gerbers.zip` for PCB quotation. Use `assembly/JLCPCB_BOM.csv` and `assembly/JLCPCB_CPL.csv` for assembly quotation. The full review ZIP contains notes, checks, the supply-separately list, and assembly drawings; it is not a substitute for the Gerber-only upload ZIP.

`source_snapshot` freezes the CAD files and local libraries used for this export. `SHA256_MANIFEST.json` records source and delivered-file hashes. Standard KiCad libraries and the original repository's Datasheets directory are external resources; they are not bundled in the source snapshot. The annotated drawing is supplied as SVG and PNG.

The BOM's LCSC-number fields are intentionally blank. Match by **both exact manufacturer and exact MPN** in JLCPCB's order interface. A matching family name is insufficient. In particular, do not replace LTC4368 **-1** with **-2**, or substitute a different MOSFET or generic SMBJ24CA manufacturer without an engineering review. Public catalog searches did not establish exact assembly availability for the selected U1, Q1/Q2, or F2. J1/J3 have an LCSC listing, but that does not establish JLCPCB assembly stock or acceptance.

Use Standard PCBA as the planning route because of the heavy-copper stackup, large terminal blocks, and mixed SMT/THT assembly. Confirm the selected assembly service at quotation. The board outline is 127.5 × 65.0 mm; request a routed manufacturing panel with rails and fiducials meeting JLCPCB's minimum assembly dimensions. Two 5 mm rails above and below would give a nominal 127.5 × 75 mm bounding size, subject to their final fixture/panel design. Supply single-board data and let JLCPCB repeat it. Keep tabs, tooling holes, and fiducials off the finished board's current paths.

Coordinates use KiCad's absolute datum in millimeters, X to the right and Y upward; KiCad board Y values are negated in the CPL. THT entries use the body/courtyard centers instead of pad-1 origins. SMT entries retain component origins; asymmetric courtyards were not used as SMT body centers. `Placement_Review.csv` records the original coordinates and actual pad-1 locations. **Every polarity, pin-1 position, rotation, and body alignment must be checked against JLCPCB's matched library preview before order release.** No assumed library rotation corrections have been applied.

## Power-path desk review

| Path | Findings | Qualification still needed |
| --- | --- | --- |
| J1 → F2 → J3 ESC | F2 connects raw input directly to ESC_VBAT. ESC positive uses a broad top zone plus In2 copper. Eleven 0.6 mm-drill stitching vias join ESC copper. J1/J3 each provide four plated pins per pole. Ground return includes F.Cu, In1, and B.Cu. The avionics protection chain is bypassed. | Current-sharing, copper constrictions, connector solder fill, terminal/harness heating, and voltage drop. Check via plating and current sharing rather than treating the via count as an ampacity rating. |
| F2 overload backup | SCHURTER 3-140-177 is 100 A / 50 VDC. The saved 3.4 × 6.15 mm pads, 3.3 mm gap, and ±3.35 mm centers agree with the manufacturer's drawing. | Manufacturer performance was measured on **22 mm-wide, 210 µm copper**, which differs from this 70 µm/layer design. Typical cold resistance 0.71 mΩ implies 2.56 W at 60 A and 7.1 W at 100 A; operating resistance rises with temperature. The published typical 110 mV drop at 100 A corresponds to 11 W. Derating and solder-joint heating need bench measurements. |
| Pack fault interruption | F2's interrupt rating depends on voltage: 600 A at 50 V, 1000 A at 32 V, 1300 A at 24 V, 2000 A at 16 V. F1 is rated 1000 A at 32 V. | Establish maximum pack voltage and prospective short-circuit current, including harness resistance. Do not assume the 2000 A / 16 V figure applies to a fully charged 16.8 V pack. Confirm a suitable voltage-specific rating and clearing-energy coordination. |
| J1 → F1 → Q3/U5 → Q1/Q2/U1 → R5 → J4 avionics | Separate protected branch; planning load 5 A. F1 is 7.5 A, R5 is 5 mΩ / 2 W, and the stated electronic breaker is nominally 10 A. Shunt dissipation is 0.125 W at 5 A and 0.5 W at 10 A. Q1/Q2 have custom source/drain copper primitives; their small anchor dimensions do not represent the complete pads. | Fuse/electronic-breaker coordination, startup/inrush and FET safe operating area, Kelvin accuracy, reverse-input/current blocking, effective C6 capacitance, and U3 stability. This review did not establish an assembled fault-clearing response. |
| ESC transient network | C17 is 470 µF / 35 V; D5 is a 24 V-standoff TVS. A 24 V-standoff TVS does not impose a 24 V maximum, and its stated 38.9 V clamp can exceed C17's 35 V rating. | Capture installed harness hot-plug/load-step/ringing waveforms and pulse energy. Demonstrate acceptable capacitor voltage and ripple, or revise the clamp/capacitor design before unrestricted pack use. |

The ESC branch has **no active reverse-polarity protection**. Review and label the keyed/verified pack harness accordingly. Do not apply the avionics branch's protection claims to J3.

Footprint checks covered the fuse pad drawing, the F1 holder's 9.92 × 3.40 mm hole pattern and 1.78 mm holes, J1/J3's 15 mm pole pitch and 1.6 mm drills, J4's slots, and Q1/Q2's source/gate/drain mapping. Physical samples, enclosure fit, mating cable polarity, and full solder-process qualification remain open. J1/J3 are approximately 39 mm above the PCB and need factory handling/fixture confirmation. No enclosure or harness model was supplied for collision testing.

## Before paying for prototypes

1. Confirm exact parts matching and available quantities for all 41 BOM groups. Resolve special sourcing/consignment for unavailable parts and get confirmation that JLCPCB will solder the tall J1/J3 terminals and F1 holder. Include the removable blade fuse as a separate supply item.
2. Confirm **four layers, 1.6 mm, ENIG, 2 oz finished copper on every copper layer**. JLCPCB's published option ties 2 oz inner copper to the JLC3313 stackup. The saved generic dielectric thicknesses are not a supplier-approved JLC3313 stackup. Obtain the actual build-up and plating specification; do not accept thinner inner copper as a silent substitution.
3. Confirm routed rails/fiducials, through-hole soldering, large-fuse paste deposition and reflow profile, and inspection of hidden power-device joints.
4. Check the matched assembly preview against the supplied drawing and pad-1 table. Resolve body-position and library-rotation corrections in a revised CPL, then regenerate its validation/checksums.
5. Approve the prototype quantity, quote, and the controlled bring-up plan below. This package does not authorize a production-volume build or establish the provisional current rating.

## Prototype bring-up and qualification plan

Record board serial, actual stackup, assembly lot, fixture/harness, supply settings, ambient temperature, measured voltages/current, temperatures, and scope captures for each test. Keep original measurements; do not mark a test passed without results.

1. **Incoming inspection:** confirm board dimensions, connector seating/polarity, all four layers' copper specification, plated-hole solder fill, fuse joints, IC orientation, and DNP R17/R18. Check continuity against the connector table in `assembly/ASSEMBLY_NOTES.md` and inspect for supply-to-ground shorts. Validate enclosure/cable fit before power.
2. **First power:** disconnect the ESC and host. Use a current-limited bench supply with no external load. Ramp within the intended operating range, checking unexpected current, heating, and the approximately 3.29 V local rail. A provisional 3.2–3.4 V rail window is a bring-up screen; final limits must use the regulator/divider tolerances and temperature requirements.
3. **Avionics branch:** apply incremental loads through J4 up to the intended 5 A. Measure shunt voltage with Kelvin probes (nominally 25 mV at 5 A), INA228 response, rail stability, and temperatures. Test startup with the actual downstream capacitance. Check UV/OV thresholds, fault/alert behavior and current limiting against the selected -1 controller datasheet and component tolerance envelope. Use a controlled electronic load for fault tests. Verify reverse blocking on this branch with J3 disconnected.
4. **Host interface:** verify cable contacts; J2 pin 1 is INA_ALERT, pin 2 SCL, pin 3 SDA, pin 4 GND. Confirm host-owned pull-ups and host-off behavior. Start with the saved 100 kHz / ≤90 pF bus assumption. Compare measured current and bus voltage with calibrated instruments.
5. **ESC low-load/transient testing:** start at low current using the intended harness. Capture hot-plug and load-step peaks at J1, J3, and C17 with appropriate probing. Keep C17 voltage within its rating and verify TVS pulse duty. Resolve excessive peaks before high-current tests.
6. **High-current qualification:** after the preceding tests pass, increase current in controlled steps while logging terminal, fuse, copper, via-region and ground-return temperatures and voltage drop. Establish an agreed maximum ambient/enclosure condition and thermal acceptance limits from component ratings before testing 60 A to steady state. The common input must carry ESC plus avionics load (65 A at simultaneous 60 A ESC + 5 A avionics). Attempt the provisional 100 A / 30 s ESC burst only after lower-load thermal results support it; input then carries up to 105 A with avionics. Repeat after cooldown and inspect solder joints afterward. Stop if temperature rises without stabilizing or approaches the agreed limit.
7. **Fault qualification:** establish source short-circuit duty and verify fuse/PCB/harness clearing coordination using an appropriately rated controlled fixture. Do not use an uncontrolled pack short as a bring-up test. Reinspect and remeasure the board following fault tests.

## Sources

- [JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/)
- [JLCPCB assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)
- [JLCPCB copper weights](https://jlcpcb.com/help/article/jlcpcb-copper-weight) and [2 oz inner-layer option](https://jlcpcb.com/quote/pcbOrderFaq/Copper%20Weight)
- [JLCPCB BOM](https://jlcpcb.com/help/article/bill-of-materials-for-pcb-assembly), [CPL](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly), and [parts matching/sourcing](https://jlcpcb.com/help/article/common-bom-and-cpl-matching-issues-and-explanations)
- Local SCHURTER_UHS.pdf pp. 2–3, Keystone_3568.pdf drawing, Littelfuse_297_MINI.pdf pp. 1–2, Datasheet ISC015N06NM5LF2.pdf pp. 1 and 11, and AMASS_XT60PW-F.pdf drawing in the project's Datasheets directory.
- [Phoenix Contact 1932588](https://www.phoenixcontact.com/en-sg/products/printed-circuit-board-terminal-mkdsp-25-2-1500-1932588)
- [C18 manufacturer specifications](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012X7R1H105K125AB), [C19 manufacturer specifications](https://search.kemet.com/download/specsheet/C0805C104K5RACTU), and [D5 manufacturer datasheet](https://www.bourns.com/docs/product-datasheets/smbj.pdf)
