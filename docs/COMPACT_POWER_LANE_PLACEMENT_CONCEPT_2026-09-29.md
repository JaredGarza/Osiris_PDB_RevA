# Compact power-lane placement concept — 29 September 2026

**Placement study only.** The routed board remains unchanged. This sketch is
not a fitted KiCad placement, current-capacity calculation, or fabrication
release.

## Connector finding

The board-mount AMASS [XT60PW-M](https://www.china-amass.net/xt60pw-m-product/)
and [XT60PW-F](https://www.china-amass.net/xt60pw-f-product/) used in the
current candidate are each rated 35 A at up to 85 K temperature rise.
AMASS also lists [XT60H-F](https://www.china-amass.net/xt60h-f-product/) at
35 A with 12 AWG wire. I found no manufacturer-qualified board-mount XT60
variant that establishes 60 A continuous and 100 A for 30 seconds. Even a
hypothetical 60 A connector would leave no input margin at J1, which must
carry the ESC branch plus avionics. Keep all three connector *positions* in
this study, but select a higher-rated power interface before electrical
release if the 60/100 A target is retained.

## Preferred top-view arrangement

```text
                  common power-cable exit edge
    ┌─────────────────────────────────────────────────────┐
    │  J1 BAT XT60       J3 ESC XT60                      │
    │   +  -               +  -                           │
    │       F2       D5 / C17 / C18 / C19                │
    │   ═════════════ wide positive-and-return lane ═══  │
    │                                                     │
    │ F1 → Q3 → U1/Q1/Q2 → R5 → J4 AVIONICS XT60         │
    │                              J2 I²C                 │
    └─────────────────────────────────────────────────────┘
                avionics and data cable exit
```

The diagram indicates placement and current flow; it does not prescribe
physical pin order or copper width. Confirm both mated cable polarities
before orienting the footprints.

1. Put J1 and J3 on one straight edge, with F2 directly between their
   positive pins on the inside of the board. Avoid the present route from
   J1 up to the shelf-mounted F2 and back down to J3. The existing footprint
   centers are J1 `(31.15, 33.85)`, F2 `(40, -4)`, and J3 `(92.25, 34.75)`
   mm, so the fuse is nearly 39 mm above the two connectors. A direct lane
   is geometrically shorter and removes the need for the upper power shelf.
2. Place D5 and C17–C19 immediately inboard of J3, between its positive
   and return contacts. At present they are on the shelf roughly 39 mm
   above J3. The new position gives the ESC clamp and bypass parts a short
   local loop. Keep their connections out of the narrow fuse-to-J3 path.
3. Reserve a clear power corridor for **both** battery positive and return.
   Keep mounting holes, avionics traces, and thin plane necks out of it.
   The positive path still crosses F2, so its land pattern and joints are
   part of the current path. Avoid making a few small vias the only return
   between J3 and J1.
4. Take the lower-current avionics branch from J1 near the input, then lay
   out F1, Q3, U1/Q1/Q2, R5, and J4 in their electrical order in the lower
   region. Keep the shunt's Kelvin sense traces away from the ESC lane. Put
   J2 beside J4 so the Osiris power and I²C harnesses leave together.
5. Fit the four mounting holes outside the power corridor and preserve tool
   access to F1/F2. Check the mated connector bodies, cable bend radius,
   frame holes, and capacitor height before setting a final outline. A
   rectangular outline without the current upper shelf is the starting
   shape, but no smaller dimensions are claimed until a footprint fit.

This arrangement reduces the geometric detour and separates the noisy ESC
path from telemetry. It cannot solve the connector, fuse, or copper ratings
by placement alone. The present 1 oz, two-layer stackup needs a thermal and
fault-current design review before it can be used at 60/100 A.
