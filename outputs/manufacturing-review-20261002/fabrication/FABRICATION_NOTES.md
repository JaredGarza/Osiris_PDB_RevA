# Osiris PDB Rev A prototype fabrication requirements

For JLCPCB quotation/DFM review; obtain agreement before manufacturing.

- FR-4, four copper layers: F.Cu / In1.Cu / In2.Cu / B.Cu.
- Finished thickness 1.6 mm. ENIG finish; green solder mask proposed for prototypes.
- **2 oz finished copper (nominal 70 µm) on all four layers. Inner copper must not default to 0.5 oz.** Confirm JLC3313 availability and supply the actual approved dielectric build-up. Generic source dielectric values are not an approved factory stackup.
- Board outline 127.5 × 65.0 mm from Edge.Cuts centerline. Gerber aperture bounds include the 0.05 mm outline stroke; do not enlarge the board by this stroke.
- Routed outline; no V-scoring through the finished board. Four 3.2 mm NPTH mounting holes.
- Separate metric PTH and NPTH Excellon files; do not mirror or recenter individual layers. Two 0.6 × 1.7 mm plated mounting slots at J4.
- Electrical net test using supplied fabrication data; IPC-D-356 comparison netlist is in the checks folder of the full package.
- Confirm hole/barrel plating, especially the current-sharing connector holes and 0.6 mm stitching vias. Preserve all copper/via geometry; no silent copper-weight or via substitutions.
- Request Standard mixed SMT/THT assembly. Supply single-board data and factory panelization. Provide rails, tooling holes and fiducials meeting assembly minimum dimensions; proposed 5 mm rails above/below the board require manufacturer fixture/tab review.
- Keep all added panel features outside finished-board copper paths and mounting/connector clearances. Confirm depaneling method and mechanical support for the tall J1/J3 terminals.
- Factory to confirm paste/stencil and reflow process for F2 and the power-device copper pads. Inspect hidden joints and plated-hole solder fill. Supply F1 blade fuse separately and insert after soldering.
- Prototype only. Continuous/burst ampacity and fault interruption of the assembled board are not qualified.
