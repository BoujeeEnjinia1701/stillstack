---
doc_id: SSK-PRC-001
title: StillStack design precis
project: StillStack
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, design choices, safety, media)
---

# StillStack design precis

StillStack is a tilted, glazed panel of 1 m2 containing four thin evaporation stages stacked like a sandwich: each stage is a wet cloth wick under a metal plate, a 6 mm vapor gap, and the next plate below. Sunlight heats the top plate, and the heat released when vapor condenses on each plate evaporates water from the wick under it, so the same solar energy is used four times. First-order numbers suggest about 13 L of distillate per m2 per day on a 5.5 kWh per m2 day, roughly three times a single-basin still, for about $240 in parts.

![Hero render](../media/hero.png)

## How it works

1. **Collect.** Sunlight passes through twin-wall polycarbonate glazing and is absorbed by a black-coated aluminum plate. A 25 mm air gap under the glazing limits heat loss from the top.
2. **Evaporate, stage 1.** A cloth wick bonded to the underside of the absorber is kept wet with feed water. Heat conducts through the plate and evaporates water from the wick.
3. **Condense and reuse.** The vapor crosses a 6 mm gap and condenses on the top face of the next plate. The latent heat released there (about 2.26 MJ per kg) conducts through that plate into the wick under it, which evaporates water into stage 2. The cascade repeats through four stages, each running about 6 to 8 K cooler than the one above.
4. **Reject heat.** The bottom plate is the last condenser. Folded aluminum fins on its shaded underside reject the remaining heat to air.
5. **Feed and drain.** Feed water drips from a user-filled container into a trough along the high edge. The wicks drape over the frame wall into the trough and are fed by capillary action and gravity down the 20 deg slope. Excess salty water leaves the low end of each wick into a brine gutter.
6. **Collect distillate.** Condensate runs down each condenser plate to its low edge, drops through a slot into a separate distillate manifold, and leaves through a spout into a clean covered container. An air break keeps wick edges away from distillate paths.

![Energy and water flow (estimates)](../media/flow.png)

## Main components

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Glazing | 6 mm twin-wall UV-stabilized polycarbonate, 1.0 x 1.0 m | Light, shatter resistant, rated above 110 °C |
| 2 | Insulated frame | 12 mm exterior plywood walls with 25 mm foam liner, 1.1 x 1.1 m outside | Holds the stack; slots at the low edge for distillate |
| 3 | Absorber plate | 0.5 mm aluminum, high-temperature matte black paint on top | Stage 1 evaporator surface underneath |
| 4 | Wicks, 4 stages | Cotton or viscose-polyester nonwoven cloth, about 1 mm thick, 1.0 x 1.25 m each | Extra length drapes into the feed trough and brine gutter |
| 5 | Condenser plates, 4 | 0.5 mm aluminum with food-grade coating on the condensing face, or 316 stainless steel | Coating choice proposed, awaiting Amish |
| 6 | Stage spacers | 3D-printed side rails, 6 mm gap, ASA or polycarbonate | Ends left open for feed and drainage |
| 7 | Feed trough | PVC or HDPE rain gutter section with end caps | Fed by a drip valve from a container |
| 8 | Distillate manifold | Food-grade PP or HDPE channel with silicone outlet tube | Separate outlet from the brine |
| 9 | Brine gutter | PVC gutter under the distillate manifold with drain hose | Brine to a soak-away or evaporation pond |
| 10 | Rear heat-rejection fins | Ten folded 0.5 mm aluminum strips, 30 mm deep | On the shaded underside of the bottom plate |
| 11 | Tilt stand | 45 x 45 mm timber posts and rails | 20 deg modeled; adjustable tilt proposed for R11 |
| 12 | Sealant, fasteners and tubing | NSF/ANSI 51 or 61 silicone, stainless screws, silicone tube | Not shown in the model |

