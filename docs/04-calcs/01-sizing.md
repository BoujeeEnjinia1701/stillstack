---
doc_id: SSK-CAL-001
title: StillStack sizing calculations
project: StillStack
doc_type: Calculation
version: "0.5"
status: Draft
date: '2026-10-02'
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
  - version: "0.4"
    date: 2026-10-01
    author: Amish Chadha
    change: Design for construction (SSK-DDR-003); constructability checks; budget treated as a value-engineering target
  - version: "0.5"
    date: '2026-10-02'
    author: Amish Chadha
    change: "SSK-DDR-003 accepted (2026-10-02); R4, R7 and R10 rows note the decisions; figures unchanged"
---

# StillStack sizing calculations

On paper the decided design (four stages, 6 mm gaps, air-cooled fins, 1 m2 at 20 deg) makes about **10.6 L per m2 per day** on the 5.5 kWh per m2 design day, with a gained output ratio of **1.26 to 1.34**. That meets R1 with a thin margin, puts R2 at risk, and misses the 13 L design goal. Dry stagnation reaches about **140 °C** at stage 1 (**144 °C** in calm air). Under SSK-DDR-002 R8 now asks for a 150 °C rating in stages 1 and 2 and 110 °C elsewhere, plus a stagnation cover; the margins are 6 K and 0 K, so R8 is **at risk**. Value-engineering target: USD 355. Estimated cost of the constructable design: USD 416.20 (USD 61.20 over the target). The constructable design of SSK-DDR-003 (base ring, glazing trim, zigzag plate edges with distillate and brine tongues, stop blocks, pinned props) leaves the yield at 10.6 L and the panel at 18.5 kg dry. Every number below is printed by `docs/04-calcs/sizing.py`; the geometry figures come from `cad/src/model.py`.

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

**Support of the whole stack (SSK-DDR-003).** The stack rests on a 12 mm plywood base ring whose 15 mm ledge carries the bottom plate's edges and the side rails. The ribs carry their share of the stack (about 108 N/m2 normal to the plate at 20 deg) onto the bottom plate, which spans the 970 mm between the high and low ledges as ten fin-stiffened strips: with the fins bonded the sag is about 0.5 mm, and 1.0 mm if the fins carried the load alone (section 13). The whole stack moves together, so the gaps do not change. The wicks now stop 13 mm inside the plates' zigzag low edge, which lowers the wet wick fraction from 0.824 to 0.817; the design-day yield stays at 10.6 L.

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
| Distillate, stages 1 to 4 | 3.44, 2.97, 2.59, 2.28 L |
| Distillate, quasi-steady | 11.3 L |
| Gained output ratio, quasi-steady | 1.34 |
| Warm-up energy (25.7 kJ/K per m2 of stack to the mean noon temperature) | 0.92 MJ |
| Distillate after warm-up deduction | 10.6 L |
| Gained output ratio after warm-up deduction | 1.26 |

At noon the plates run at 73.3, 69.5, 65.8, 62.2 and 58.4 °C, the bottom plate 28.4 K above ambient, and the top loss is 172 W/m2. The TRL 2 figures of 13.2 L and a gained output ratio of 1.5 were optimistic mainly because of the glazing transmittance and because the sensible heat of the feed (3.8 MJ, about 19 % of the sun) was not counted. The warm-up deduction is conservative, since part of the stored heat still produces distillate as the stack cools in the evening.

Table 3. Sensitivity of daily output (quasi-steady).

| Case | Distillate (L/m2/day) | Gained output ratio | Peak absorber (°C) | Peak bottom (°C) |
| --- | --- | --- | --- | --- |
| 3 stages | 9.1 | 1.08 | 73 | 62 |
| 4 stages (base) | 11.3 | 1.34 | 73 | 58 |
| 6 stages | 14.9 | 1.77 | 74 | 53 |
| No rib breaks in the wicks | 11.7 | 1.39 | 72 | 59 |
| Feed ratio 3.5 | 10.5 | 1.25 | 71 | 55 |
| Wind 3 m/s | 11.6 | 1.38 | 69 | 48 |
| Painted underside (emissivity 0.90) | 11.7 | 1.39 | 70 | 50 |
| Sunny day, 6.5 kWh/m2 | 13.6 | 1.36 | 77 | 62 |
| Hazy day, 4.5 kWh/m2 | 9.0 | 1.31 | 69 | 54 |

