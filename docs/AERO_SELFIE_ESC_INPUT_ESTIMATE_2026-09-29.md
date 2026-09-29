# Representative input-current estimate for the AERO SELFIE 45 A ESC

Date: 29 September 2026. **Planning example, not a measured aircraft load or
a released PDB current rating.** The user identified the AERO SELFIE
lightweight 45 A four-in-one ESC with OneShot support and asked for nominal
motor, propeller, and battery assumptions while exact parts are unknown.

## Confirmed ESC data

The [AERO SELFIE manufacturer manual](https://cdn.shopify.com/s/files/1/0728/7321/4171/files/45A_4IN1-ESC_Manual_Book_EN-CN.pdf?v=1745301381)
identifies model `4IN1-ESC-LDO`, 6–28 V (2S–6S), **45 A continuous per motor
channel** and **55 A peak per motor channel** across four channels. It is
43.5 × 44.0 × 6.0 mm with 30.5 × 30.5 mm mounting centers. Its diagram
shows battery-positive/negative solder pads, an external capacitor, and an
XT60 male power cable. The [manufacturer product page](https://aeroselfie.myshopify.com/products/45a-4-in-1-esc-brushless-motor-speed-controller)
says the 55 A bursts last up to 30 seconds. The manual does not state a
common battery-input current rating. `45 A × 4 = 180 A` and `55 A × 4 =
220 A` are sums of **channel capabilities**, not predictions of battery
current.

## Representative 4S build used for the estimate

- Four **T-Motor F40 PRO IV 2306, 2400 KV** motors with **T5146 5-inch
  tri-blade** propellers. This is an illustrative, commercially documented
  4S combination, not a claim about the user's installed hardware. The
  [manufacturer's single-motor bench table](https://store.tmotor.com/product/f40pro-4-fpv-motor.html)
  reports supply current at each throttle point around 15.6–16.1 V.
- A nominal **4S, 1550 mAh, 100C** pack, using the
  [Tattu FunFly 4S 1550 mAh](https://genstattu.com/ta-ff-100c-1550-4s1p.html)
  only as a size/class example. Its advertised `1.55 Ah × 100C = 155 A`
  describes the pack claim; it does not qualify its XT60 plug, wiring,
  thermal rise, or our PCB for 155 A.
- **5 A additional avionics input allowance** at J1, carried forward from
  the provisional motor-branch design basis. J3 carries the ESC branch only.

| Bench throttle | One motor input | Four motors, rough J3 current | With 5 A avionics, rough J1 current |
| --- | ---: | ---: | ---: |
| 50% | 8.39 A | 34 A | 39 A |
| 60% | 12.76 A | 51 A | 56 A |
| 70% | 18.22 A | 73 A | 78 A |
| 80% | 24.74 A | 99 A | 104 A |
| 100% | 41.36 A | 165 A | 170 A |

The four-motor values multiply one static bench result by four. They are a
**scenario**, not flight averages: aircraft mass determines hover throttle,
and propeller load, battery sag, airflow, manoeuvres, motor choice, and
simultaneous throttle all change the input. Motor phase current reported by
an ESC is not automatically equal to battery DC current; this table uses
the motor test's supply-current figures rather than the ESC channel limit.

## Consequence for the PDB

The previously agreed **60 A continuous / 100 A for 30 seconds at J3**
remains a *provisional operating target*. This example is below 60 A near
50–60% bench throttle and near 100 A at 80%, while full throttle could be
considerably higher. A 45 A-per-channel ESC therefore does **not** prove
that a 60 A battery branch is adequate. Nor should the design automatically
be sized to 180/220 A without knowing the real motors and intended operating
limits. Establish a maximum battery-input envelope by measurement or an
enforceable current limit before choosing J1/J3 connectors, F2, wire, and
copper. The current AMASS XT60PW board connectors' 35 A published rating
remains below even this example's moderate J3 load.
