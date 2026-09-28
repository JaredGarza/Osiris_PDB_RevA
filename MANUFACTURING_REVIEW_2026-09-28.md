# PDB manufacturing review — 28 September 2026

**Decision: NO-GO for a final manufacturing release.** This is the active
`A-P4-DRAFT` PDB in `Osiris_PDB_RevA.kicad_pro`. Do not send the temporary
Gerbers or order assembly as a released design. A limited engineering prototype
would need a separate, explicit acceptance of the open mechanical and
electrical risks.

## CAD checks on the Desktop working copy

| Check | Result |
| --- | --- |
| Schematic ERC, all enabled severities | 0 findings |
| PCB DRC, zones refilled, all track errors | 3 findings: H3/J4 courtyard overlap; Q1/Q2 differ from the local footprint library |
| Unconnected board items | 0 |
| Schematic-to-PCB parity | 17 findings: 13 grouped MOSFET pad numbers, 4 symbol footprint-filter mismatches |
| Board | 2 copper layers, 1.6 mm nominal, 35 µm copper per layer, 64 footprints |
| Fabrication-file test | Gerber layers and drill files export; outline is closed; 223 plated and 4 non-plated holes, including six 0.6 mm plated slots |

Reports and a fresh 60-row schematic BOM are in `review/2026-09-28/`. Seven
test pads correctly have no purchasing MPN. The prior September 15 documents
refer to older 4/5 A fuse and 5/8 mΩ shunt combinations, and must not be used
as the active population list. This board has **F1 = 4 A** and **R5 = 5 mΩ**.

## Changes made in this review

- Set the board-wide copper clearance to **0.20 mm** from 0.25 mm. The smallest
  measured clearance among the formerly flagged routes was 0.20 mm. This is
  above JLCPCB's published 0.10 mm trace/space capability for a 2-layer, 1 oz
  FR-4 board, assuming copper is covered by solder mask. This clears 99
  previously reported spacing findings; it does not change the copper shapes.
  The selected fabrication order must use 1 oz copper unless the rules are
  checked again for a heavier-copper process.
- Removed one off-board table mistakenly on `Edge.Cuts` and six non-electrical
  silkscreen bars that crossed capacitor outlines. Repositioned U4, C9, and
  C14 reference labels away from exposed pads.
- Updated D3 on the PCB to the project-local DPAK footprint, retained its
  cathode on `PDB_VOUT` and both anode leads on GND, and matched its hidden
  schematic fields. This removed D3's library and parity discrepancies.
- Re-enabled KiCad's missing-courtyard, footprint type/filter, and off-center
  via checks as warnings. No additional PCB geometry violations appeared;
  four footprint-filter metadata mismatches appeared in parity.

## Release gates

1. **Mechanical fit:** H3's mounting-hole courtyard overlaps J4's output XT60
   courtyard. The four holes form a 45 × 40 mm pattern. Confirm the actual
   screw/washer/head, connector body and mating cable clearance against the
   enclosure. Move H3 or J4 only after the hole pattern and connector edge
   positions are approved; then reroute and rerun DRC.
2. **Power MOSFET land pattern:** The placed Q1/Q2 footprints use one merged
   source copper pad numbered 1, gate pad 4, and one merged drain pad numbered
   5. The local library contains separate pads 2/3/6/7/8, so KiCad flags two
   library mismatches. Q3 uses the same grouped-pad convention in its stock
   footprint. The [Infineon ISC015N06NM5LF2 datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-isc015n06nm5lf2-datasheet-en.pdf)
   identifies pins 1–3 as source and 5–8 as drain, which explains the 13
   parity findings but does not itself approve the solder land, mask, or paste
   geometry. Check Gerber copper and stencil apertures against the ordered
   packages, then make the library and placed footprints consistent.
3. **Electrical protection:** The current D3 100 V/10 A Schottky clamp has not
   been shown to keep the INA228 sense/VBUS pins within their negative absolute
   limits during reverse input or output collapse. The TVS energy and clamp
   voltage, LTC4368 and FET stress during hot-plug/retry, battery short-circuit
   duty, and F1/trace/holder thermal coordination also remain unqualified.
   The earlier [electrical review](docs/PDB-ELECTRICAL-REVIEW-20260915.md)
   identifies these mechanisms; its component population numbers are stale.
4. **Current and temperature:** The main feed uses top-layer copper pours,
   several 1.0 mm segments, and 3.0 mm output segments. The 0.3 mm branches on
   power-named nets go to sense/control circuitry. This is a plausible layout
   for the **25 W and 2.5 A** operating target, not proof of survival up to
   the 4 A fuse's clearing time or a higher battery fault current. Confirm
   actual load current, copper drop, hot-spot temperature and fault duration.
5. **Mating and assembly:** Verify J1 input and J3/J4 output cable polarity
   with the real harness. Confirm the 0.6 mm plated slots and through-hole
   component fit. If JLCPCB will assemble the board, reconcile the fresh BOM,
   part availability, footprint/paste, placement files, and remaining
   `Selection_Status` notes that still say verification is pending.

## Fabrication assumptions and evidence

The draft Gerber/drill export was made only in a temporary review directory,
outside this project. It is **not a release package**. The order settings to
confirm are 2-layer FR-4, 1.6 mm, 1 oz finished outer copper, solder mask,
surface finish, NPTH/PTH separation, and connector/mounting clearances. The
[JLCPCB rigid-board capabilities](https://jlcpcb.com/capabilities/Capab) list
0.10 mm minimum 1 oz trace/space and 0.5 mm minimum plated-slot width for
2-layer FR-4. Its [copper-weight guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight)
requires wider trace/space for heavier copper. The [ST D3 datasheet](https://www.st.com/resource/en/datasheet/stpst10h100sb.pdf)
shows two anode terminals and the cathode/tab arrangement used here.

KiCad's zero ERC count excludes four project-configured categories (single
global labels, four-way junctions, SPICE models, footprint filters). The only
remaining ignored PCB category is tuning-profile geometry. CAD checks do not
replace electrical fault tests or physical fit validation.