Air fins are adequate for four stages: the bottom plate stays near 58 °C and the stage temperatures stay well below the limits of the wicks and spacers in wet operation. Six stages would gain about 3.6 L on paper without a water-cooled bottom, but the decision is four.

## 5. Hot operation and dry stagnation

At 1,000 W/m2 and 35 °C ambient, wet operation peaks at 80.1 °C at the absorber and 67.1 °C at the bottom plate. With dry wicks the plates reach **140, 123, 106, 87 and 65 °C** (absorber first). In calm air they reach **144, 128, 110, 91 and 69 °C**. The inner glazing sheet reaches about 109 °C (115 °C in calm air) and the outer sheet 61 °C.

> **Safety:** A dry panel in full sun holds the absorber near 140 °C. Fit the stagnation cover before opening the stack, and treat an empty feed container as a burn and material-damage hazard.

Consequences for R8 as restated in SSK-DDR-002. Stages 1 and 2 (absorber to plate 2) peak at 144 °C against the 150 °C rating, a margin of 6 K; their rails are therefore a 150 °C polymer (PPS or a high-heat polycarbonate copolymer), the ribs silicone and the liner stone wool, and the wick and the coating on plates 1 and 2 must tolerate 150 °C. Stages 3 and 4 peak at 110 °C in calm air against the 110 °C rating, a margin of 0 K; printed polycarbonate rails remain acceptable there, but ASA (softening near 95 to 100 °C) stays excluded from stages 1 to 3. The inner glazing sheet at 115 °C in calm air is close to the typical limit of twin-wall polycarbonate. The stagnation cover (BOM line 14) and the shade rule are the second barrier: the cover is fitted whenever the feed runs out.

## 6. Wick feed capacity

At noon stage 1 evaporates 0.58 kg/m2/h, so each metre of wick width must carry 1.44 kg/h of feed at a ratio of 2.5. With gravity along the 20 deg slope (3,360 Pa/m) and an assumed 4 kPa of capillary pressure over the 1 m run, Darcy flow through a 1 mm wick needs a permeability of at least **3.0 x 10^-11 m2**. Capacity is 0.48, 1.44 and 4.81 kg/h per metre at 1 x 10^-11, 3 x 10^-11 and 1 x 10^-10 m2. The permeability of the candidate fabrics is not known, so feed supply is a risk to R1 and R6.

## 7. Salt balance and carryover

At a feed ratio of 2.5 the brine leaves at 58.3 g/L for 35 g/L seawater and 66.7 g/L for 40 g/L feed, a factor of 4.8 below sodium chloride saturation (about 317 g/L). Salt does not travel with the vapor, so distillate salinity depends only on liquid carryover. To stay below 50 mg/L the brine reaching the distillate must be under 0.075 % of the distillate, about **8.5 mL per day** on the design day. On the design day the panel takes about 28.2 L of feed and discharges 16.9 L of brine.

## 8. Mass, footprint and tilt

Table 4. Panel mass (constructable design, SSK-DDR-003).

| Item | Mass (kg) |
| --- | --- |
| Plates, five 0.5 mm aluminum, with tongues | 6.94 |
| Glazing, twin-wall polycarbonate, 1.06 m square | 1.46 |
| Walls, 12 mm plywood, less openings | 1.35 |
| Liner, 25 mm stone wool | 0.69 |
| Base ring, 12 mm plywood | 1.40 |
| Glazing trim, aluminum angle | 1.00 |
| Wicks, dry, with tails | 1.12 |
| Side rails, 150 °C polymer and printed polycarbonate | 0.81 |
| Ribs, silicone cord | 0.71 |
| Fins | 0.63 |
| Trough, manifold, gutter, brackets, closure and fittings | 1.80 |
| Sealant, tape, fasteners and tubing | 0.60 |
| **Panel, dry** | **18.5** |
| Panel, wet wicks | 22.5 |
| Adjustable stand | 8.9 |

