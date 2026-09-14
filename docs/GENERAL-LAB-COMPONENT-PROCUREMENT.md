# General lab component procurement plan

## 1 / Shared lab stocking strategy

Purchase proposal | September 14, 2026 | For September 15 discussion. Scope: general embedded electronics and avionics prototyping across multiple projects, plus a separate PDB project kit. Quantities below are recommended initial stock targets, not an assumed board count or an approved purchase order.

| Priority | What to stock | Starting policy |
|---|---|---|
| P1 - core stock | Frequently reused passives, indicator LEDs, small transistors, common logic and analog ICs, basic connectors. | Order after Ryan's inventory and machine/carrier check. Keep stocked through reorder thresholds. |
| P2 - expand on demand | CAN/RS-485, memory, MCUs, selected regulators, precision analog and uncommon passive values. | Small quantities once the lab chooses a preferred family; expand when recurring designs use it. |
| Project kits | PDB protection controller, power MOSFETs, shunt, fuse and other board-specific selections. | Reserve by BOM and build batch. Do not count committed project stock as freely available lab stock. |
| Equipment and process | Feeders, nozzles, dry/ESD storage, paste, stencil printing, reflow, inspection and harness tooling. | Confirm what comes with the machine and what the lab already owns before quoting gaps. |

### Package standard

Proposed default for NEW general-purpose designs: 0603 EIA passives. Keep an 0402 satellite stock for compact Osiris work once the machine is confirmed capable. Keep 0805/1206 where power, capacitance or voltage requires them. This policy does not change any existing PCB footprint.

### Ryan's books

Inventory the books by value, package, rating, quantity, MPN and carrier. Keep assorted values for tuning and hand rework. Count them as machine stock only if identifiable and feedable. A book does not by itself replace continuous tape/reels.

### What makes this save time

Use a shared approved-parts library with stock IDs, footprints, datasheets and known carrier settings. Design new boards around these parts when electrically appropriate; reuse validated circuit blocks. Avoid a different regulator, connector and package on every project.

### Quantity interpretation

Targets are PER value, color, voltage option or selected IC variant unless stated otherwise. Subtract verified usable stock. Allow separate feeder setup/repair stock. Prices, supplier stock, factory reel quantities and packaging fees need quotes; no spend total is claimed.

## 2 / Passives: the reel inventory

P1 means the first stocking wave. Prefer one approved manufacturer part per value/specification/package. Full reels suit sustained demand; custom reels provide smaller machine-ready stock. No automatic substitution into the PDB or Osiris is implied.

| Priority / group | Values and minimum selection criteria | Target per variant |
|---|---|---|
| P1 / resistors, 0603 | 0 ohm jumpers; 100 ohm, 330 ohm, 1 k, 4.7 k, 10 k, 100 k. 1% for nonzero values; at least 0.1 W nominal with application derating. | 1,000 each; quote one factory reel as alternative |
| P1 / resistors, 0603 | 10, 22, 33, 47, 49.9, 220, 470 ohm; 2.2 k, 3.3 k, 6.8 k, 22 k, 47 k, 1 M. Same 1% class. | 250 each |
| P1 / ceramic caps, 0603 | 100 nF, X7R, >=25 V, 10%; 1 uF, X7R, >=16 V, 10%. Choose exact MPN after bias/rating review. | 2,000 of 100 nF; 1,000 of 1 uF |
| P1 / ceramic caps, 0603 | 1 nF and 10 nF, X7R, >=50 V, 10%. | 250 each |
| P1 / bulk ceramic caps | 4.7 uF and 10 uF, X7R, >=16 V, 0805. Verify effective capacitance at working voltage. | 250 each |
| P2 / signal capacitors | 22 pF, 47 pF, 100 pF, 1 nF, C0G, >=50 V, 0603; tolerance selected for the application. Crystal load values are circuit-specific. | 100 each |
| P2 / compact 0402 stock | 0 ohm, 1 k, 4.7 k, 10 k, 100 k; 100 nF X7R >=16 V. Exact ratings and MPNs reviewed separately. | 500 each resistor; 1,000 caps; after machine check |
| P2 / larger power passives | PDB 0805/1206 parts use the exact frozen order list. General bulk caps, shunts and precision dividers selected per power circuit. | Project quantities; promote proven repeat parts later |
| P2 / ferrites and inductors | Start a small evaluation assortment; choose ferrite impedance curve/DC current/DCR and inductor inductance/saturation/RMS current/footprint together. | 10-25 per selected MPN; no generic inductor reel buy |