![Exploded view](../media/exploded.png)

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Solar input | 19.8 MJ per m2 per day | 5.5 kWh per m2 per day on the aperture | |
| Optical loss | 3.0 MJ (15 %) | Glazing transmittance about 0.88, absorptance about 0.96 | |
| Top loss | 4.4 MJ (22 %) | Convection and radiation from a plate at about 70 °C through one glazing layer | |
| Heat into stage 1 | 12.4 MJ | 19.8 minus 3.0 minus 4.4 | |
| Evaporation fraction per stage | 0.70 | The rest of each stage's heat crosses the gap by conduction and radiation without evaporating water | |
| Edge and sensible loss per stage | 10 % of stage heat | Frame edges and warming the feed and brine | |
| Single-stage yield | about 3.8 L per m2 per day | 0.70 x 12.4 MJ / 2.26 MJ per kg; matches the 3 to 5 L of a basin still | |
| Four-stage yield | about 13.2 L per m2 per day | Stages give 3.8, 3.5, 3.1 and 2.8 L as heat falls 12.4, 11.2, 10.0 and 9.0 MJ | R1 met on paper |
| Gained output ratio | about 1.5 | 29.8 MJ of latent heat in the distillate / 19.8 MJ of sun | R2 met on paper |
| Plausible range | 10.5 to 17.5 L per m2 per day | Gained output ratio 1.2 to 2.0; outdoor transients and fouling push toward the low end | |
| Heat rejected at the bottom | about 8.1 MJ per day, peak about 280 W/m2 | Over about 8 effective sun hours | |
| Bottom plate temperature rise | about 20 to 25 K above ambient | Natural convection about 8 W/m2K on about 1.6 m2 of plate and fin area | Limits stage count; see open questions |
| Stage 1 temperature | about 70 to 80 °C at noon | Bottom plate about 50 to 55 °C plus four stages of about 6 K | |
| Feed and brine | about 35 L feed, about 22 L brine per day | Feed-to-distillate ratio 2.7; seawater brine leaves at about 55 g/L | R6 met on paper |
| Dry stagnation temperature | about 100 to 120 °C | Dry absorber with the stack acting as insulation | R8 depends on material choices |
| Panel mass | about 15 kg dry, 19 kg wet; stand about 6 kg | Five 0.5 mm aluminum plates 6.8 kg, glazing 1.5 kg, frame 4 kg, wicks, fins and channels 2.5 kg | R9 met |
| Parts cost | about $241 | Indicative prices, see bom/bom.csv | R12 met, thin margin |

## Key design choices

- **Four stages.** Each extra stage adds less than the one before because stage heat falls about 10 % per stage and the stack temperature rises as the bottom plate warms. Four stages give an estimated gained output ratio of about 1.5 with manageable temperatures and cost. Options: three stages (simpler, about 10.5 L), four stages (recommended), or six stages (more output only if the bottom can be water-cooled). Proposed, awaiting Amish.
- **Air-cooled fins under the bottom plate.** Keeps the unit standalone. Options: air fins (recommended for the first build), a shallow water tray under the bottom plate that also preheats feed, or placing the unit on a water body as some research prototypes do. Proposed, awaiting Amish.
- **Aluminum plates with a food-grade coating on the condensing face.** Bare aluminum corrodes under salty wicks and leaches into low-mineral distillate. Options: coated aluminum (recommended on cost), 316 stainless steel (better corrosion resistance, about three times the plate cost and over budget), or anodized aluminum. Proposed, awaiting Amish.
- **High-temperature spacer material.** PETG, listed in the original scaffold as "printed spacers", softens near 75 to 80 °C and would fail in stage 1 and at stagnation. ASA or polycarbonate filament is recommended. Proposed, awaiting Amish.
- **Tilt of 20 deg with gravity feed and drainage.** A tilted panel lets both the wicks and the condensate drain by gravity and is better aligned with the sun than a flat basin. Proposed, awaiting Amish; an adjustable stand is needed to meet R11.
- **Aperture of 1 m2.** Household scale that fits the $250 budget. Proposed, awaiting Amish.

## Safety

> **Safety:** Distillate is not certified drinking water. Test it before drinking (at least conductivity and E. coli), store it in a clean covered container, and disinfect it (for example with chlorine) before use. Stages run below pasteurization certainty, brine can wick or splash into distillate channels, and volatile contaminants in the feed can carry over with the vapor. Long-term drinking of distillate needs remineralization.

> **Safety:** Use only food-contact rated materials on every surface that touches distillate: coated or stainless plates, PP or HDPE channels, and NSF/ANSI 51 or 61 silicone. Never use lead-containing solder, treated timber or recycled containers of unknown history in the water path.

> **Safety:** The absorber and glazing can exceed 70 °C in normal use and 100 °C when dry. Do not touch the glazing or open the stack in sun; shade the panel before maintenance. Tip-over in wind is a hazard for a 1 m2 panel at 20 deg: anchor the stand.

- Brine is strongly saline. Discharge it away from crops, wells and soil that must stay fresh.

## Open questions for TRL 3

- Confirm the stage energy balance, including vapor-gap conduction and radiation, and the evaporation fraction of 0.70 assumed here.
- Can air fins reject about 280 W/m2 without pushing stage 1 above the wick and spacer limits, or is a water-cooled bottom needed?
- How is the feed rate set without power (drip valve, wick-limited flow or float valve), and how does salt crystallization at the wick edges behave on a hot, dry afternoon?
- Which condenser coating is food safe, durable at 80 °C and affordable?
- Identify a coastal community or NGO partner for co-design and eventual field testing.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html), [cutaway](../media/cutaway.png).
