# Osiris PDB REV1.1 Low Copper prototype fabrication

- Four-layer FR-4: F.Cu / In1.Cu / In2.Cu / B.Cu, 1.6 mm finished thickness.
- **1 oz outer / 0.5 oz inner copper**: nominal 35 / 17.5 / 17.5 / 35 µm. Confirm availability for the chosen assembly service. These are requested nominal copper weights, not measured factory minima.
- Use a standard compatible manufacturer stackup. Source dielectric entries are nominal thickness bookkeeping, not a prescribed dielectric/core build or impedance specification.
- ENIG finish, green solder mask proposed. Finished outline 127.5 × 65 mm from Edge.Cuts centerline. Stroke bounds add 0.05 mm; do not enlarge the board by this stroke.
- Separate metric PTH and NPTH drills, 263 plated holes/slots and four 3.2 mm NPTH mounting holes. Two 0.6 × 1.7 mm plated mounting slots at J4. Preserve single-board layer registration.
- Confirm finished hole/barrel plating and inspect solder fill on J1/J3. DC screening assumed 25 µm via barrel copper; the actual plating must be confirmed, and that model assumption is not a factory guarantee.
- Do not alter copper geometry, remove distributed vias, or change copper weights without updating the review.
- Electrical net test; comparison netlist supplied in checks/LowCopper.ipc.
- Factory panelization/rails/tooling outside finished-board current paths; confirm mixed SMT/THT assembly and support for the tall terminals.
- Review paste/reflow for F2 and power-device pads; inspect hidden joints. Insert the separately supplied F1 blade fuse after soldering.
- **Test prototype. Current capacity, enclosure temperatures, voltage drop and fault duty have not been physically qualified.**
