"""StillStack STEM check calculations (SSK-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv and the claims table in docs/01b-stem-check.md (between the
STM_TABLE markers). The CAL numbers come from docs/04-calcs/sizing.py (SSK-CAL-001); every row also has
an independent first-order check written here, so a CAL error shows up as a disagreement.

Option A is the current design (four-stage wick still). Option B is the single-effect tilted wick still of
SSK-OPT-001; its first-order numbers are computed in option_b() below and quoted in the options document.
Row S11 failed at first run (printed polycarbonate rails in stage 3 at 110 C calm-air stagnation against a
113 C short-term softening point) and is closed by the fix of SSK-DEC-001 D-01 (PPS rails in stage 3,
decided 2026-10-24 under Amish's standing instruction of 2026-10-23); the row below checks the fixed design.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "docs/04-calcs")]
from stem_check import Check, limits, G, SIGMA, WITHIN, PLAUSIBLE, FIX  # noqa: E402,F401
import sizing as S  # noqa: E402

c = Check(ROOT / "docs/04-calcs/stem_results.csv")
P = S.P
DOC = ROOT / "docs/01b-stem-check.md"

# ------------------------------------------------------------------ CAL results (SSK-CAL-001)
dd = S.design_day()
H = P["H_day_kwh"] * 3.6           # MJ/m2/day
E_sun, E_abs, E_top, E_edge = dd["E_sun"] / 1e6, dd["E_abs"] / 1e6, dd["E_top"] / 1e6, dd["E_edge"] / 1e6
st_in = dd["stage_in"] / 1e6
yield_qs = dd["yield"]
noon = dd["peak"]
dry = S.solve_stack(1000.0, Ta=35.0, dry=True)
dry_calm = S.solve_stack(1000.0, Ta=35.0, dry=True, v=0.0)
_, (t_in_calm, _) = S.q_top(dry_calm["Tp"][0], 35.0, 0.0)
rib = S.rib_design()
HFG = S.hfg(60.0) / 1e6            # MJ/kg at a mean stage temperature
C_STACK = 5 * 2700 * P["plate_t"] * 900 + 4 * 1.0 * S.CP_W + 4 * 0.25 * 1300 + 1.3 * 1200   # J/K per m2, as CAL-001 section 5
warm = C_STACK * (noon["Tp"].mean() - P["T_amb"]) / 1e6   # MJ, CAL-001 section 5
yield_net = yield_qs * (1 - warm / E_abs)   # CAL-001 section 5: the stored heat would have been reused in every stage

# ------------------------------------------------------------------ Physics: thermodynamics and heat transfer
c.balance("S1", f"Consistency check: stage 1 takes no more heat than the absorber keeps after top and edge losses ({st_in[0]:.1f} of {E_abs:.1f} MJ/m2 absorbed)",
          "Physics", "Thermodynamics",
          inputs={"absorbed": E_abs}, outputs={"top loss": E_top, "edge loss": E_edge, "into stage 1": st_in[0]}, unit="MJ/m2",
          law="First law at the absorber node; a check of the solver's integration, not an independent result (independent review)")
cross1 = st_in[0] - dd["stage_sens"][0] / 1e6
c.balance("S2", f"Consistency check: stage 2 takes in no more than the heat crossing gap 1 ({st_in[1]:.1f} of {cross1:.1f} MJ/m2)", "Physics", "Thermodynamics",
          inputs={"crossing gap 1": cross1}, outputs={"into stage 2": st_in[1]}, unit="MJ/m2",
          law="First law: heat into stage 2 is the latent, conducted, radiated and rib heat crossing gap 1, less edge loss (like quantities)")
gor = dd["GOR"]
c.claim("S3", f"Gained output ratio {gor:.2f} quasi-steady ({gor * yield_net / yield_qs:.2f} after warm-up) is below the ideal limit for four stages",
        "Physics", "Thermodynamics", law="Ideal multi-effect still: GOR <= N x tau x alpha (every effect reuses all the heat, no losses)",
        value=round(gor, 2), limit=P["n_stages"] * P["tau"] * P["alpha"], unit="", rule="below")
c.claim("S4", f"Daily distillate {yield_net:.1f} L/m2 ({yield_qs:.1f} L quasi-steady) on a 5.5 kWh/m2 day (an upper-bound screen only)",
        "Physics", "Thermodynamics",
        law="Multi-effect upper bound: N stages x single-stage evaporation limit at tau alpha (limits.evaporation_kg_per_m2_day)",
        value=round(yield_qs, 1), limit=P["n_stages"] * limits.evaporation_kg_per_m2_day(P["H_day_kwh"], P["tau"] * P["alpha"]),
        unit="L/m2/day", rule="below")
# independent order-of-magnitude: Fick diffusion across a 6 mm gap at 60 C wick face, 5 K across the gap
Tw, Tc = 60.0, 55.0
Tm = 0.5 * (Tw + Tc) + 273.15
D_va = 2.6e-5 * (Tm / 298.0) ** 1.75                     # m2/s, water vapour in air (Bird, Stewart and Lightfoot)
cw = S.A_W * S.psat(Tw) * 0.018 / (8.314 * (Tw + 273.15))   # brine water activity (CAL v0.8)
cc = S.psat(Tc) * 0.018 / (8.314 * (Tc + 273.15))
stefan = 1 / (1 - 0.5 * (S.A_W * S.psat(Tw) + S.psat(Tc)) / 101325)
q_fick = D_va * (cw - cc) / P["gap"] * stefan * S.hfg(57.5)
q_cal, *_ = S.gap_flux(60.0, 55.0)
c.order_of_magnitude("S5", f"Latent flux across a 6 mm gap with 5 K across it is about {q_cal:.0f} W/m2 at a 60 C brine-wet wick face (water activity {S.A_W:.3f})",
                     "Physics", "Heat transfer", claimed=round(q_cal), estimate=q_fick, unit="W/m2",
                     law="Fick diffusion with the Stefan flow correction, independent property fits; cf. Chiavazzo et al. 2018")
q_cond = 0.028 / P["gap"] * 5.0
c.order_of_magnitude("S6", "Conduction across the still 6 mm gap is about 23 W/m2 at 5 K (Nu = 1, heated from above)", "Physics", "Heat transfer",
                     claimed=23.4, estimate=q_cond, unit="W/m2", law="Fourier conduction, k air 0.028 W/mK; stable stratification (Incropera, ch. 9)")
# bottom heat rejection: effective h per m2 of aperture against natural convection plus radiation over the finned area
# Before the independent review the CAL used a 5 W/m2K floor for the sheltered underside and a bare (0.10) surface: 9.8
# W/m2K claimed against 5.5 estimated (ratio 1.77). Corrected in CAL v0.8 (laminar flat plate) and fixed in the design by
# SSK-DEC-001 D-07 (underside and fins painted matte black, emissivity 0.90); the row checks the corrected, fixed design.
dTb = noon["Tp"][-1] - P["T_amb"]
h_claim = noon["q_bot"] / dTb
area_ratio = S.fin_area() / S.A
Tf = 0.5 * (noon["Tp"][-1] + P["T_amb"]) + 273.15
h_nat = 0.27 * (9.81 / Tf * dTb / (1.8e-5) ** 2 * 0.71 * 0.342) ** 0.25 * 0.028       # facing down (Incropera eq. 9.32)
h_frc = 0.664 * (0.5 / 1.8e-5) ** 0.5 * 0.89 * 0.028                                    # laminar, 0.5 m/s under the panel
h_est = (h_nat + h_frc) * area_ratio * 0.85 + 0.90 * 4 * SIGMA * Tf ** 3
c.order_of_magnitude("S7", f"Painted fins and underside reject the peak {noon['q_bot']:.0f} W/m2 at {dTb:.0f} K above ambient (effective {h_claim:.1f} W/m2K per m2 of aperture)",
                     "Physics", "Heat transfer", claimed=round(h_claim, 1), estimate=h_est, unit="W/m2K",
                     law="Downward-facing natural plus laminar forced convection over the finned area, radiation at emissivity 0.90 (Incropera)",
                     closed_by="SSK-DEC-001 D-07 (painted underside and fins; CAL v0.8)")
# dry stagnation: absorber at 1,000 W/m2, 35 C, with an independent two-path loss estimate
U_top = 5.5
gap_U = 0.028 / P["gap"] + 4 * SIGMA * 0.86 * (380.0) ** 3
U_down = 1 / (4 / gap_U + 1 / h_claim)
T_stag_est = 35.0 + P["tau"] * P["alpha"] * 1000.0 / (U_top + U_down)
c.order_of_magnitude("S8", f"Dry stagnation holds the absorber near {dry['Tp'][0]:.0f} C ({dry_calm['Tp'][0]:.0f} C in calm air) at 1,000 W/m2 and 35 C",
                     "Physics", "Heat transfer", claimed=round(dry["Tp"][0] - 35.0), estimate=T_stag_est - 35.0, unit="K above ambient",
                     law="Absorbed flux = (U top + U down) x rise; U top about 5.5 W/m2K, four dry gaps and the fins in series below")
# ------------------------------------------------------------------ Physics: strength of materials and statics
E_al = 69e9
I_strip = P["plate_t"] ** 3 / 12
q_plate = rib["w"] if "w" in rib else 22.6
sag = 5 * 22.6 * 0.194 ** 4 / (384 * E_al * I_strip / (1 - 0.33 ** 2)) * 1000   # plate stiffness, as CAL
c.claim("S9", "0.5 mm plates sag about 0.5 mm between ribs at 194 mm pitch, under one sixth of the 6 mm gap",
        "Physics", "Strength of materials", law="Simply supported strip, w = 5 q L^4 / 384 E I, aluminium E 69 GPa, 22.6 N/m2",
        value=round(sag, 2), limit=P["sag_allow"] * 1000, unit="mm", rule="below")
grow = 1.0 * 23e-6 * 60 * 1000
c.claim("S10", "A plate grows about 1.4 mm across 1 m at a 60 K rise, inside the 2 mm clearance each side",
        "Physics", "Strength of materials", law="Linear expansion, aluminium 23e-6 /K", value=round(grow, 2), limit=2 * P["plate_clear"] * 1000,
        unit="mm", rule="below")
# S11: stage 3 rail polymer at calm-air stagnation. First run: printed PC, 110 C + 10 K margin against 113 C (ISO 75, 0.45 MPa,
# Prusament PC Blend) failed. Fixed by SSK-DEC-001 D-01: PPS (long-term service 218 C, Tecatron/Techtron 1000 PPS datasheet).
T_st3 = dry_calm["Tp"][2]
c.claim("S11", f"Stage 3 side rails survive calm-air dry stagnation ({T_st3:.0f} C) with at least 10 K margin",
        "Physics", "Strength of materials",
        law="Long-term service temperature in air: PPS 218 C (Mitsubishi Chemical Tecatron 1000 PPS); printed PC softens at 113 C (ISO 75, 0.45 MPa)",
        value=round(T_st3) + 10, limit=218.0, unit="C", rule="below", closed_by="SSK-DEC-001 D-01 (PPS rails in stage 3)")
c.claim("S12", f"Stage 1 and 2 PPS rails and silicone ribs survive {dry_calm['Tp'][0]:.0f} C calm-air stagnation",
        "Physics", "Strength of materials", law="PPS long-term service 218 C (datasheet); silicone rubber cord rated about 200 C (supplier class)",
        value=round(dry_calm["Tp"][0]) + 10, limit=200.0, unit="C", rule="below")
c.claim("S13", f"The inner twin-wall glazing sheet stays below its service limit at calm-air stagnation ({t_in_calm:.0f} C)",
        "Physics", "Strength of materials", law="Twin-wall polycarbonate service temperature -40 to 120 C (Multicraft TW6C624 data)",
        value=round(t_in_calm), limit=120.0, unit="C", rule="below", margin=0.10,
        closed_by="Kept with the stagnation cover and shade rule as the barrier, the rule on the panel label (SSK-DEC-001 D-05, decided by Amish 2026-10-25)")
F_wind = 0.5 * 1.2 * 17.0 ** 2 * 1.2 * (P["aperture"] + 2 * P["wall"]) ** 2
wet = 22.7
Fp = math.hypot(wet * G, F_wind) / 2
f_h = 0.11 * (1 - 0.01 * 10) * 500.0
c.claim("S14", "M10 pivot bolt bearing on 12 mm plywood is about 1.4 MPa with the wet panel and 17 m/s wind",
        "Physics", "Mechanics and statics", law="Embedment strength of plywood f_h = 0.11 (1 - 0.01 d) rho_k (EN 1995-1-1, eq. 8.20), rho_k 500 kg/m3",
        value=round(Fp / (0.010 * 0.012) / 1e6, 1), limit=f_h, unit="MPa", rule="below")
Pcr = math.pi ** 2 * 8e9 * (0.045 ** 4 / 12) / 1.0 ** 2
c.claim("S15", "A 45 x 45 mm timber prop, 1.0 m pinned, does not buckle under the panel and wind load (about 0.4 kN)",
        "Physics", "Mechanics and statics", law="Euler buckling, softwood E 8 GPa", value=0.4, limit=Pcr / 1e3, unit="kN", rule="below")
# S16 (rewritten after the independent review): tipping, not lift, governs. Wind from behind on the underside pushes the
# panel up and toward the low edge; the unanchored stand tips about the front end of its ground frame.
sys.path.insert(0, str(ROOT / "cad/src"))
import model as MW  # noqa: E402
A_w = (P["aperture"] + 2 * P["wall"]) ** 2
W_tot = (22.8 + 8.9) * G
sg_ = MW.stand_geometry()
x_front = sg_["pivot"][0] + 1.5 * MW.PARAMS["post"]
x_rear = sg_["pivot"][0] - MW.PARAMS["rail_rear"]
xc, zc = MW.to_world(0.0, 15.0)
xg = (22.8 * xc + 8.9 * 0.5 * (x_front + x_rear)) / (22.8 + 8.9)
b_ = math.radians(P["tilt_deg"])
arm_o = (math.cos(b_) * (x_front - xc) + math.sin(b_) * zc) / 1000
arm_r = (x_front - xg) / 1000
v_tip = math.sqrt(W_tot * arm_r / (0.5 * 1.2 * 1.2 * A_w * arm_o))
# D-09 (a), decided by Amish 2026-10-25: anchoring is a hold point and PR-013 is stated for the anchored stand. Unanchored it
# tips at v_tip; with 40 kg of ballast on the rear of the ground rails (or the four stakes) it holds well past 17 m/s.
arm_b = (x_front - x_rear) / 1000
v_tip_b = math.sqrt((W_tot * arm_r + 40.0 * G * arm_b) / (0.5 * 1.2 * 1.2 * A_w * arm_o))
c.claim("S16", f"Anchored (four stakes or 40 kg of ballast, a hold point), the panel and stand do not tip below 17 m/s of wind (PR-013); unanchored it tips at {v_tip:.1f} m/s",
        "Physics", "Mechanics and statics",
        law="Moment balance about the front end of the ground frame: normal force 0.5 rho v^2 Cf A (Cf 1.2) at the panel centre against the wet weight plus 40 kg of ballast at the rear of the ground rails",
        value=17.0, limit=round(v_tip_b, 1), unit="m/s", rule="below",
        closed_by="SSK-DEC-001 D-09 (decided by Amish 2026-10-25); stake pull-out in soft or sandy ground to check at TRL 5")
# ------------------------------------------------------------------ Physics: fluid mechanics (wick feed)
c.cited("S17", "A 1 mm wick carries the 1.44 kg/h per metre of width that stage 1 needs at noon if its permeability is 3.0e-11 m2 or more",
        "Physics", "Fluid mechanics", law="Darcy flow, gravity along 20 deg plus 4 kPa capillary pressure (SSK-CAL-001 section 6)",
        detail="Needed 3.0e-11 m2; permeability of the shortlisted fabrics not yet measured (wicking-rise test, SSK-DEC-001)", verdict=PLAUSIBLE)
lift_head = 1.0
c.claim("S18", "The gravity feed needs no pump: the trough rim is at most 1.00 m above the ground at 35 deg", "Engineering and technology",
        "Power and link budgets", law="Hydrostatic head from a user-filled container at most 1.5 m (R5)", value=lift_head, limit=1.5, unit="m", rule="below")
# ------------------------------------------------------------------ Chemistry
sat = 317.0
brine = P["feed_salinity_max"] * P["FR"] / (P["FR"] - 1)
c.claim("S19", f"Brine leaves at {brine:.1f} g/L from 40 g/L feed at a feed ratio of 2.5, so salt stays in solution",
        "Chemistry", "Physical chemistry", law="Salt mass balance; NaCl saturation about 317 g/L of solution at 25 to 80 C (CRC Handbook)",
        value=round(brine, 1), limit=sat, unit="g/L", rule="below")
c.cited("S20", "Dissolved salt does not evaporate with the vapour, so distillate salinity comes only from liquid carryover",
        "Chemistry", "Physical chemistry", law="Raoult's law; NaCl is non-volatile at still temperatures",
        detail="The 8.2 mL/day of SSK-CAL-001 section 7 is an allowance for 50 mg/L, not a computed carryover (rows S29, PR-003); volatile organics can carry over (PRC safety)",
        verdict=WITHIN)
c.claim("S34", f"Brine lowers the wick's vapour pressure (water activity {S.A_W:.3f} at the mean wick salinity of {S.S_MEAN:.0f} g/L), now in the CAL",
        "Chemistry", "Physical chemistry", law="Raoult's law with an osmotic coefficient of 0.93 for NaCl (CAL v0.8, added after the independent review)",
        value=round(S.A_W, 3), limit=1.0, unit="", rule="below")
c.cited("S21", "Bare 3003 or 1050 aluminium plate undersides survive contact with hot (60 to 80 C) brine-wet wicks for years",
        "Chemistry", "Electrochemistry and batteries",
        law="3000 and 5000 series aluminium resists seawater to 125 C; crevice corrosion under gaskets is the main concern (Kappes 2017); 1050 resists better than 3003 (Dumitrascu et al. 2016)",
        detail="The wick under its clips is a crevice in 58 to 67 g/L brine; no crevice rate at 60 to 80 C found; a perforation would let brine reach the distillate face",
        verdict=PLAUSIBLE, closed_by="Corrosion coupon test in the TRL 4 plan, 1050 preferred over 3003; 5052 plates if the coupons show crevice attack (SSK-DEC-001 D-04, decided by Amish 2026-10-25)")
c.cited("S22", "The fluoropolymer coating on the condensing faces is food-contact safe in hot salty distillate and tolerates 150 C dry",
        "Chemistry", "Materials and polymer chemistry", law="PTFE and PFA are stable well above 150 C; drinking-water contact needs an NSF/ANSI/CAN 61 or equivalent certificate",
        detail="Coating class chosen, certified product not yet seen (SSK-DEC-001, to confirm item 8)", verdict=PLAUSIBLE)
# ------------------------------------------------------------------ Biology
c.cited("S23", "Distillate is a raw product and is not claimed safe to drink without testing and disinfection",
        "Biology", "Microbiology", law="WHO Guidelines for Drinking-water Quality, 4th ed. with first and second addenda (2022)",
        detail="Stages run at 58 to 80 C, below pasteurization certainty; brine carryover can carry microbes; test (conductivity, E. coli) and disinfect (PRC safety)",
        verdict=WITHIN)
c.cited("S24", "Long-term drinking of distillate needs remineralization; low dissolved solids are not a health target",
        "Biology", "Human physiology and biomechanics",
        law="WHO, Nutrients in Drinking Water (2005), on demineralized and desalinated water; WHO TDS fact sheet: no health-based value",
        detail="50 mg/L is used as a carryover check only (PRS PR-003)", verdict=WITHIN)
c.cited("S25", "The wick fabric tolerates 150 C dry without losing its wicking, and conducts like the k 0.45 W/mK the CAL assumes",
        "Chemistry", "Materials and polymer chemistry",
        law="Polyester nonwovens soften well below their 250 C melt; glass-fibre fabric is stable far above 150 C; cellulose (cotton, viscose) degrades with time at 140 C",
        detail="Fabric chosen by the wicking-rise test between a polyester-type nonwoven and a glass-fibre fabric (SSK-DEC-001, 2026-10-02); the CAL's k and dry mass are cotton or viscose values", verdict=PLAUSIBLE)
c.cited("S29", "Brine does not drip from the wick onto the condensing face below, and condensate drops do not bridge the 6 mm gap to the wick",
        "Physics", "Fluid mechanics",
        law="Capillary retention in an unsaturated wick; sessile drops on a 20 deg face slide at a few mm (capillary length 2.7 mm), below the 6 mm gap",
        detail="A wick fed past its capacity or a hydrophobic (fluoropolymer) face holding pinned drops could carry brine across; per-stage conductivity at TRL 4 decides", verdict=PLAUSIBLE)
c.cited("S30", "The 5052 aluminium wick clips survive in hot brine and do not attack the aluminium plates",
        "Chemistry", "Electrochemistry and batteries",
        law="Galvanic series in seawater: stainless steel is about 0.5 V nobler than aluminium, so the 304 clips first chosen drove aluminium corrosion; 5052 is a marine alloy within the same aluminium group as 1050 and 3003, so the couple is negligible",
        detail="The clips touch bare plate in 58 to 67 g/L brine at 60 to 80 C. Fixed by D-08 (a), decided by Amish 2026-10-25: clips bent from 5052-H32 strip 0.4 x 8 mm, same shape; the crevice under the clip stays with S21 and the TRL 4 coupon test",
        verdict=WITHIN, closed_by="SSK-DEC-001 D-08")
c.cited("S31", "Carbonate and sulphate scale on the wicks stays within weekly rinsing", "Chemistry", "Inorganic chemistry",
        law="Seawater concentrated 1.7 times at 60 to 80 C exceeds calcium carbonate saturation; calcium sulphate stays below saturation at that factor",
        detail="Scale rate not computed; the weekly rinse (PR-010) and a vinegar soak are the controls; the wicking-rise test should be repeated on a scaled wick", verdict=PLAUSIBLE)
c.cited("S32", "Adhesives, glazing tape and sealant survive their stagnation temperatures", "Chemistry", "Materials and polymer chemistry",
        law="High-temperature silicone adhesives and sealants are commonly rated about 200 to 260 C; the fins sit at about 64 C, the tape under the glazing edge near the inner sheet (113 C calm)",
        detail="Products not yet named; check each datasheet when buying (SSK-DEC-001, to confirm item 6)", verdict=PLAUSIBLE)
c.cited("S33", "The glazing passes about 0.80 of the sun (solar-weighted, with incidence and dust losses)", "Physics", "Optics and radiation",
        law="The 80 % of the source is a light transmission; solar-weighted values with incidence-angle loss and soiling are likely 0.72 to 0.78 (independent review)",
        detail="At 0.75 the design day gives 10.1 L quasi-steady (CAL sensitivity), so PR-001 is met only near 0.80; measure the sheet at TRL 4", verdict=PLAUSIBLE)
# ------------------------------------------------------------------ Mathematics
dd_half = S.design_day(dt_h=0.125)
c.claim("S26", "The design-day integration is resolved in time: halving the 15 min step moves the daily yield by under 1 %", "Mathematics", "Numerical method",
        law=f"Quasi-steady fsolve over a 10 h sine day (SSK-CAL-001 section 1); noon solution converged: {noon['ok']}",
        value=round(abs(dd_half["yield"] - yield_qs) / yield_qs * 100, 3), limit=1.0, unit="%", rule="below")
c.order_of_magnitude("S27", f"{yield_net:.1f} L/m2/day is two to three times a single-basin still (3 to 5 L/m2/day)", "Mathematics", "Orders of magnitude",
                     claimed=round(yield_net, 1), estimate=4.0 * 2.5, unit="L/m2/day", law="Basin still 3 to 5 L/m2/day (SSK-PRB-001) times a gained-output gain of 2 to 3")
c.order_of_magnitude("S28", "Vapour lost through the low-end tongue openings is about 25 mL/day (0.2 % of the yield)", "Physics", "Fluid mechanics",
                     claimed=25.0, estimate=4 * 2.9e-5 * (0.13 - 0.018) * (0.54 * 0.006) / 0.05 * 1.25 * 0.6 * 36000 * 1000, unit="mL/day",
                     law="Fick diffusion through the openings, 4 gaps, 60 C inside, 30 C at 60 % RH outside")


# ------------------------------------------------------------------ Option B: single-effect tilted wick still
def option_b():
    """First-order numbers of option B (SSK-OPT-001): one black wick on an insulated backboard under a 4 mm glass cover."""
    tau_g, alpha_w = 0.85, 0.92            # 4 mm float glass (typical), black cloth wick
    eta = 0.45                             # daily efficiency, inside the 0.35 to 0.57 reported for wick stills
    y = H * eta / HFG
    U_top_b, U_back = 6.5, 0.9
    T_stag = 35.0 + tau_g * alpha_w * 1000.0 / (U_top_b + U_back)
    return dict(tau_alpha=tau_g * alpha_w, eta=eta, yield_L=y, area_for_10L=10.0 / y, T_stag=T_stag)


B = option_b()
c.claim("B1", f"Option B makes about {B['yield_L']:.1f} L/m2/day at an assumed (not computed) 45 % daily efficiency on the 5.5 kWh/m2 day",
        "Physics", "Thermodynamics", law="Single-effect limit: evaporation <= tau alpha x sun / h_fg (limits.evaporation_kg_per_m2_day)",
        value=round(B["yield_L"], 1), limit=limits.evaporation_kg_per_m2_day(P["H_day_kwh"], B["tau_alpha"]), unit="L/m2/day", rule="below")
c.order_of_magnitude("B2", f"Option B yield of {B['yield_L']:.1f} L/m2/day matches tilted wick stills in the literature", "Mathematics", "Orders of magnitude",
                     claimed=round(B["yield_L"], 1), estimate=4.77, unit="L/m2/day", law="Sharon et al., tilted wick and basin still, 4.54 and 4.99 L/m2/day (cited in Agrawal and Rana 2019)")
c.claim("B3", f"Option B wick survives dry stagnation (about {B['T_stag']:.0f} C) only with a 150 C fabric",
        "Physics", "Heat transfer", law="Absorbed flux = (U top 6.5 + U back 0.9) x rise, single glazing",
        value=round(B["T_stag"]), limit=150.0, unit="C", rule="below", margin=0.10)
c.cited("B4", "Condensate runs down the underside of a 20 deg glass cover to the low-edge gutter as a film", "Physics", "Fluid mechanics",
        law="Clean glass is wetted by water (low contact angle), so film-wise condensation drains along the slope; standard in tilted stills",
        detail="20 deg is above the 10 to 15 deg usually needed for drops to run on clean glass", verdict=WITHIN)


def fill_doc(rows):
    if not DOC.exists():
        return
    head = "| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    body = "".join(f"| {r['id']} | {r['claim']} | {r['field']} | {r['branch']} | {r['law']} | {r['check']} | {r['verdict']} | {r['closed_by'] or 'Open'} |\n"
                   for r in rows)
    t = DOC.read_text(encoding="utf-8")
    t = re.sub(r"<!-- STM_TABLE -->.*?<!-- /STM_TABLE -->", "<!-- STM_TABLE -->\n" + head + body + "<!-- /STM_TABLE -->", t, flags=re.S)
    DOC.write_text(t, encoding="utf-8")


if __name__ == "__main__":
    c.rows.sort(key=lambda r: (r["id"][0] != "S", int(r["id"][1:])))
    state = c.write()
    fill_doc(c.rows)
    for r in c.rows:
        print(f"{r['id']:>4}  {r['verdict']:<32} {r['check']}")
    print(f"Option B: tau alpha {B['tau_alpha']:.2f}, {B['yield_L']:.2f} L/m2/day, {B['area_for_10L']:.1f} m2 for 10 L, stagnation {B['T_stag']:.0f} C")
    print(f"Dry stagnation calm plate temperatures: {', '.join(f'{t:.0f}' for t in dry_calm['Tp'])} C; inner glazing {t_in_calm:.0f} C")
