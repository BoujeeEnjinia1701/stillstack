# BOM notes

Prices are indicative TRL 3 estimates by supplier type, not quotes. Line numbers match the callouts in `media/exploded.png`; line 6 is split into two rows by stage, and lines 13 (sealant, fasteners and tubing) and 14 (stagnation cover) are not modeled.

Parts total **$351.20** for one 1 m2 prototype (checked by `docs/04-calcs/sizing.py`, section 13). The budget in `project.yaml` was raised from $250 to $320 by Amish on 2026-09-25 (SSK-DDR-002) and topped up to **$355** on 2026-09-26, so the BOM is **$3.80 under** and R12 is met.

Changes under SSK-DDR-002 (decided by Amish, 2026-09-25, going with the recommendations):

- the four side rails in stages 1 and 2 (line 6) are now a polymer rated to 150 °C or more (PPS or a high-heat polycarbonate copolymer), at an allowance of $9.00 each in place of $3.50 (+$22.00); the product is not yet selected;
- the frame liner (line 2) is foil-faced stone wool in place of PIR, at the same price;
- a stagnation cover (line 14, $12.00) is added;
- the silicone-cord ribs (line 7, $19.20) are now decided.

The largest cost is still the five aluminum plates with coating (lines 3 and 5, $108). Choosing 316 stainless steel plates instead would add roughly $100 to $150 more.

Every part that touches distillate (lines 5, 7, 9 and 13) must be food-contact rated. The rails in stages 3 and 4 may stay printed polycarbonate; ASA and PETG soften below the dry stagnation temperature of stages 1 to 3 (about 110 to 144 °C in calm air).
