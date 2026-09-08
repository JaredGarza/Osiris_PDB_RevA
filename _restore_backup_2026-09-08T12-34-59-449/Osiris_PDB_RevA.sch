EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:Connector
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Osiris 4S Power Distribution Board"
Date "2026-09-03"
Rev "A-PROTOTYPE"
Comp "Osiris UAV"
Comment1 "4S input, four external ESC branches, fused raw-4S Osiris output"
Comment2 "Prototype ratings require bench, transient, and thermal validation"
Comment3 "Four-layer 2 oz copper target"
Comment4 "Do not connect a LiPo before current-limited bench bring-up"
$EndDescr
Text Notes 900 900 0    100  ~ 20
4S BATTERY AND MOTOR BUS
Text Notes 5900 3900 0    100  ~ 20
SEPARATELY PROTECTED OSIRIS BRANCH
$Comp
L Connector:Screw_Terminal_01x02 J1
U 1 1 68000001
P 2100 1450
F 0 "J1" H 2180 1442 50  0000 L CNN
F 1 "BATTERY_IN_4S" H 2180 1351 50 0000 L CNN
F 2 "Connector_Wire:SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm" H 2100 1450 50 0001 C CNN
F 3 "" H 2100 1450 50 0001 C CNN
	1    2100 1450
	1    0    0    -1
$EndComp
Wire Wire Line
	1900 1450 1450 1450
Text Label 1450 1450 0    50   ~ 0
VBAT
Wire Wire Line
	1900 1550 1450 1550
Text Label 1450 1550 0    50   ~ 0
GND
$Comp
L Connector:Screw_Terminal_01x02 J2
U 1 1 68000002
P 5200 1300
F 0 "J2" H 5280 1292 50 0000 L CNN
F 1 "ESC1_OUT" H 5280 1201 50 0000 L CNN
F 2 "Connector_Wire:SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm" H 5200 1300 50 0001 C CNN
F 3 "" H 5200 1300 50 0001 C CNN
	1    5200 1300
	1    0    0    -1
$EndComp
Wire Wire Line
	5000 1300 4550 1300
Text Label 4550 1300 0    50   ~ 0
VBAT
Wire Wire Line
	5000 1400 4550 1400
Text Label 4550 1400 0    50   ~ 0
GND
$Comp
L Connector:Screw_Terminal_01x02 J3
U 1 1 68000003
P 5200 1950
F 0 "J3" H 5280 1942 50 0000 L CNN
F 1 "ESC2_OUT" H 5280 1851 50 0000 L CNN
F 2 "Connector_Wire:SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm" H 5200 1950 50 0001 C CNN
F 3 "" H 5200 1950 50 0001 C CNN
	1    5200 1950
	1    0    0    -1
$EndComp
Wire Wire Line
	5000 1950 4550 1950
Text Label 4550 1950 0    50   ~ 0
VBAT
Wire Wire Line
	5000 2050 4550 2050
Text Label 4550 2050 0    50   ~ 0
GND
$Comp
L Connector:Screw_Terminal_01x02 J4
U 1 1 68000004
P 7300 1300
F 0 "J4" H 7380 1292 50 0000 L CNN
F 1 "ESC3_OUT" H 7380 1201 50 0000 L CNN
F 2 "Connector_Wire:SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm" H 7300 1300 50 0001 C CNN
F 3 "" H 7300 1300 50 0001 C CNN
	1    7300 1300
	1    0    0    -1
$EndComp
Wire Wire Line
	7100 1300 6650 1300
Text Label 6650 1300 0    50   ~ 0
VBAT
Wire Wire Line
	7100 1400 6650 1400
Text Label 6650 1400 0    50   ~ 0
GND
$Comp
L Connector:Screw_Terminal_01x02 J5
U 1 1 68000005
P 7300 1950
F 0 "J5" H 7380 1942 50 0000 L CNN
F 1 "ESC4_OUT" H 7380 1851 50 0000 L CNN
F 2 "Connector_Wire:SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm" H 7300 1950 50 0001 C CNN
F 3 "" H 7300 1950 50 0001 C CNN
	1    7300 1950
	1    0    0    -1
$EndComp
Wire Wire Line
	7100 1950 6650 1950
Text Label 6650 1950 0    50   ~ 0
VBAT
Wire Wire Line
	7100 2050 6650 2050
Text Label 6650 2050 0    50   ~ 0
GND
$Comp
L Device:D_TVS D1
U 1 1 68000006
P 2200 2800
F 0 "D1" V 2154 2880 50 0000 L CNN
F 1 "SMCJ17CA" V 2245 2880 50 0000 L CNN
F 2 "Diode_SMD:D_SMC" H 2200 2800 50 0001 C CNN
F 3 "https://www.littelfuse.com/assetdocs/tvs-diodes-smcj-datasheet" H 2200 2800 50 0001 C CNN
	1    2200 2800
	0    1    1    0
$EndComp
Wire Wire Line
	2200 2650 2200 2450
Text Label 2200 2450 1    50   ~ 0
VBAT
Wire Wire Line
	2200 2950 2200 3150
Text Label 2200 3150 3    50   ~ 0
GND
$Comp
L Device:C_Polarized C1
U 1 1 68000007
P 3100 2800
F 0 "C1" H 3218 2846 50 0000 L CNN
F 1 "1000uF 35V LOW-ESR" H 3218 2755 50 0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D12.5mm_P5.00mm" H 3138 2650 50 0001 C CNN
F 3 "https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFR1V102" H 3100 2800 50 0001 C CNN
	1    3100 2800
	1    0    0    -1
$EndComp
Wire Wire Line
	3100 2650 3100 2450
