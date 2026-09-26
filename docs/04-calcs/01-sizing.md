---
doc_id: SSK-CAL-001
title: StillStack sizing calculations
project: StillStack
doc_type: Calculation
version: "0.3"
status: Draft
date: 2026-09-26
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-09-25
    author: Amish Chadha
    change: First TRL 3 sizing (stage energy balance, supports, stagnation, wick feed, salt, mass, tilt, cost)
  - version: "0.2"
    date: 2026-09-25
    author: Amish Chadha
    change: Recommendations accepted by Amish (DDR-002)
  - version: "0.3"
    date: 2026-09-26
    author: Amish Chadha
    change: Budget top-up approved by Amish
---

# StillStack sizing calculations

On paper the decided design (four stages, 6 mm gaps, air-cooled fins, 1 m2 at 20 deg) makes about **10.6 L per m2 per day** on the 5.5 kWh per m2 design day, with a gained output ratio of **1.26 to 1.34**. That meets R1 with a thin margin, puts R2 at risk, and misses the 13 L design goal. Dry stagnation reaches about **140 °C** at stage 1 (**144 °C** in calm air). Under SSK-DDR-002 R8 now asks for a 150 °C rating in stages 1 and 2 and 110 °C elsewhere, plus a stagnation cover; the margins are 6 K and 0 K, so R8 is **at risk**. The priced BOM, with the 150 °C rails and the cover added, totals **$351.20** against the $355 budget approved by Amish on 2026-09-26, so R12 is **met** with a $3.80 margin. Every number below is printed by `docs/04-calcs/sizing.py`; the geometry figures come from `cad/src/model.py`.

## 1. Method

The script solves a quasi-steady energy balance of the stack every 15 minutes through a sinusoidal design day, then integrates.

- **Nodes.** Absorber plate, three intermediate condenser plates and the bottom plate (five plate temperatures), plus the four wet wick faces. Heat conducts from each plate through its 1 mm wick (k = 0.45 W/mK) to the wick face.
- **Vapor gap.** Latent transfer by Stefan diffusion of vapor through air, m = (P M D / R T d) ln((P - p_c)/(P - p_w)); conduction through still air (the gap is heated from above and stably stratified, so Nu = 1); gray-body radiation between the wet wick (emissivity 0.95) and the condensing face (0.90); conduction through the ribs and rails.
- **Top loss.** Absorber to glazing across the 25 mm air layer (Hollands correlation for an inclined layer, plus radiation with emissivities 0.90), across the twin-wall cells (9.3 W/m2K, from a typical sheet U-value of 3.6 W/m2K less surface films), and from the outer sheet to wind (h = max(5, 8.6 V^0.6 / L^0.4)) and sky (Swinbank sky temperature).
- **Bottom.** Natural convection from a heated surface facing down at 70 deg from vertical (Fujii and Imura), combined with sheltered wind at half the free-stream speed; fin efficiency for 0.5 mm aluminum fins 30 mm deep; radiation from the bare aluminum underside (emissivity 0.10) to ground at ambient.
- **Feed.** Each stage heats its own feed from ambient to the wick temperature at a feed-to-distillate ratio of 2.5, and that heat leaves with the brine.
- **Edges.** 12 mm plywood plus 25 mm foil-faced stone wool (k about 0.035 W/mK), U = 1.07 W/m2K, over the wall height of each stage. Stone wool replaced PIR under SSK-DDR-002 with the same assumed conductivity, so the energy balance is unchanged.
- **Thermal mass.** Treated separately as a warm-up deduction, because the quasi-steady solution ignores it.

### Assumptions

- Design day: 5.5 kWh per m2 (19.8 MJ per m2) on the tilted aperture, spread as a sine over 10 h (peak 864 W/m2); ambient 30 °C; wind 1 m/s.
- Optics: twin-wall polycarbonate transmittance 0.80 and absorber absorptance 0.95, so τα = 0.76. The TRL 2 estimate used 0.88 for the glazing, which is a single-glass value.
- Latent heat varies with temperature (2.33 to 2.36 MJ per kg over the stage range), replacing the flat 2.26 MJ per kg used at TRL 2.
- Wet wick area: wicks are cut into five strips with 10 mm dry breaks at each rib and rail (R4) and stop 20 mm short of the low edge, leaving 82.4 % of the aperture wet.
- The feed ratio is held at the R6 minimum of 2.5 to limit sensible loss.
- Properties of air and vapor use standard power-law fits; saturation pressure uses the Buck equation.

