---
doc_id: SSK-REQ-001
title: StillStack requirements
project: StillStack
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-24'
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
---

# StillStack requirements

These are first-pass requirements for the concept. Targets are proposals for review and will be checked by calculation at TRL 3.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Produce more distillate per unit area than a basin still | 10 L per m2 of aperture per day or more on a clear day with 5.5 kWh per m2 of sun (design goal 13 L) | Stage energy balance calculation; later outdoor test with a single-basin still alongside |
| R2 | Reuse the latent heat of condensation | Daily gained output ratio (latent heat in distillate divided by solar input) of 1.3 or more | Stage energy balance calculation |
| R3 | Remove salt | Distillate conductivity 75 µS/cm or less (about 50 mg/L dissolved solids) from feed up to 40 g/L salinity | Calculation of carryover paths; later conductivity meter |
| R4 | Keep brine and distillate apart | A physical air break of 10 mm or more between every wick edge and every distillate channel; no shared drain | Design review of the model |
| R5 | Run without power | No pumps, electronics or batteries; gravity feed from a user-filled container at most 1.5 m above ground | Design review |
| R6 | Accept real feed water | Seawater or brackish water up to 40 g/L salinity after cloth or 20 µm prefiltering; feed-to-distillate ratio 2.5 or more so salt stays in solution | Salt balance calculation |
| R7 | Food-safe wetted parts | Every surface that touches distillate is food-contact rated (for example 316 stainless steel, food-grade coated aluminum, PP, HDPE or NSF/ANSI 51 or 61 silicone) | Material list review |
| R8 | Survive dry stagnation | No damage after an empty-wick day at 1,000 W/m2 and 35 °C ambient; all internal materials rated to 110 °C or more | Stagnation temperature calculation; material datasheets |
| R9 | Household scale and portable | 1.0 m2 aperture; panel mass 20 kg or less dry; carried by two people; footprint within 1.3 x 1.3 m | Massing model and mass estimate |
| R10 | Easy maintenance | Wicks removable, rinsed and refitted by one person without special tools in 30 min or less; salt flushing no more often than once a week | Design review |
| R11 | Adjustable tilt | Tilt between 10 and 35 deg to suit latitudes of about 0 to 35 deg | Model check |
| R12 | Low cost and buildable | Parts cost $250 or less for the 1 m2 prototype; hand tools, sheet metal shears and a 3D printer only | Priced BOM |

## Assumptions

- Design day: 5.5 kWh per m2 per day (19.8 MJ per m2) on the tilted aperture, 30 °C mean daytime ambient, light wind.
- Latent heat of vaporization taken as 2.26 MJ per kg for first-order estimates (the true value at 40 to 70 °C is about 2.33 to 2.41 MJ per kg, which makes the estimates slightly optimistic).
- The WHO does not set a health-based limit for dissolved solids; 50 mg/L is chosen as a check that salt carryover is negligible, not as a potability limit.
- Household need of about 3 L per person per day for drinking and 2 L for cooking, so 13 L per day serves a household of two or three.
