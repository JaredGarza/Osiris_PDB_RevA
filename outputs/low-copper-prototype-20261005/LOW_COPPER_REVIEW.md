# Osiris PDB REV1.1 — Low Copper Prototype

Prepared October 5, 2026 from the current Osiris_PDB_RevA project.

**Selected prototype specification: 1 oz outer / 0.5 oz inner, four-layer FR-4, 1.6 mm total thickness. This is the lowest standard copper combination listed by JLCPCB, not a demonstrated minimum for the board's current targets. The 60 A continuous / 100 A for 30 seconds targets remain unqualified.**

Open `Osiris_PDB_RevA.kicad_pro`. This branch keeps the repository's original project filenames, with the revised low-copper PCB in place. Keep the local Libraries folder and library tables beside the project. The schematic and component placement remain the same as the source design. The bottom silkscreen identifies this board as `LC TEST 1/0.5oz`.

The input and ESC positive pours were widened on the top and supplemented with parallel bottom pours. The sharp top-zone step near J3 was removed. In1 remains an uninterrupted ground-plane zone; In2 now carries ground in its unused left, lower and right regions rather than filling those regions with positive copper. Added 22 vias: five distributed ESC ties, fourteen return-path ties and three local capacitor/test-point ground ties. Three short ground tracks connect the latter pads to their new vias. Existing routed tracks, vias, footprint positions, pad geometry and part selections were preserved.

All-severity PCB DRC, unconnected-item checks, schematic parity and schematic ERC passed with zero reported issues. Thirteen Gerber/drill files were independently parsed, and exported copper artwork was visually reviewed. The Gerber job specifies 35 / 17.5 / 17.5 / 35 µm copper. The generic dielectric entries maintain nominal 1.6 mm thickness; use the manufacturer's standard compatible stackup rather than treating those entries as a controlled dielectric requirement.

## Quotation files

Use `outputs/low-copper-prototype-20261005/Osiris_PDB_REV1.1_LowCopper_Prototype_Gerbers.zip` for PCB upload. The same directory contains the unchanged BOM/CPL, assembly instructions, fabrication notes and checks; start with `START_HERE.md`. Earlier manufacturing packages retained in this repository describe the original board and must not be used for this revision. Select **1 oz outer and 0.5 oz inner explicitly** on the quote page; Gerber artwork alone does not establish copper weight. No order has been placed, and no savings amount has been verified.

## Resistance screening and test limits

A nominal room-temperature DC grid model compared the original and widened layouts. It includes positive paths and the ESC ground return, sheet-copper conductance and nominal 25 µm plated via barrels. It assumes ideal connector terminals and excludes fuse/contact/solder resistance, enclosure behavior and thermal coupling. Pads were simplified to rectangles/circles. This is a screening model, not a certified field solver or thermal simulation.

| Layout | Outer / inner | Estimated copper loop resistance | Estimated copper-only loss at 60 A |
|---|---|---:|---:|
| Original | 2 / 2 oz | 0.83 mΩ | 3.0 W |
| Widened | 2 / 1 oz | 1.06 mΩ | 3.8 W |
| Widened | 2 / 0.5 oz | 1.34 mΩ | 4.8 W |
| **Selected lowest-copper prototype** | **1 / 0.5 oz** | **2.07 mΩ** | **7.5 W** |

The selected prototype's estimated copper loop resistance is approximately **2.5 times the original** despite widening. Its approximate copper-only drop is 124 mV at 60 A. These figures do not include the fuse's substantial additional loss, and copper resistance increases with temperature. A preliminary 0.25 mm grid and the final 0.20 mm grid gave similar loop estimates, but that numerical agreement does not validate the model assumptions. Raw results are in `outputs/low-copper-prototype-20261005/checks/dc-screen-0.2.json`; that file records the geometry hashes.

Load/temperature measurements are required before accepting this copper choice for the current targets. Test both positive and ground drop, fuse/connector/via-region temperatures, and avionics behavior in the actual enclosure and ambient conditions. Input current can reach 65 A continuous or 105 A burst with a simultaneous 5 A avionics load; the model table above considers the 60 A ESC loop alone. Establish component-based temperature limits and measure steady-state behavior before attempting the target burst. If the lowest-copper prototype fails those requirements, use the measured results to select a heavier build or revise the layout further. This review cannot establish the lowest electrically adequate copper weight without those results.

Manufacturer copper options: [JLCPCB copper-weight guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight). Current availability and price depend on the selected manufacturing/assembly service.
