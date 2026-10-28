# BOM notes

Prices are indicative TRL 3 estimates by supplier type, not quotes. Line numbers match the callouts in `media/exploded.png`; line 6 is split into two rows by stage, lines 13 (sealant, fasteners and tubing), 14 (stagnation cover) and 19 (labels) are not modeled, and line 18 (wick clips) is shown with the wicks (line 4).

Value-engineering target: USD 355 (`budget_usd` in `project.yaml`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 460.70 (USD 105.70 over the target), 20 lines, checked by `docs/04-calcs/sizing.py`, section 13. Panel mass about 18.8 kg dry. Every made or bought part of option A in `cad/src/model.py` carries its BOM line number (kit 1.9, checked by `.kit/cad_check.py`); line 13 covers the stainless screws drawn in the model and line 12 the stand bolts, corner plates and stakes.

Changes under Amish's decisions of 2026-10-25 ("i concur with your recommendations", SSK-DEC-001):

- the wick clips (line 18) are 5052-H32 aluminium strip in place of 304 stainless (D-08); the USD 0.35 a clip is still the stainless basis, kept as an estimate until 5052 strip is priced;
- the labels (line 19) go from two to three, adding a panel label with the stagnation cover rule (D-05), +USD 1.50 at the same indicative price per label.

Changes under SSK-DDR-002 (decided by Amish, 2026-09-25, going with the recommendations):

- the four side rails in stages 1 and 2 (line 6) are now a polymer rated to 150 °C or more (PPS or a high-heat polycarbonate copolymer), at an allowance of $9.00 each in place of $3.50 (+$22.00); the product is not yet selected;
- the frame liner (line 2) is foil-faced stone wool in place of PIR, at the same price;
- a stagnation cover (line 14, $12.00) is added;
- the silicone-cord ribs (line 7, $19.20) are now decided.

The largest cost is still the five aluminum plates with coating (lines 3 and 5, $108). Choosing 316 stainless steel plates instead would add roughly $100 to $150 more.

Every part that touches distillate (lines 5, 7, 9 and 13) must be food-contact rated. The stage 4 rails stay printed polycarbonate (91 °C at calm-air dry stagnation against a 113 °C softening point); ASA and PETG soften below the dry stagnation temperature of stages 1 to 3 (about 110 to 144 °C in calm air).

Carried into the BOM on 2026-10-02 (SSK-DEC-001):

- the stage 1 and 2 rails (line 6) are natural (tan) PPS, 4 rails at $11.50 (+$10.00 over the $9.00 allowance). Basis: a 7 x 70 x 1000 mm length (about 0.66 kg) at about USD 70 per kg list price for natural PPS sheet gives about $46; this is a distributor list price, not a quote, so a sheet quote is still to be obtained (register item 7 to confirm). The two stop blocks are cut from the offcut. The stage 3 and 4 rails are printed in teal polycarbonate so the two kinds never swap;
- the coating (line 5, and the paint in line 3 is unchanged) is a fluoropolymer (PTFE or PFA type) cookware coating applied by a coater to the top face of the four condenser plates, kept at the $5 per plate allowance; the coater must supply an NSF/ANSI 61 or equivalent certificate for hot salty water, rated to 150 °C dry, before the order, otherwise plates 1 and 2 move to 316 stainless (roughly +$100 to $150 for the pair, register item 8); no named product has been verified;
- the wick fabric (line 4) is chosen by a wicking-rise test between a polyester-type nonwoven and a glass-fibre fabric; the test is TRL 4 work, so line 4 keeps its indicative price;
- the wick clips (line 18): 40 of 0.4 x 8 mm 304 stainless strip, bent by hand, 0.35 each ($14.00; one 6 m coil at about $14 retail gives the 5.5 m needed), replacing the silicone dots; no adhesive;
- DISTILLATE and BRINE labels (line 19), 2 at $1.50;
- the lip on each condensing plate's high edge is a bend (no sheet or price change).

Silicone strip in place of the 150 °C rails is not a saving to take, because it would undo the R8 materials decision.

Carried into the BOM on 2026-10-24 (kit 1.9.1 upgrade, SSK-DEC-001):

- D-01: the stage 3 rails (line 6) are PPS like stages 1 and 2, so line 6 has 6 PPS rails at $11.50 and 2 printed rails at $3.50 (+$16.00). The fix closes STEM row S11 and was decided under Amish's standing instruction of 2026-10-23. Six rails need two 70 mm lengths or one 100 mm strip of 7 mm sheet; the pro rata price is not a quote;
- D-02: the stand hardware (line 12) is two M10 x 75 pivot bolts, two M10 x 120 hinge bolts and two M10 x 120 foot pins with wing nuts (the 10 and 15 deg holes go through the gussets), four galvanised corner plates and four stakes; the line price is unchanged.