## 2. Vapor gap transfer

Most of the heat crossing each gap is latent, and the fraction rises steeply with temperature (Table 1). The TRL 2 assumption of 0.70 per stage was conservative: at the noon operating point the four stages run at 0.91, 0.89, 0.87 and 0.85.

Table 1. Heat flux across one 6 mm gap with 5 K between the wick face and the condensing face.

| Wick face (°C) | Latent (W/m2) | Conduction (W/m2) | Radiation (W/m2) | Evaporation fraction |
| --- | --- | --- | --- | --- |
| 40 | 150 | 22.3 | 29.2 | 0.74 |
| 50 | 251 | 22.9 | 32.1 | 0.82 |
| 60 | 418 | 23.4 | 35.2 | 0.88 |
| 70 | 712 | 24.0 | 38.5 | 0.92 |
| 80 | 1,298 | 24.6 | 42.0 | 0.95 |

## 3. Plate support and spacer ribs

A 0.5 mm aluminum plate carrying a wet wick cannot span the frame. Under 22.6 N/m2 (plate, 1.0 kg/m2 of wet wick and condensate, normal to the 20 deg slope), beam theory gives a sag of about 325 mm over the 0.972 m clear span, so the TRL 2 concept with side rails only would close every gap. Treating each strip as simply supported, a sag of 1.0 mm (one sixth of the gap) allows a pitch of up to 229 mm. **Four intermediate ribs per gap at 194 mm pitch** give a sag of 0.52 mm. The ribs run down the slope so they do not block feed or condensate. Each plate grows about 1.4 mm across 1 m at a 60 K rise, so the model leaves 2 mm of clearance each side instead of tensioning the plates.

The ribs are 7 mm food-grade silicone cord (decided by Amish on 2026-09-25, SSK-DDR-002): silicone is rated well above the stagnation temperature and wets poorly, which limits brine creep across the rib. Printed polycarbonate ribs would cost about the same.

## 4. Design day

Table 2. Daily energy and water balance per m2 of aperture.

| Quantity | Value |
| --- | --- |
| Solar input | 19.8 MJ |
| Optical loss | 4.8 MJ |
| Absorbed | 15.1 MJ |
| Top loss | 4.5 MJ |
| Edge loss | 0.15 MJ |
| Heat into stage 1, 2, 3, 4 wicks | 10.5, 9.2, 8.1, 7.3 MJ |
| Feed heating lost with brine, stages 1 to 4 | 1.32, 1.03, 0.81, 0.63 MJ (3.8 MJ total) |
| Heat rejected at the bottom | 6.6 MJ (peak 277 W/m2) |
| Distillate, stages 1 to 4 | 3.45, 2.97, 2.60, 2.29 L |
| Distillate, quasi-steady | 11.3 L |
| Gained output ratio, quasi-steady | 1.34 |
| Warm-up energy (25.7 kJ/K per m2 of stack to the mean noon temperature) | 0.92 MJ |
| Distillate after warm-up deduction | 10.6 L |
| Gained output ratio after warm-up deduction | 1.26 |

At noon the plates run at 73.2, 69.4, 65.7, 62.0 and 58.3 °C, the bottom plate 28.3 K above ambient, and the top loss is 172 W/m2. The TRL 2 figures of 13.2 L and a gained output ratio of 1.5 were optimistic mainly because of the glazing transmittance and because the sensible heat of the feed (3.8 MJ, about 19 % of the sun) was not counted. The warm-up deduction is conservative, since part of the stored heat still produces distillate as the stack cools in the evening.

Table 3. Sensitivity of daily output (quasi-steady).

| Case | Distillate (L/m2/day) | Gained output ratio | Peak absorber (°C) | Peak bottom (°C) |
| --- | --- | --- | --- | --- |
| 3 stages | 9.1 | 1.08 | 73 | 62 |
| 4 stages (base) | 11.3 | 1.34 | 73 | 58 |
| 6 stages | 14.9 | 1.77 | 74 | 53 |
| No rib breaks in the wicks | 11.7 | 1.39 | 72 | 59 |
| Feed ratio 3.5 | 10.5 | 1.25 | 71 | 55 |
| Wind 3 m/s | 11.6 | 1.39 | 69 | 48 |
| Painted underside (emissivity 0.90) | 11.7 | 1.39 | 70 | 50 |
| Sunny day, 6.5 kWh/m2 | 13.6 | 1.37 | 77 | 62 |
| Hazy day, 4.5 kWh/m2 | 9.0 | 1.31 | 69 | 54 |

