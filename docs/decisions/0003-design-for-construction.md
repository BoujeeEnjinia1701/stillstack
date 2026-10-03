---
doc_id: SSK-DDR-003
title: StillStack design for construction
project: StillStack
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish (2026-10-02) with exceptions: A2 decided as option (c), P11 wick fixing replaced by clips; A1 as recommended; status kept Draft"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Exceptions carried into the model, drawings, BOM and calculations (lip tabs, wick clips, PPS rails, labels); mass, cost and drawing figures updated"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted, with exceptions. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." The changes in Tables 1 and 2 are accepted as made, with two exceptions decided in the design decisions register (SSK-DEC-001): A2 is decided as option (c), a 4 mm downturned lip on each condensing plate's high edge, not the (a) the model and build plan show; and the silicone dots of P11 are replaced by clips at each wick's high and low ends with no adhesive. A1 is accepted as recommended, with each stage's distillate conductivity test a pass condition at TRL 4 before any water is drunk. The model and the build plan pictures still show option (a) of A2 and the silicone dots until they are updated.

## Context

On 2026-09-30 Amish asked for a build plan that shows how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model (SSK-DDR-002) showed what StillStack does but left several parts that could not be made, fixed or assembled as drawn. Checking the model with build123d found twelve (P1 to P12 below).