The model's own volume-based estimate for the modeled parts (16.1 kg without the trough, manifold, gutter and fasteners) agrees within the allowances above.

The stand (SSK-DDR-003) pivots the panel on two M10 bolts through front posts 372 mm above the ground and holds it with two fixed props, 1,000 mm between pins, hinged on blocks near the high end and pinned to the ground rails. One hole per tilt sets the angle; measured back from the pivot the holes are at 113, 151, 195, 245, 309 and 396 mm for 10, 15, 20, 25, 30 and 35 deg. The plan footprint is 1.28 x 1.25 m at 10 deg, 1.21 x 1.25 m at 20 deg and 1.05 x 1.25 m at 35 deg. The ground rails run 760 mm behind the pivot, so the wet panel's centre of mass (about 500 mm behind the pivot at 10 deg) stays at least 260 mm inside the ground frame. The model builds and checks the stand at all six holes; the feed trough rim is at most 1.00 m above the ground.

## 9. Wind

At 20 m/s the normal force on the 1.15 m2 panel (force coefficient 1.2) is about 332 N, against 308 N for the wet panel and stand. Lift equals weight at about 18.7 m/s.

> **Safety:** The panel and stand can overturn in a strong breeze. Anchor the stand to the ground or ballast it before filling.

## 10. Cost

Value-engineering target: USD 355 (a hypothetical control target, `budget_usd` in `project.yaml`). Estimated cost of the constructable design: USD 416.20 from `bom/bom.csv` (18 lines), USD 61.20 over the target. Before SSK-DDR-003 the concept priced at USD 351.20. The USD 65 added for construction is USD 20 for larger plate blanks for the tongues (lines 3 and 5), USD 2 for longer wicks (line 4), USD 20 for the glazing trim and tape (line 15), USD 7 for the stand's ground frame, gussets and pins (line 12), USD 4 for the trough brackets (line 8), USD 6 for the outlet brackets (line 16) and USD 6 for the feed closure (line 17).

## 11. Results against requirements

Table 5. Requirement status at TRL 3, not met first.

| ID | Quantity | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R8 | Temperatures at dry stagnation | Stages 1 and 2: 144 °C calm (6 K margin); stages 3 and 4: 110 °C calm (0 K margin); cover specified | 150 °C in stages 1 and 2, 110 °C elsewhere, cover and shade rule | At risk |
| R2 | Gained output ratio | 1.34 quasi-steady; 1.26 after warm-up deduction | 1.3 or more | At risk |
| R4 | Air break between wick edges and distillate paths | 10 mm at ribs and rails and inside the plate edges; brine tongues pass 10.5 mm or more over the closed manifold lid and at least 44 mm from any distillate tongue (SSK-DDR-003 A1, accepted 2026-10-02; high-edge lip of A2 (c) decided, not yet modelled) | 10 mm or more, no shared drain | At risk |
| R6 | Brine salinity; wick feed | 66.7 g/L at 40 g/L feed; needs permeability of 3.0 x 10^-11 m2 or more | Feed ratio 2.5 or more, salt stays in solution | At risk |
| R7 | Food-contact wetted surfaces | Coated aluminum decided; coating product not selected (rule decided 2026-10-02: certified for drinking-water contact and 150 °C dry, else 316 stainless for plates 1 and 2) | All distillate-side surfaces food-contact rated | At risk |
| R10 | Wick removal time; flushing interval | Plates lift out after the low wall cap is removed; wicks to be held by end clips with no adhesive (decided 2026-10-02) | 30 min or less; weekly or less often | At risk |
| R3 | Distillate conductivity | Carryover allowance 0.075 % (8.5 mL/day) | 75 µS/cm or less | Not verifiable at TRL 3 |
| R1 | Daily distillate | 10.6 L/m2 (11.3 quasi-steady) | 10 L/m2 or more (goal 13) | Met (6 % margin; goal not met) |
| R12 | Parts cost | USD 416.20 | Value-engineering target USD 355 | USD 61.20 over the target |
| R5 | Power; feed head | Passive; feed trough rim 1.00 m at 35 deg | No power; container at most 1.5 m | Met |
| R9 | Mass; footprint | 18.5 kg dry; 1.28 x 1.25 m | 20 kg or less; within 1.3 x 1.3 m | Met |
| R11 | Tilt range | Six prop holes, 10 to 35 deg in 5 deg steps; model built and checked at each | 10 to 35 deg | Met |

