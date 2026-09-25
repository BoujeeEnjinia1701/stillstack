---
doc_id: SSK-REQ-001
title: StillStack requirements
project: StillStack
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Add TRL 3 status from SSK-CAL-001; record decisions from SSK-DDR-001 (budget kept at $250, tilt stand, aperture); targets unchanged
---

# StillStack requirements

These requirements were checked by calculation at TRL 3 in SSK-CAL-001. Two are **not met** (R8 dry stagnation and R12 cost), five are at risk and one cannot be verified until TRL 4. No target has been relaxed: the TRL 2 review decisions (SSK-DDR-001, decided by Amish on 2026-09-25) kept the 1 m2 aperture, the 20 deg tilt on an adjustable stand and the $250 budget, with no redefinition of what the budget covers. Changes to R8 or R12 are proposed, awaiting Amish, in docs/REVIEW.md.

Table 1. Requirements and status at TRL 3.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (SSK-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Produce more distillate per unit area than a basin still | 10 L per m2 of aperture per day or more on a clear day with 5.5 kWh per m2 of sun (design goal 13 L) | Stage energy balance calculation; later outdoor test with a single-basin still alongside | Met on paper: 10.6 L after warm-up deduction (11.3 L quasi-steady); the 13 L goal is not met |
| R2 | Reuse the latent heat of condensation | Daily gained output ratio (latent heat in distillate divided by solar input) of 1.3 or more | Stage energy balance calculation | At risk: 1.34 quasi-steady, 1.26 after warm-up deduction |
| R3 | Remove salt | Distillate conductivity 75 µS/cm or less (about 50 mg/L dissolved solids) from feed up to 40 g/L salinity | Calculation of carryover paths; later conductivity meter | Not verifiable at TRL 3: brine carryover must stay below 0.075 % of the distillate (8.6 mL per day) |
| R4 | Keep brine and distillate apart | A physical air break of 10 mm or more between every wick edge and every distillate channel; no shared drain | Design review of the model | At risk: 10 mm dry breaks at ribs and rails and 20 mm at the low edge are modeled; the brine exit over the lidded distillate manifold is not yet detailed |
| R5 | Run without power | No pumps, electronics or batteries; gravity feed from a user-filled container at most 1.5 m above ground | Design review | Met: fully passive; feed trough top at most 1.06 m (at 35 deg) |
| R6 | Accept real feed water | Seawater or brackish water up to 40 g/L salinity after cloth or 20 µm prefiltering; feed-to-distillate ratio 2.5 or more so salt stays in solution | Salt balance calculation | At risk: brine at 66.7 g/L is well below saturation, but the wick needs a permeability of 3.0 x 10^-11 m2 or more to carry the feed, which is not yet known |
| R7 | Food-safe wetted parts | Every surface that touches distillate is food-contact rated (for example 316 stainless steel, food-grade coated aluminum, PP, HDPE or NSF/ANSI 51 or 61 silicone) | Material list review | At risk: coated aluminum is decided, but no coating product rated for wet, salty service at 80 °C is selected |
| R8 | Survive dry stagnation | No damage after an empty-wick day at 1,000 W/m2 and 35 °C ambient; all internal materials rated to 110 °C or more | Stagnation temperature calculation; material datasheets | Not met: stage 1 reaches about 140 °C (144 °C in calm air), above the 110 °C rating; ASA is excluded from stages 1 to 3 |
| R9 | Household scale and portable | 1.0 m2 aperture; panel mass 20 kg or less dry; carried by two people; footprint within 1.3 x 1.3 m | Massing model and mass estimate | Met: 15.9 kg dry (19.9 kg wet); footprint 1.28 x 1.16 m at 10 deg |
| R10 | Easy maintenance | Wicks removable, rinsed and refitted by one person without special tools in 30 min or less; salt flushing no more often than once a week | Design review | At risk: wicks are bonded under the plates and the removal method is not defined |
| R11 | Adjustable tilt | Tilt between 10 and 35 deg to suit latitudes of about 0 to 35 deg | Model check | Met: stand with rear struts of 0.53 to 0.94 m; model built at 10, 20 and 35 deg |
| R12 | Low cost and buildable | Parts cost $250 or less for the 1 m2 prototype; hand tools, sheet metal shears and a 3D printer only | Priced BOM | Not met: $317.20, $67.20 over budget |

## Assumptions

- Design day: 5.5 kWh per m2 per day (19.8 MJ per m2) on the tilted aperture, 30 °C mean daytime ambient, light wind (1 m/s in SSK-CAL-001).
- Latent heat of vaporization: SSK-CAL-001 uses temperature-dependent values (about 2.33 to 2.36 MJ per kg over the stage range) in place of the flat 2.26 MJ per kg used at TRL 2.
- The WHO does not set a health-based limit for dissolved solids; 50 mg/L is chosen as a check that salt carryover is negligible, not as a potability limit.
- Household need of about 3 L per person per day for drinking and 2 L for cooking, so 10 to 11 L per day serves a household of two.