Air fins are adequate for four stages: the bottom plate stays near 58 °C and the stage temperatures stay well below the limits of the wicks and spacers in wet operation. Six stages would gain about 3.6 L on paper without a water-cooled bottom, but the decision is four.

## 5. Hot operation and dry stagnation

At 1,000 W/m2 and 35 °C ambient, wet operation peaks at 80.0 °C at the absorber and 66.9 °C at the bottom plate. With dry wicks the plates reach **140, 123, 106, 87 and 65 °C** (absorber first). In calm air they reach **144, 128, 110, 91 and 69 °C**. The inner glazing sheet reaches about 109 °C (115 °C in calm air) and the outer sheet 61 °C.

> **Safety:** A dry panel in full sun holds the absorber near 140 °C. Fit the stagnation cover before opening the stack, and treat an empty feed container as a burn and material-damage hazard.

Consequences for R8 as restated in SSK-DDR-002. Stages 1 and 2 (absorber to plate 2) peak at 144 °C against the 150 °C rating, a margin of 6 K; their rails are therefore a 150 °C polymer (PPS or a high-heat polycarbonate copolymer), the ribs silicone and the liner stone wool, and the wick and the coating on plates 1 and 2 must tolerate 150 °C. Stages 3 and 4 peak at 110 °C in calm air against the 110 °C rating, a margin of 0 K; printed polycarbonate rails remain acceptable there, but ASA (softening near 95 to 100 °C) stays excluded from stages 1 to 3. The inner glazing sheet at 115 °C in calm air is close to the typical limit of twin-wall polycarbonate. The stagnation cover (BOM line 14) and the shade rule are the second barrier: the cover is fitted whenever the feed runs out.

## 6. Wick feed capacity

At noon stage 1 evaporates 0.58 kg/m2/h, so each metre of wick width must carry 1.45 kg/h of feed at a ratio of 2.5. With gravity along the 20 deg slope (3,360 Pa/m) and an assumed 4 kPa of capillary pressure over the 1 m run, Darcy flow through a 1 mm wick needs a permeability of at least **3.0 x 10^-11 m2**. Capacity is 0.48, 1.44 and 4.81 kg/h per metre at 1 x 10^-11, 3 x 10^-11 and 1 x 10^-10 m2. The permeability of the candidate fabrics is not known, so feed supply is a risk to R1 and R6.

## 7. Salt balance and carryover

At a feed ratio of 2.5 the brine leaves at 58.3 g/L for 35 g/L seawater and 66.7 g/L for 40 g/L feed, a factor of 4.8 below sodium chloride saturation (about 317 g/L). Salt does not travel with the vapor, so distillate salinity depends only on liquid carryover. To stay below 50 mg/L the brine reaching the distillate must be under 0.075 % of the distillate, about **8.6 mL per day** on the design day. On the design day the panel takes about 28.7 L of feed and discharges 17.2 L of brine.

## 8. Mass, footprint and tilt

Table 4. Panel mass.

| Item | Mass (kg) |
| --- | --- |
| Plates, five 0.5 mm aluminum (four with 77 mm lips) | 7.17 |
| Glazing, twin-wall polycarbonate | 1.30 |
| Frame, 12 mm plywood | 2.00 |
| Liner, 25 mm stone wool | 1.02 |
| Wicks, dry | 1.00 |
| Side rails, 150 °C polymer and printed polycarbonate | 0.81 |
| Ribs, silicone cord | 0.71 |
| Fins | 0.65 |
| Trough, manifold, gutter and fittings | 1.50 |
| Sealant, fasteners and tubing | 0.50 |
| **Panel, dry** | **16.7** |
| Panel, wet wicks | 20.7 |
| Adjustable stand | 7.1 |

The model's own volume-based estimate for the modeled parts (13.9 kg without the trough, manifold, gutter and fasteners) agrees within the allowances above.

