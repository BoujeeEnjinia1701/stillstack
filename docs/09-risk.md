---
doc_id: SSK-RSK-001
title: StillStack risk register and hazard analysis
project: StillStack
doc_type: Risk register and hazard analysis
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First risk register, preliminary hazard analysis and design FMEA (kit 1.9.1 upgrade)
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Amish''s decisions of 2026-10-25: P7 and F11 with 5052 aluminium clips (D-08; F11 occurrence 3 to 1, RPN 48 to 16); P6 and F4 coupon test (D-04); H3 anchoring a hold point (D-09)'
---

# StillStack risk register and hazard analysis

The top risks are brine reaching the distillate (a health hazard if the water is drunk untested), a dry panel in full sun (burns and damage at about 142 °C), and a wick fabric that cannot carry the feed (output well below PR-001). Each has a control in the design and a pass condition or test planned for TRL 4. Method: STANDARDS section 23. Likelihood, impact, severity, occurrence and detection are scored 1 (low) to 5 (high; for detection, 5 means hardest to detect).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Wick fabric too tight to carry the feed | Permeability below 3.0e-11 m2 (SSK-CAL-001 section 6) | Dry patches, output below PR-001, local stagnation | 3 | 4 | Design lead | Wicking-rise test of the two shortlisted fabrics before purchase (SSK-DEC-001, 2026-10-02) |
| P2 | No certified food-contact coating found | Coaters may not certify hot salty distillate at 150 °C dry | PR-007 not met; plates 1 and 2 move to 316 stainless (cost up) | 3 | 3 | Design lead | Rule of 2026-10-02: lowest-cost certified coating, else 316 stainless for plates 1 and 2 |
| P3 | Cost stays over the value-engineering target | Coated plates and PPS rails | USD 105.70 over; harder for NGOs to fund | 4 | 2 | Design lead | Savings in SSK-DEC-001 (nested blanks, folded trim, reclaimed timber); report against the target |
| P4 | Concept selection stays open | Options A and B within 10 % (SSK-OPT-001) | Effort spent on the wrong option | 2 | 3 | Amish | Decision D-03 requested |
| P5 | No partner lab agrees to test | Partner not yet approached | TRL 4 delayed | 3 | 3 | Amish | First candidate named (Politecnico di Torino); a coastal NGO later |
| P7 | Stainless clips corrode the plates | Galvanic couple of 304 and aluminium in hot brine (STEM S30) | Pitting at the clips; brine path to the distillate face | 3 | 4 | Design lead | 5052 aluminium clips (D-08, decided by Amish 2026-10-25) |
| P6 | Crevice corrosion perforates a plate | Bare aluminium under wet wicks and clips in 60 to 80 °C brine | Brine path to the distillate face; plate replacement | 2 | 4 | Design lead | Coupon test at TRL 4, 1050 preferred (D-04, decided by Amish 2026-10-25); 5052 as the fallback alloy |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Contaminated distillate drunk | Brine carryover, microbes below pasteurization, volatile organics in the feed | Illness | 5 | 3 | Separate distillate and brine tongues with 10 mm air breaks, lip tabs, labelled outlets (PR-004); test conductivity and E. coli and disinfect before drinking (PRC safety); per-stage conductivity pass condition at TRL 4 | 5 x 2: acceptable only with the testing rule in the instructions |
| H2 | Hot surfaces | Absorber near 80 °C in use and 142 °C when dry (SSK-CAL-001 section 5) | Burns | 3 | 3 | Stagnation cover (BOM 14); never open the stack in sun; shade rule; trim and glazing kept on | 3 x 2 |
| H3 | Panel tips over in wind | Unanchored, it tips at about 16.5 m/s of wind from behind; PR-013 is stated for the anchored stand (D-09) | Crush or cut injuries; broken glazing | 4 | 3 | Four ground stakes or 40 kg of ballast as a hold point before filling and before the panel faces the sun (BLD safety stops S4, S5; D-09, decided by Amish 2026-10-25); 28.8 m/s with the ballast | 4 x 1 anchored |
| H4 | Material damage at dry stagnation | Feed runs out on a sunny day | Softened rails, scorched wick, leaking stack | 2 | 3 | Ratings above stagnation in stages 1 to 3 (PPS since D-01), cover rule | 2 x 2 |
| H5 | Brine discharge | Brine at 58 to 67 g/L | Salinised soil or wells | 2 | 3 | Discharge away from crops and wells (PRC safety; G10) | 2 x 2 |
| H6 | Cuts during the build | 0.5 mm aluminium sheet edges and tongues | Hand cuts | 2 | 3 | Deburr, gloves (BLD) | 2 x 2 |
| H7 | Lifting the panel onto the stand | 18.8 kg dry panel, awkward shape | Back strain, dropped panel | 2 | 2 | Two people, panel dry, cover on (BLD safety stop S4) | 2 x 1 |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Brine tongue and lid | Keep brine tails off the distillate path | Brine drips onto the lid slots | Salt in distillate (H1) | Tail sags, lid deformed | 5 | 2 | 3 | 30 | Lid slots only under distillate tongues; tails 10.5 mm clear; conductivity per stage at TRL 4 |
| F2 | Lip tabs on condensing plates | Stop feed creeping onto the condensing faces | Feed wets the condensing face at the high edge | Salt in distillate | Tabs bent wrong, wick tail touches plate | 5 | 2 | 3 | 30 | Bend before coating; check 1.5 mm clearance at assembly (model check) |
| F3 | Wick strips | Carry feed down the slope | Dry patch | Lower output, local hot spot | Low permeability, salt crust | 3 | 3 | 3 | 27 | Fabric test; weekly rinse (PR-010) |
| F4 | Plate (bare wick face) | Conduct heat, carry the wick | Crevice corrosion through 0.5 mm | Brine reaches distillate face | Hot brine crevice under wick and clips | 5 | 2 | 4 | 40 | Coupon test (D-04); inspect plates at each wick change |
| F5 | Condensing-face coating | Food-contact surface | Coating blisters or leaches | PR-007 not met | Wrong product, poor adhesion on bends | 4 | 2 | 3 | 24 | Certified product only (rule of 2026-10-02); bend before coating |
| F6 | Spacer ribs | Hold the 6 mm gap | Rib creeps, gap closes | Wick touches plate below; carryover | Silicone set under heat | 3 | 2 | 3 | 18 | Silicone rated about 200 °C; inspect gaps at wick change |
| F7 | Side rails, stage 3 | Hold the gap at the edges | Rail softens at stagnation | Gap closes at the edge | Printed PC at 110 °C (before D-01) | 3 | 1 | 2 | 6 | Closed by D-01 (PPS) |
| F8 | Glazing (inner sheet) | Transmit sunlight, keep heat in | Sheet distorts | Lower output, leaks | 115 °C at calm stagnation against a 120 °C limit | 3 | 2 | 2 | 12 | Cover rule (D-05) |
| F11 | Wick clips | Hold the wicks | Clip or plate corrodes at the contact | Brine path or loose wick | Galvanic couple with stainless clips (removed by the 5052 aluminium clips, D-08, 2026-10-25); crevice under the clip remains | 4 | 1 | 4 | 16 | 5052 aluminium clips (D-08, decided by Amish 2026-10-25); coupon test (D-04); inspect at each wick change |
| F12 | Fins and underside paint | Reject heat (emissivity 0.90, D-07) | Paint chalks or peels | Hotter stack, lower yield (about 1 L at emissivity 0.10) | UV and heat ageing | 3 | 2 | 2 | 12 | High-temperature paint as on the absorber; inspect yearly |
| F9 | Stand foot pin | Hold the tilt | Pin missing or loose | Panel drops to the stops | Pin not refitted after a tilt change | 4 | 2 | 2 | 16 | M10 x 120 pins with nuts (D-02); two-person tilt change in BLD |
| F10 | Ground stakes | Hold the stand in wind | Stake pulls out | Overturn (H3) | Soft or sandy ground | 4 | 2 | 3 | 24 | Ballast where stakes cannot hold; site check at TRL 5 |