Text Label 3100 2450 1    50   ~ 0
VBAT
Wire Wire Line
	3100 2950 3100 3150
Text Label 3100 3150 3    50   ~ 0
GND
$Comp
L Device:C C2
U 1 1 68000008
P 4400 2800
F 0 "C2" H 4515 2846 50 0000 L CNN
F 1 "100nF 50V X7R" H 4515 2755 50 0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 4438 2650 50 0001 C CNN
F 3 "" H 4400 2800 50 0001 C CNN
	1    4400 2800
	1    0    0    -1
$EndComp
Wire Wire Line
	4400 2650 4400 2450
Text Label 4400 2450 1    50   ~ 0
VBAT
Wire Wire Line
	4400 2950 4400 3150
Text Label 4400 3150 3    50   ~ 0
GND
$Comp
L Device:Fuse F1
U 1 1 68000009
P 6900 4500
F 0 "F1" V 6703 4500 50 0000 C CNN
F 1 "0678H6300-02 6.3A" V 6794 4500 50 0000 C CNN
F 2 "Osiris_PDB:FUSC9830X318N" V 6830 4500 50 0001 C CNN
F 3 "https://www.belfuse.com/products/circuit-protection/fuses/0678h6300-02" H 6900 4500 50 0001 C CNN
	1    6900 4500
	0    1    1    0
$EndComp
Wire Wire Line
	6750 4500 6250 4500
Text Label 6250 4500 0    50   ~ 0
VBAT
Wire Wire Line
	7050 4500 7550 4500
Text Label 7550 4500 2    50   ~ 0
OSIRIS_FUSED
$Comp
L Connector:Screw_Terminal_01x02 J6
U 1 1 6800000A
P 9400 4500
F 0 "J6" H 9480 4492 50 0000 L CNN
F 1 "OSIRIS_OUT_XT60_M_PIGTAIL" H 9480 4401 50 0000 L CNN
F 2 "Connector_Wire:SolderWire-2sqmm_1x02_P7.8mm_D2mm_OD3.9mm" H 9400 4500 50 0001 C CNN
F 3 "" H 9400 4500 50 0001 C CNN
	1    9400 4500
	1    0    0    -1
$EndComp
Wire Wire Line
	9200 4500 8600 4500
Text Label 8600 4500 0    50   ~ 0
OSIRIS_FUSED
Wire Wire Line
	9200 4600 8600 4600
Text Label 8600 4600 0    50   ~ 0
GND
$Comp
L Device:D_TVS D2
U 1 1 6800000B
P 6500 5550
F 0 "D2" V 6454 5630 50 0000 L CNN
F 1 "SMCJ17CA" V 6545 5630 50 0000 L CNN
F 2 "Diode_SMD:D_SMC" H 6500 5550 50 0001 C CNN
F 3 "https://www.littelfuse.com/assetdocs/tvs-diodes-smcj-datasheet" H 6500 5550 50 0001 C CNN
	1    6500 5550
	0    1    1    0
$EndComp
Wire Wire Line
	6500 5400 6500 5200
Text Label 6500 5200 1    50   ~ 0
OSIRIS_FUSED
Wire Wire Line
	6500 5700 6500 5900
Text Label 6500 5900 3    50   ~ 0
GND
$Comp
L Device:C C3
U 1 1 6800000C
P 7400 5550
F 0 "C3" H 7515 5596 50 0000 L CNN
F 1 "1uF 50V X7R" H 7515 5505 50 0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 7438 5400 50 0001 C CNN
F 3 "https://search.kemet.com/component-documentation/download/specsheet/C0805C105K5RACAUTO" H 7400 5550 50 0001 C CNN
	1    7400 5550
	1    0    0    -1
$EndComp
Wire Wire Line
	7400 5400 7400 5200
Text Label 7400 5200 1    50   ~ 0
OSIRIS_FUSED
Wire Wire Line
	7400 5700 7400 5900
Text Label 7400 5900 3    50   ~ 0
GND
$Comp
L Device:C C4
U 1 1 6800000D
P 8300 5550
F 0 "C4" H 8415 5596 50 0000 L CNN
F 1 "100nF 50V X7R" H 8415 5505 50 0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 8338 5400 50 0001 C CNN
F 3 "" H 8300 5550 50 0001 C CNN
	1    8300 5550
	1    0    0    -1
$EndComp
Wire Wire Line
	8300 5400 8300 5200
Text Label 8300 5200 1    50   ~ 0
OSIRIS_FUSED
Wire Wire Line
	8300 5700 8300 5900
Text Label 8300 5900 3    50   ~ 0
GND
$Comp
L Device:C_Polarized C5
U 1 1 6800000E
P 9300 5550
F 0 "C5" H 9418 5596 50 0000 L CNN
F 1 "100uF 35V DNP" H 9418 5505 50 0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm" H 9338 5400 50 0001 C CNN
F 3 "" H 9300 5550 50 0001 C CNN
	1    9300 5550
	1    0    0    -1
$EndComp
Wire Wire Line
	9300 5400 9300 5200
Text Label 9300 5200 1    50   ~ 0
OSIRIS_FUSED
Wire Wire Line
	9300 5700 9300 5900
Text Label 9300 5900 3    50   ~ 0
GND
Text Notes 6100 6300 0    60   ~ 0
C5 is initially DNP. Fit only after hot-plug/transient measurements.
Text Notes 1150 3550 0    60   ~ 0
D1/C1 must be mounted close to the battery/ESC star region.
Text Notes 1150 3750 0    60   ~ 0
Main aircraft fuse is external for the prototype.
$EndSCHEMATC