With a front pivot 350 mm above the ground, the rear struts are 0.53, 0.70 and 0.94 m long at 10, 20 and 35 deg. The plan footprint is 1.28 x 1.16 m at 10 deg, 1.24 x 1.16 m at 20 deg and 1.11 x 1.16 m at 35 deg. The parametric model builds cleanly across the range (plan depth 1,263, 1,204 and 1,048 mm including the stand; feed trough top 609, 799 and 1,058 mm above the ground).

## 9. Wind

At 20 m/s the normal force on the 1.15 m2 panel (force coefficient 1.2) is about 332 N, against 272 N for the wet panel and stand. Lift equals weight at about 17.5 m/s.

> **Safety:** The panel and stand can overturn in a strong breeze. Anchor the stand to the ground or ballast it before filling.

## 10. Cost

The priced BOM (`bom/bom.csv`, 15 lines) totals **$351.20**, which is **$3.80 under** the $355 budget approved by Amish on 2026-09-26 (SSK-DDR-002 v0.2; the budget was $320 in SSK-DDR-002 v0.1). Version 0.1 of this note gave $317.20 against $250. The $34 added under SSK-DDR-002 is $22 for the four 150 °C rails in stages 1 and 2 (an allowance of $9 each in place of $3.50) and $12 for the stagnation cover; the stone wool liner is priced the same as the PIR it replaces.

## 11. Results against requirements

Table 5. Requirement status at TRL 3, not met first.

| ID | Quantity | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R8 | Temperatures at dry stagnation | Stages 1 and 2: 144 °C calm (6 K margin); stages 3 and 4: 110 °C calm (0 K margin); cover specified | 150 °C in stages 1 and 2, 110 °C elsewhere, cover and shade rule | At risk |
| R2 | Gained output ratio | 1.34 quasi-steady; 1.26 after warm-up deduction | 1.3 or more | At risk |
| R4 | Air break between wick edges and distillate paths | 10 mm at ribs and rails, 20 mm at the low edge; brine exit over the lidded manifold not yet detailed | 10 mm or more, no shared drain | At risk |
| R6 | Brine salinity; wick feed | 66.7 g/L at 40 g/L feed; needs permeability of 3.0 x 10^-11 m2 or more | Feed ratio 2.5 or more, salt stays in solution | At risk |
| R7 | Food-contact wetted surfaces | Coated aluminum decided; coating product not selected | All distillate-side surfaces food-contact rated | At risk |
| R10 | Wick removal time; flushing interval | Wicks bonded under plates; removal method not defined | 30 min or less; weekly or less often | At risk |
| R3 | Distillate conductivity | Carryover allowance 0.075 % (8.6 mL/day) | 75 µS/cm or less | Not verifiable at TRL 3 |
| R1 | Daily distillate | 10.6 L/m2 (11.3 quasi-steady) | 10 L/m2 or more (goal 13) | Met (6 % margin; goal not met) |
| R12 | Parts cost | $351.20 | $355 or less | Met ($3.80 margin) |
| R5 | Power; feed head | Passive; feed trough top 1.06 m at 35 deg | No power; container at most 1.5 m | Met |
| R9 | Mass; footprint | 16.7 kg dry; 1.28 x 1.16 m | 20 kg or less; within 1.3 x 1.3 m | Met |
| R11 | Tilt range | Stand and model built at 10, 20 and 35 deg | 10 to 35 deg | Met |

## 12. Changes to earlier figures

SSK-PRC-001 v0.2 gave 13.2 L per day, a gained output ratio of about 1.5, stage 1 at 70 to 80 °C, dry stagnation at 100 to 120 °C, feed of 35 L and brine of 22 L, a panel of about 15 kg and parts of about $241. The precis v0.3 now quotes the values in this note.

Version 0.2 of this note (SSK-DDR-002) adds the calm-air plate temperatures and the restated R8 check, and changes the panel mass from 15.9 to 16.7 kg dry (19.9 to 20.7 kg wet), the wet panel and stand weight from 264 to 272 N, and the parts cost from $317.20 to $351.20 against a budget raised from $250 to $320. The energy balance, yield and gained output ratio are unchanged.

Version 0.3 of this note records the budget top-up to $355 approved by Amish on 2026-09-26; the parts cost is unchanged at $351.20 and R12 moves from not met to met.