## 12. Changes to earlier figures

SSK-PRC-001 v0.2 gave 13.2 L per day, a gained output ratio of about 1.5, stage 1 at 70 to 80 °C, dry stagnation at 100 to 120 °C, feed of 35 L and brine of 22 L, a panel of about 15 kg and parts of about $241. The precis v0.3 now quotes the values in this note.

Version 0.2 of this note (SSK-DDR-002) adds the calm-air plate temperatures and the restated R8 check, and changes the panel mass from 15.9 to 16.7 kg dry (19.9 to 20.7 kg wet), the wet panel and stand weight from 264 to 272 N, and the parts cost from $317.20 to $351.20 against a budget raised from $250 to $320. The energy balance, yield and gained output ratio are unchanged.

Version 0.3 of this note records the budget top-up to $355 approved by Amish on 2026-09-26; the parts cost is unchanged at $351.20 and R12 moves from not met to met.

Version 0.4 of this note follows SSK-DDR-003 (design for construction, made under Amish's 2026-09-30 instruction to make the design physically buildable; accepted by Amish on 2026-10-02 with the exceptions recorded there). The wet wick fraction falls from 0.824 to 0.817, which moves the stage outputs by at most 0.01 L; the daily yield (10.6 L), gained output ratio and stagnation temperatures are unchanged at the precision quoted. The panel rises from 16.7 to 18.5 kg dry (20.7 to 22.5 kg wet), the stand from 7.1 to 8.9 kg, the footprint from 1.28 x 1.16 m to 1.28 x 1.25 m, the wind speed at which lift equals weight from 17.5 to 18.7 m/s, and the cost from USD 351.20 to USD 416.20, now reported against the USD 355 value-engineering target. Feed and brine figures were also brought in line with the script (28.2 and 16.9 L per day).

## 13. Design for construction checks

Table 6. Checks added for the constructable design (section 14 of the script).

| Check | Result |
| --- | --- |
| Bottom plate sag on the base ring, fins bonded (composite) | 0.5 mm |
| Bottom plate sag, fins carrying the load alone | 1.0 mm |
| Glazing growth, 1.06 m sheet at a 70 K rise | 4.8 mm, against 14 mm of room inside the trim |
| Load per pivot bolt, wet panel plus 17 m/s wind | 163 N; bearing on 12 mm plywood 1.4 MPa |
| Prop buckling, 45 x 45 mm timber, 1.0 m pinned | 27 kN, far above the load |
| Outlet bracket load, manifold and gutter full | 29 N each; 62 N pull on the top screw |
| Vapor lost through the low-end tongue openings (diffusion, 4 gaps) | 25 mL per day (0.2 % of the yield) |
| Lowest brine tongue tail above the distillate lid | 10.5 mm |

The parametric model also runs its own constructability checks (`python cad/src/model.py --check`): no overlaps among the 46 panel parts, every part that must touch does touch, every brine path keeps 10 mm or more from every distillate path, and the stand at each of the six tilt holes has no clashes, keeps the centre of mass inside the ground frame and stays within the 1.3 x 1.3 m footprint.