### Avoid unnecessary breadth

Do not buy full reels of every E-series value. Ryan's books can cover experiments; machine-ready stock should favor repeat values. The targets above establish useful depth without claiming every item is already shared across project BOMs.

### Reel quotation

Ask for target quantity on a custom reel AND factory reel total price, including reeling fees, minimum packs and available continuous length. Final manufacturer part numbers and carrier dimensions must appear on the order.

## 3 / Common ICs: a reusable shelf

These are function/family recommendations checked against manufacturer product pages. Family names are NOT complete order codes. Select one package and full ordering suffix per row before purchase; maintain it in the lab CAD library. Start with small custom reels or supported continuous cut tape.

| Priority / function | Candidate family and selection boundary | Target |
|---|---|---|
| P1 / 3.3 V and 1.8 V LDO | TI TLV755P: select fixed output and SOT-23-5 variant. Low-voltage local rail use; 5.5 V maximum input, NOT a direct 4S battery regulator. | 50 of 3.3 V; 25 of 1.8 V |
| P1 / dual op amp | TI TLV9002: general low-voltage signal conditioning. Prefer SOIC-8 for initial shared library if board area permits. Review input/output range and bandwidth per use. | 25 |
| P1 / comparator | TI TLV3201: threshold detection. Choose exact package, verify supply/input range and add designed hysteresis where required. | 25 |
| P1 / Schmitt inverter | TI SN74LVC1G14: signal cleanup / logic inversion; select SOT-23 variant and verify logic thresholds. | 50 |
| P1 / tri-state buffer | TI SN74LVC1G125: controlled signal buffering. Select SOT-23 variant; check enable and power-off behavior. | 50 |
| P1 / direction-controlled translator | TI SN74LVC1T45: push-pull digital level translation. Not a universal bidirectional I2C translator. | 25 |
| P1 / load switch | TI TPS22918: local low-voltage rail switching, up to 5.5 V input. This is not a 4S battery protector or a current-limiting eFuse. | 25 |
| P2 / current-sense amplifier | TI INA180: analog current measurement. Choose gain/package and common-mode range for the circuit. PDB INA228 remains a separate exact BOM part. | 25 of one gain variant |
| P2 / CAN transceiver | TI TCAN332: candidate for 3.3 V CAN designs. Select exact variant/package against required bus mode and protection. | 20 if CAN is a recurring lab interface |
| P2 / platform-dependent ICs | Choose ONE familiar MCU platform plus supported programmer; then matching flash/EEPROM, RS-485, I2C translator, reset supervisor and USB-UART parts as projects require. | 10-20 per selected MPN; buy after platform review |
| P2 / switching power | Choose a small number of validated buck-regulator circuits with matching inductors, caps and layout. New Rev B power design is not yet selected. | 10-20 matched circuit kits after design selection |

### Design once, reuse

For each stocked IC: store symbol, footprint, pin mapping, decoupling requirements and a tested example circuit. Order by complete manufacturer code, not just a familiar name; gain, voltage, pinout and packaging variants matter.

### Upgrade to larger reels

When repeated builds establish demand, increase the selected IC stock target. Keep expensive/specialized devices at small quantities until recurring consumption justifies more.

## 4 / Discretes, connectors and tools

This list fills common gaps that delay a build even when its ICs are in stock. Quantities are proposed shared-stock targets. Exact device ratings, mechanical drawings and packaging must be selected before ordering.

