# BOM notes

Prices are indicative TRL 3 estimates by supplier type, not quotes. Line numbers match the callouts in `media/exploded.png`; line 13 (sealant, fasteners and tubing) is not modeled.

Parts total **$317.20** for one 1 m2 prototype (checked by `docs/04-calcs/sizing.py`, section 13). That is **$67.20 over** the $250 budget in `project.yaml`, which Amish kept on 2026-09-25 (SSK-DDR-001), so R12 is not met. The budget is not changed here. The increase over the TRL 2 estimate of $241 comes from:

- 16 silicone-cord spacer ribs (line 7, $19.20), which SSK-CAL-001 shows are needed to hold the 6 mm gaps;
- printed polycarbonate side rails priced by filament mass (line 6, $28.00);
- a $5 per plate allowance for the food-contact coating (line 5);
- a PIR foam liner and paint in the frame (line 2, $35.00);
- pivot hardware, pins and anchors for the adjustable stand (line 12, $21.00).

The largest cost is still the five aluminum plates with coating (lines 3 and 5, $108). Choosing 316 stainless steel plates instead would add roughly $100 to $150 more.

Every part that touches distillate (lines 5, 7, 9 and 13) must be food-contact rated. Rails (line 6) must be polycarbonate: ASA and PETG soften below the dry stagnation temperature of stages 1 to 3 (about 106 to 140 °C).
