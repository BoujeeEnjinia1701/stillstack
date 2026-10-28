---
doc_id: SSK-PLN-001
title: StillStack project plan
project: StillStack
doc_type: Project plan
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First project plan (kit 1.9.1 upgrade), with the reference list of every source cited in the repo
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Decisions of 2026-10-25 recorded (D-04 to D-06, D-08 to D-10); coupon test scope (D-04); prototype parts USD 460.70'
---

# StillStack project plan

StillStack is at stage P3 (design outputs, TRL 3): model detailed to D3 for both concept options, drawings, priced BOM, build plan, decisions register, design FMEA and traceability exist. The next gate is P4 (verification, TRL 4), which stays on hold under the portfolio cap. Decision requested from Amish: the concept selection D-03 (options A and B are within 10 %, sent without a pick). D-04, D-05, D-06, D-08, D-09 and D-10 were decided by Amish on 2026-10-25 (SSK-DEC-001). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept and science | Design lead | STEM check SSK-STM-001, concept options SSK-OPT-001, DDR-004 | Done at P3; STEM open (ten plausible rows, two fixes with Amish); selection awaiting Amish |
| Requirements and traceability | Design lead | SSK-URS-001, SSK-PRS-001, SSK-RTM-001 | Done at P3 |
| Calculations | Design lead | SSK-CAL-001 v0.8 (`sizing.py`, `stem_check.py`), corrected after the independent review | Done at P3 |
| Detailed design | Design lead | `cad/src/model.py` at D3 for options A and B, STEP per part and per assembly, drawings SSK-DWG-002 and 101 to 120 | Done at P3 |
| Build plan | Design lead | SSK-BLD-001 | Done at P3 (a plan, not a record) |
| Regulatory, risk and market | Design lead | SSK-REG-001, SSK-RSK-001, SSK-MKT-001 | First pass at P3 |
| Partner | Amish | Approach the first candidate lab (Politecnico di Torino group) | Not started; Amish's decision |
| Verification (P4) | Partner lab | Wicking-rise test, coupon corrosion test of 1050 or 3003 plate, wick and 5052 clip in hot brine (D-04), stake pull-out check at the site (D-09, TRL 5), stagnation test (ISO 9806 method), per-stage conductivity, outdoor yield beside a basin still | On hold (TRL 3 cap) |

## Resources needed

Table 2. Resources (P4 and later on hold; costs are not estimated until the cap is lifted).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Prototype parts | One panel and stand (BOM) | One builder, about a week | 460.70 (BOM) |
| Partner lab time | Distillate quality and yield tests | To assess with the lab | To assess |
| Coater | Certified food-contact coating on four plates | One batch | About 20 in the BOM; certificate cost to assess |
| Field partner | Household trial (P5) | To assess | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users and stakeholders, STM, OPT, REG, FEA, PLN | Done (2026-10-24) |
| P1 Definition | URS, PRS, RSK with hazard analysis, MKT | Done (2026-10-24) |
| P2 Design inputs | PRS targets and verification, CAL, RTM, concept selection DDR | Done; the selection itself awaits Amish (D-03) |
| P3 Design outputs | Model at D3, STEP, drawings, priced BOM, BLD, DEC, design FMEA, traceability | Done (2026-10-24) |
| P4 Verification | Test plans and reports, verification report | On hold (TRL 3 cap) |
| P5 Validation | Field trial with a partner, certification status | On hold |
| P6 Commercialization | Only with a named deployment partner | On hold |

## Next steps and decision requested

1. Amish decides D-03 (concept selection); D-04 to D-06 and D-08 to D-10 were decided on 2026-10-25 (SSK-DEC-001).
2. The coordinator renders `media/options.png` and the product views in `RENDER_VIEWS` in Blender Cycles on Amish's Mac.
3. When the cap is lifted: approach the partner lab, then the TRL 4 tests listed above, starting with the wicking-rise test (it decides PR-001 and PR-006).

## References