| Priority / category | What to request | Target |
|---|---|---|
| P1 / indicator LEDs | Red, green, blue; 0603, identified polarity and brightness/current specification. | 250 per color |
| P1 / small transistors | One NPN and one PNP switching transistor in SOT-23; one small logic-level N-MOSFET and one P-MOSFET. Verify pinout and MOSFET RDS(on) at actual gate voltage. | 100 per selected MPN |
| P1 / diodes | One fast small-signal diode and one small Schottky in chosen standard packages. Size power Schottky, TVS and ESD arrays separately for their circuits. | 100 per small diode MPN |
| P2 / interface protection | One selected low-capacitance ESD array for the actual interface voltage and speed; TVS parts selected for the power bus. | 25-50 per selected MPN |
| P1 / simple interconnect | 2.54 mm breakaway male/female headers and jumpers; test points and chosen small tactile switch. Headers generally hand/through-hole assembly. | 25 header strips per type; 100 jumpers; 100 test points; 50 switches |
| P1 / harness standard | Choose one locking wire-to-board family. JST GH is a candidate already used in PDB references. Start with 2/3/4/6-position board connectors, matching housings and contacts. | 25 per chosen connector/housing variant; 500 contacts |
| P2 / project connectors | Power connectors, USB, SWD/programming connector and RF connectors must match mechanical plans. Quote board connector AND mating cable/housing. | 10-25 per selected variant |
| P1 / feeder readiness | Compatible feeders, nozzles, cut-tape fixtures if supported, splice/leader supplies, reel storage and durable labels. Width/pitch and slots from selected machine. | Quote machine-specific kit; do not assume counts |
| P1 / assembly process | Paste compatible with process; stencil printing/support, reflow oven/profile measurement, microscope, solder/rework tools, tweezers and flux/cleaning supplies. | Inventory equipment; buy gaps and consumables |
| P1 / handling and harness work | ESD work area, component storage per moisture requirements, stock bins, wire, heat-shrink, matched crimper and extraction tools. | One shared setup; replenish consumables |

### Do not buy short-lived supplies in bulk

Buy solder paste to the near-term assembly schedule and manufacturer storage/shelf-life requirements. Stencils are specific to released PCB/panel layouts.

### Machine-ready does not mean machine-only

Many headers and power connectors need hand or through-hole assembly. Reserve a separate work step and tools; verify actual machine capabilities for any nonstandard carrier.

## 5 / Purchasing and replenishment

The aim is to keep recurring builds moving. A shared inventory plus standard parts and repeatable feeder setups will save more time than an untracked assortment of reels.

| Step / owner to assign | Deliverable | Completion gate |
|---|---|---|
| 1 / Lab inventory owner | Count Ryan's books, reels, connectors and equipment; identify unknown parts and reserved project stock. | Usable free stock known per exact MPN/package/carrier. |
| 2 / Machine owner | Document supported feeders, reel sizes, nozzles, smallest packages and supplied accessories. | Stock packaging and equipment quote match the machine. |
| 3 / Hardware lead | Approve package defaults and full MPNs for P1 groups. Use the family shortlist on page 3; resolve exact variants. | Each order line has a complete code/spec, datasheet and footprint. |
| 4 / Purchasing | Quote P1 first; quote P2 separately. Compare custom versus factory reels on TOTAL price and availability. | Budget-approved quantities net of stock and reservations. |
| 5 / Receiving / assembly | Label MPN, value, package, lot, quantity, location, moisture status and carrier; verify identity before stocking. | Trial loading and a first-article board establish feeder/vision/reflow settings. |
| 6 / All designers | Use approved stock parts in new designs where appropriate; reserve material at design release. | No unrecorded borrowing from project kits. |

### Starter reorder rule

Until usage data exists, review weekly and flag core passives at 25% of target or below; flag core ICs at 10 units or below. Reorder to target after subtracting open purchase orders. These are provisional rules, not measured consumption forecasts.

### Once consumption is known

Reorder point = expected use during supplier lead time + safety stock. Available stock = on-hand usable stock minus project reservations. Include setup losses in consumption and increase safety stock for long or variable lead times.

### Tomorrow's boss request

Approve a shared P1 stock budget separate from project BOM purchases, assign the inventory/machine owners, and authorize distributor quotes. P2 expands after lab platform choices. The existing 27-code PDB list remains a separate procurement attachment.

### Sources / checked September 14, 2026

Manufacturer families: https://www.ti.com/product/TLV755P ; /TLV9002 ; /TLV3201 ; /SN74LVC1G14 ; /SN74LVC1G125 ; /SN74LVC1T45 ; /TPS22918 ; /INA180 ; /TCAN332 (all on www.ti.com/product/). Packaging: https://www.digikey.com/en/resources/product-services and https://forum.digikey.com/t/details-about-digi-reels/1303 . Stock quantities and priorities are planning recommendations, not manufacturer guidance.