The changes keep what the panel does: the same 1 m2 aperture, four stages with 6 mm gaps, plate and wick materials, ribs at 194 mm pitch, 25 mm air gap and twin-wall glazing, air-cooled fins, gravity feed from a trough at the high edge, a lidded distillate manifold and a brine gutter outboard of and lower than it at the low edge, and a stand adjustable from 10 to 35 deg. Every change is in `cad/src/model.py`, which now runs 93 constructability checks (`python cad/src/model.py --check`): no overlaps among the 46 panel parts, every contact that must exist does, every brine path keeps 10 mm from every distillate path, and the stand is checked at each of its six tilt holes.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations (Draft, open for Amish's review).*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The stack sat on a 5 mm "ledge" of no stated material along the two side walls only; the bottom plate had nothing under its high and low edges and nothing under its middle. | A 12 mm plywood base ring (four strips) under the walls, with a 15 mm ledge into the aperture on all four sides. The bottom plate rests on the ledge all round and spans 970 mm between the high and low ledges as ten fin-stiffened strips; the side rails sit directly over the side ledges. | The ribs bring the stack's weight (108 N/m2) down onto the bottom plate; with its fins bonded it sags about 0.5 mm (1.0 mm on the fins alone), and the whole stack moves together, so the gaps stay at 6 mm (SSK-CAL-001 section 13). |
| P2 | The low wall had four 996 x 2 mm slits for the plate lips, leaving 5.5 mm slivers of plywood that cannot be cut or survive, and a plate with a lip cannot be put through a slit from inside the frame. | The low wall is a comb: a 12 mm sill along the bottom and teeth between eleven open-topped notches 33 mm deep, with a separate cap strip (and its liner) that closes the notches above the stack. | Each plate drops in from above with its tongues in the notches. Lifting the cap lets the plates come out again, which also helps R10. |
| P3 | The brine exit at the low edge was not detailed (R4 at risk): wick tails had to cross the distillate lips, which sit 7.5 mm apart in the same edge. | The plates' low edges are cut to a zigzag. Distillate leaves on six 30 mm tongues at the rib lines and corners, which turn down through slots in the manifold lid. Brine leaves on five 50 mm tongues at the strip centres, each carrying a 30 mm wick tail underneath, over the closed lid and down into the brine gutter. A silicone chevron dam at each brine tongue root turns condensate aside. See A1. | Brine and distillate are separated across the panel's width, not stacked, so every brine path keeps at least 10.5 mm (over the lid) and 44 mm (sideways) from every distillate path. |
| P4 | Nothing stopped the plates and rails sliding down the slope: the lips slid freely in their slits and the plate ends faced soft stone wool. | Two stop blocks, cut from the stage 1 rail polymer, fill the liner's low corners. The plate corners and the rail ends bear on them, and they bear on the low wall. | A hard face where the stack's down-slope load (up to sin 35 deg of its weight) goes into the plywood. |
| P5 | The glazing floated 4 mm below a frame lip with no fixing, in an opening its own size, with no room for the 4.8 mm it grows when hot. | A 1,060 mm square sheet on 3 mm silicone foam tape on the wall tops, held by a mitred aluminium trim (25 x 20 x 2 mm angle) screwed to the walls. The walls end under the tape (52.5 mm tall). | 7 mm of room each side for growth; the trim stops 14 mm outside the aperture, so it casts no shade. This adopts item 1 of the 2026-09-26 product model review. |
| P6 | The wicks "drape over the frame wall into the trough", but the wall rises above the stack and the trough had no fixing. | Five feed openings in the high wall, one per wick strip; each tail runs out, up the outside of the wall and over the trough rim. A silicone foam strip on the trough's inner wall closes the openings around the tails. The trough hangs on two fascia gutter brackets screwed to the wall's solid ends. | Feed reaches each stage without crossing anything but the wall; the closure keeps vapor in and dust out. |
| P7 | The manifold and brine gutter had no support or fixing. | Two outlet brackets (30 x 4 mm aluminium flat bar, bent to an L) screwed to teeth of the low wall comb carry the manifold against their uprights and the gutter on their outer ends. | The gutter sits 10 mm lower and 7 mm outboard of the manifold, as the concept requires. |
| P8 | The fins had no fixing and their ends ran into the zigzag edge and the ledge. | Fins 940 mm long, bonded by their 20 mm flange with high-temperature silicone adhesive, 15 mm clear of the ledge. | Bonding leaves the condensing face above unpierced. |
| P9 | The rear struts were vertical posts from the ground, but the frame's high edge moves about 90 mm along the ground as the tilt changes, and a frame on pinned posts is a mechanism. | Ground frame (two rails, two cross rails); front posts on the rails, made rigid by plywood gussets; an M10 pivot bolt through each post and side wall; fixed-length props (1,000 mm between pins) hinged on blocks near the high end and pinned to the rail at one of six holes (10 to 35 deg in 5 deg steps). The rails run 760 mm behind the pivot. | Each side is a rigid triangle at every tilt. The centre of mass stays at least 260 mm inside the ground frame; the footprint is 1.28 x 1.25 m, within R9. |
| P10 | The walls had no corner joints. | Butt joints, glued and screwed through the side walls; the base ring and the trim tie the corners top and bottom. | Plain joints a home workshop can make. |
| P11 | "Wicks bonded under the plates" gave no method. | Dots of food-grade silicone every 100 mm along both edges of each strip. Replaced on 2026-10-02 (SSK-DEC-001): clips at each wick's high and low ends, no adhesive. | Holds the strip without sealing its face; R10 (removal) stays open. Clips let the wicks lift out for rinsing. |
| P12 | Ribs ran to the plate edge, across the new tongue mouths. | Ribs stop 8 mm short of the tongue tips. | Condensate reaches the distillate tongues unobstructed. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Yield | Wet wick fraction 0.824 to 0.817; design-day yield 10.6 L and gained output ratio 1.26 to 1.34 unchanged at the precision quoted. Low-end vapor loss 25 mL per day (0.2 %). | Wicks stop 13 mm inside the zigzag edge. |
| Mass | Panel 18.7 kg dry (was 16.7), 22.7 kg wet; stand 8.9 kg, with the wick clips, PPS rails and stop blocks. R9 (20 kg dry) still met. | Base ring, trim, tongues, brackets. |
| Cost | Value-engineering target: USD 355. Estimated cost of the constructable design: USD 443.20 (USD 88.20 over the target, after the decisions of 2026-10-02 added USD 27); the concept priced at USD 351.20. New BOM lines 15 to 19; lines 2 to 5, 8, 11 and 12 respecified. | Larger plate blanks, trim, stand ground frame, brackets, closure. |
| Footprint and wind | 1.28 x 1.25 m at 10 deg (was 1.28 x 1.16 m); lift equals weight at 18.7 m/s (was 17.5 m/s). | Props sit outside the posts. |
| Drawings | SSK-DWG-002 Rev P4; making sketches SSK-DWG-101 to 120 added (119 and 120 are the wick clips); concept blueprint SSK-DWG-001 Rev P5. | Follow the model. |
| Documents | SSK-CAL-001 v0.6, SSK-PRC-001 v0.8, SSK-REQ-001 v0.8. R12 is reported against the value-engineering target; R10 moved from at risk to met on paper when the wick clips were modelled. | Follow the model. |

*Table 3. Items proposed to Amish; decided on 2026-10-02 (A1 as recommended, A2 as option (c)).*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | How brine leaves the low edge without reaching the distillate (R4; part of the safety case, because brine in the distillate is a drinking-water hazard). | (a) zigzag edges with distillate tongues at the rib lines and brine tongues at the strip centres, as modelled (P3); (b) a cross-wick along the low edge of each stage that carries brine sideways to tails at the side walls; (c) leave the low edge as in the concept and test the brine exit separately at TRL 4. | (a): it keeps the concept's layout (brine over the closed manifold lid into an outboard, lower gutter) and every brine path at least 10 mm from every distillate path. Confirm by measuring each stage's distillate conductivity at TRL 4. Accepted 2026-10-02: each stage's distillate conductivity test is a pass condition at TRL 4 before any water is drunk; the cross-wick (b) is the fallback. |
| A2 | The feed tails leave each wick at the high edge 6 mm above the condensing plate below; if a tail sags or drips there, feed water could reach a condensing face (found in this review; R4, safety case). | (a) accept for the first prototype and measure each stage's distillate conductivity at TRL 4; (b) stagger the plates' high edges about 22 mm per level so each tail leaves clear of the plate below (costs about 4 % of the yield); (c) a 4 mm downturned lip on each condensing plate's high edge. | (a), with (c) as the first fix if the conductivity test shows carryover. Decided 2026-10-02 as (c) now: a 4 mm downturned lip, bent before coating, dropped only if TRL 4 conductivity tests without it show no carryover. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan SSK-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`), and the design decisions register SSK-DEC-001 lists A1, A2 and the other open items.
- Exceptions accepted on 2026-10-02: the high-edge lip of A2 (c) and the wick clips that replace P11's silicone dots are carried into the model, the plate and wick sketches, the BOM and the build plan pictures (2026-10-02). The lip is four 7 mm tabs on the rib lines of each condensing plate, not a full-width lip, because the wicks of the plate pass out of the same edge; the base ring has four slots for the bottom plate's tabs.
- Requirement status is unchanged except that R12 is now reported against the value-engineering target: none not met, five at risk (R2, R4, R6, R7, R8), one not verifiable at TRL 3 (R3), five met on paper (R1, R5, R9, R10, R11), and R12 USD 88.20 over the target.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` are being redone: the appearance model now follows the constructable design and the render scenes are exported; the images are made on Amish's Mac, where Blender is.
- The plate tongues stay straight until the manifold and gutter are fitted, then are bent by hand (build plan steps 15 and 17).