- AM Nautical. "Aquamate Inflatable Solar Still Desalinator, Liferaft." https://amnautical.com/products/aquamate-inflatable-solar-still-desalinator-liferaft (checked 2026-10-24).
- Agrawal, Abhay, and R. S. Rana. "Theoretical and Experimental Performance Evaluation of Single-Slope Single-Basin Solar Still with Multiple V-Shaped Floating Wicks." *Heliyon* 5, no. 4 (2019): e01525. https://pmc.ncbi.nlm.nih.gov/articles/PMC6479174 (checked 2026-10-24).
- Chiavazzo, Eliodoro, Matteo Morciano, Francesca Viglino, Matteo Fasano, and Pietro Asinari. "Passive Solar High-Yield Seawater Desalination by Modular and Low-Cost Distillation." *Nature Sustainability* 1 (2018): 763 to 772. https://doi.org/10.1038/s41893-018-0186-x.
- Dumitrascu, Valentin Marian, Camelia Staicu, and Lidia Benea. "Corrosion Behavior of 1050 and 3003 Aluminum Alloys Used in Naval Industry." *Annals of "Dunarea de Jos" University of Galati, Fascicle IX, Metallurgy and Materials Science* (2016). https://gup.ugal.ro/ugaljournals/index.php/mms/article/view/1263 (checked 2026-10-24).
- European Union. Directive (EU) 2020/2184 on the Quality of Water Intended for Human Consumption. https://www.legislation.gov.uk/eudr/2020/2184/article/11 (checked 2026-10-24).
- European Union. Regulation (EC) No 1935/2004 on Food Contact Materials. https://eur-lex.europa.eu/eli/reg/2004/1935/oj (checked 2026-10-24).
- Farm Show Magazine. Article on the SolAqua Rainmaker 550 solar still. 2021, vol. 45, no. 6, p. 28. https://farmshow.com/a_article.php?aid=37586 (checked 2026-10-24).
- Filament2Print. "Prusament PC Blend" (softening temperature 113 °C, ISO 75 at 0.45 MPa). https://filament2print.com/en/pc-polycarbonate/3457-prusament-pc-blend.html (checked 2026-10-24).
- Incropera, Frank P., David P. DeWitt, Theodore L. Bergman, and Adrienne S. Lavine. *Fundamentals of Heat and Mass Transfer.* 6th ed. Hoboken, NJ: Wiley, 2007.
- Kappes, Mariano. *Localized Corrosion of Aluminum Alloy 5052 for Desalination Service.* AMPP (NACE) paper 9151, 2017. https://store.ampp.org/localized-corrosion-of-aluminum-alloy-5052-for-desalination-service (checked 2026-10-24).
- Mitsubishi Chemical Advanced Materials. "Tecatron 1000 PPS" datasheet (maximum service temperature in air 218 °C, long term). Polymershapes, 2020. https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Tecatron-1000-PPS.pdf (checked 2026-10-24).
- Multicraft Plastics. "6 mm Clear Twinwall Polycarbonate, TW6C624" (service temperature -40 to 248 °F, light transmission 80 %). https://multicraftplastics.com/product/TW6C624 (checked 2026-10-24).
- Ruffino and others (2022), Texas Water Development Board, World Bank (2015 and blogs) and WHO and UNICEF (2025): cited with links in the README.
- Standards Council of Canada. "NSF/ANSI/CAN 61 - 2023." https://scc-ccn.ca/standardsdb/standards/4032142 (checked 2026-10-24).
- World Health Organization. *Guidelines for Drinking-Water Quality: Fourth Edition Incorporating the First and Second Addenda.* Geneva: WHO, 2022. https://www.who.int/publications/i/item/9789240045064 (checked 2026-10-24).
- World Health Organization. *Nutrients in Drinking Water.* Geneva: WHO, 2005.
- World Health Organization. "Chemical Fact Sheets: Total Dissolved Solids." https://www.who.int/publications/m/item/chemical-fact-sheets--total-dissolved-solids (checked 2026-10-24).
- Xu, Zhenyuan, and others. "Ultrahigh-Efficiency Desalination via a Thermally-Localized Multistage Solar Still." *Energy and Environmental Science* 13 (2020): 830 to 839. https://dspace.mit.edu/handle/1721.1/123794 (checked 2026-10-24).
- International Organization for Standardization. *ISO 9806:2017.* IEA SHC guide: https://www.iea-shc.org/Data/Sites/1/publications/Guide-to-Standard-ISO-9806-2017.pdf (checked 2026-10-24).
- CEN. *EN 1995-1-1* (Eurocode 5) and *EN 1991-1-4* (Eurocode 1, wind).
