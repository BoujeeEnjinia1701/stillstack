---
doc_id: SSK-REG-001
title: StillStack regulatory and standards register
project: StillStack
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First register (kit 1.9.1 upgrade); sources checked 2026-10-24
---

# StillStack regulatory and standards register

StillStack makes water that people may drink, so two sets of rules matter most: what may touch drinking water, and what may be claimed about the water. The open design is not placed on a market, and no claim of potability is made (SSK-PRB-001, out of scope). This register is not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Method: STANDARDS section 23. Sources checked 2026-10-24. No other Water Security repo in the portfolio has a regulatory register yet to share (PotPress covers filter factories, not stills).

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | WHO Guidelines for Drinking-water Quality, 4th edition incorporating the first and second addenda (2022) | International (guidance) | Microbial, chemical and acceptability guidance for drinking water | The reference for testing distillate before drinking (E. coli, conductivity) and for disinfection and safe storage (PRC safety, STEM S23) | Design lead; partner lab | Applies as guidance |
| G2 | WHO chemical fact sheet, total dissolved solids | International (guidance) | No health-based guideline value for TDS; acceptability only | PR-003 uses 50 mg/L as a carryover check, not a health limit; remineralization note (STEM S24) | Design lead | Applies as guidance |
| G3 | NSF/ANSI/CAN 61, drinking water system components, health effects (2023 edition listed by the Standards Council of Canada) | United States and Canada | Contaminants that leach from materials in contact with drinking water | The coating on the condensing faces, silicone sealant and channels (PR-007). The coater must supply a certificate before the order (SSK-DEC-001, to confirm item 8) | Builder; coater | To assess: no certified coating product seen yet |
| G4 | NSF/ANSI 51, food equipment materials | United States | Materials for food equipment | Alternative listing for the silicone sealant and cord (PR-007) | Builder | To assess per product |
| G5 | Directive (EU) 2020/2184 on water intended for human consumption, Article 11 (materials in contact) and its implementing acts | European Union | Minimum hygiene requirements for materials and products in contact with drinking water | Only if a panel is sold or supplied as a drinking-water product in the EU | Whoever places it on the market | Does not apply to the open design; certification needed later for any EU supply |
| G6 | Regulation (EC) No 1935/2004, food contact materials | European Union | General safety and labelling of materials meant to contact food | Reference for the PP and HDPE channels and the distillate container | Builder | To assess per product |
| G7 | ISO 9806:2017, solar energy, solar thermal collectors, test methods | International | Collector tests including exposure, internal shock and stagnation behaviour | Method reference for a TRL 4 dry stagnation test of PR-008 (on hold under the TRL 3 cap); StillStack is not a heating collector | Partner lab | Applies as a test-method reference later |
| G8 | EN 1995-1-1 (Eurocode 5), design of timber structures | Europe (design values) | Embedment strength of timber and plywood at dowel-type fasteners | Pivot bolt bearing on 12 mm plywood (STEM S14) | Design lead | Applies; used as a design value |
| G9 | EN 1991-1-4 (Eurocode 1), wind actions | Europe (design values) | Wind pressure and force coefficients | Wind overturning check of PR-013 uses a force coefficient of 1.2 as a first-order value; site wind not assessed | Design lead | To assess for a named site |
| G10 | National rules on household water treatment claims and brine discharge in the partner's country | Partner country | What a household water product may claim; where brine may go | Instructions and any field trial | Partner NGO | To assess when a field partner is chosen |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- World Health Organization. *Guidelines for Drinking-Water Quality: Fourth Edition Incorporating the First and Second Addenda.* Geneva: WHO, 2022. https://www.who.int/publications/i/item/9789240045064 (checked 2026-10-24).
- World Health Organization. "Chemical Fact Sheets: Total Dissolved Solids." https://www.who.int/publications/m/item/chemical-fact-sheets--total-dissolved-solids (checked 2026-10-24).
- Standards Council of Canada. "NSF/ANSI/CAN 61 - 2023." Standards database. https://scc-ccn.ca/standardsdb/standards/4032142 (checked 2026-10-24).
- European Union. Directive (EU) 2020/2184 of the European Parliament and of the Council of 16 December 2020 on the Quality of Water Intended for Human Consumption, Article 11. https://www.legislation.gov.uk/eudr/2020/2184/article/11 (checked 2026-10-24).
- European Union. Regulation (EC) No 1935/2004 on Materials and Articles Intended to Come into Contact with Food. https://eur-lex.europa.eu/eli/reg/2004/1935/oj (checked 2026-10-24).
- International Organization for Standardization. *ISO 9806:2017, Solar Energy: Solar Thermal Collectors; Test Methods.* IEA SHC guide: https://www.iea-shc.org/Data/Sites/1/publications/Guide-to-Standard-ISO-9806-2017.pdf (checked 2026-10-24).
- CEN. *EN 1995-1-1, Eurocode 5: Design of Timber Structures, Part 1-1.* Equation 8.20, embedment strength of plywood.
- CEN. *EN 1991-1-4, Eurocode 1: Actions on Structures, Part 1-4: Wind Actions.*
