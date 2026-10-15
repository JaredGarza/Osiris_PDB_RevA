# INA238 and parallel ESC capacitor bank

Implemented October 15, 2026 in the current Osiris PDB schematic and PCB. This supersedes the earlier INA228/EEHZL1H331P sourcing selections.

- U2 is now Texas Instruments INA238AIDGSR, JLC C2868250. The DGS/VSSOP-10 package, pad geometry, pin functions, address 0x40 and local 3.3 V supply remain unchanged. It provides 16-bit telemetry and requires the new INA238 driver.
- C17 and new C20 are Panasonic EEHZS1H221P, JLC C385885, 220 uF / 50 V each in parallel on ESC_VBAT/GND. The bank is 440 uF nominal at 50 V.
- C17 retains its original center. C20 is at X=172.3, Y=74.8 mm, top side, KiCad rotation -90 degrees. All other existing footprint centers and rotations are unchanged. The outline remains 82.5 x 65 mm.
- Both standard-P capacitor footprints now use Panasonic's January 30, 2026 mounting dimensions: 4.1 x 2.0 mm pads, 4.6 mm gap and 8.7 mm center pitch. They are not the different vibration-proof V-package lands. See `Datasheets/Panasonic_Hybrid_Mounting_2026.pdf`, page 2.
- Positive pads connect solidly to the existing ESC power pour. Six short 0.8 mm ground-return tracks and six 0.4 mm drill / 0.8 mm diameter ground vias were added. One existing untracked ground-stitch via was moved clear of C20; C18's silkscreen reference was moved. Copper zones were refilled.

## Verification

KiCad 10.0.5 reports zero ERC violations, zero DRC violations, zero unconnected items and zero schematic/PCB parity issues. Comparing exported netlists confirms the only added pins are C20.1 on ESC_VBAT and C20.2 on GND. Existing pad positions/sizes/nets are unchanged except for C17's deliberately revised lands.

The INA238 driver and retained legacy INA228 driver passed MSVC `/W4 /WX /std:c11` tests. INA238 tests exercise two-byte data transactions, signed scaling, 5 A and 12.12 A examples, clipping, configuration loss, I/O errors, device identity and diagnostic flags. This is a portable PDB driver, not a flashed STM32 application. Integrate `Firmware/pdb_ina238.c` into the target firmware; do not use the old INA228 driver for this U2. The host's separate INA228 device remains unchanged.

The regenerated BOM and placement file contain 57 fitted parts per board, 39 grouped purchasing lines, and the added C20 placement. Eleven Gerber layers and two drill files were reopened with an independent parser; outline and four-layer copper stackup were verified. The parser reports KiCad's usual G90 drill-header placement warnings, with no failed file reads. Fresh manufacturing files are in `outputs/jlcpcb-rev1.1`.

## Ordering and costs

The updated one-sheet procurement files are `engineering/PnP.xlsx` and `engineering/JLCPCB_BOM_Stock_5_Boards.xlsx`. Five boards need five INA238 ICs and ten capacitors before JLC's actual extras. The local PnP policy orders six ICs and 100 capacitors. Its current reference parts order subtotal is $788.84, including spares; assembly and service quotes remain blank.

The replacement lines have stock in the checked JLC catalog: INA238 493; EEHZS1H221P 850. The separately checked LCSC loose-part pages report 333 and 470 respectively. Inventory snapshots are not reservations. The other JLC sourcing issues remain: four short-stock groups (C1, D1/D4, F1, U1) and four unmatched groups (D5, F2, R5, R19). This is not a complete all-in-stock assembly order.

## Physical verification still required

The component ratings support the redesign, but CAD checks do not establish installed ESC/harness transient behavior, capacitor ripple heating/current sharing, hot-plug inrush or vibration endurance. The ideal parallel-bank ESR is 6.5 mOhm at 100 kHz/20 C; the summed 7.4 Arms rating at 100 kHz/125 C depends on current sharing and thermal conditions. The bank stores 62.09 mJ at 16.8 V. Preserve the ESC manufacturer's required capacitor at the ESC terminals and the existing system current/fuse limitations.

Sources: [TI INA238](https://www.ti.com/lit/ds/symlink/ina238.pdf), [Panasonic ZS](https://industrial.panasonic.com/cdbs/www-data/pdf/RDD0000/RDD0000C1244.pdf), [Panasonic mounting](https://industrial.panasonic.com/cdbs/www-data/pdf/RDD0000/DMD0000COL4.pdf), [LCSC U2](https://www.lcsc.com/product-detail/C2868250.html), [LCSC capacitor](https://www.lcsc.com/product-detail/C385885.html). JLC inventory responses are saved in the dated replacement-review output folder.
