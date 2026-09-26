#!/usr/bin/env python3
"""StillStack sizing calculations (SSK-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py

First-principles, quasi-steady energy balance of a four-stage passive wick still
on a tilted 1 m2 aperture, plus structural, salt, wick-transport, stagnation,
mass, geometry and cost checks. Every number quoted in 01-sizing.md is printed here.

Model summary
  * Stack: absorber plate (node 0), four stages, bottom plate (node 4) with air fins.
    Stage k: wet wick under plate k-1, vapor gap, condensing face of plate k.
  * Gap transfer: Stefan diffusion of vapor through air (latent), conduction through
    still air (the gap is heated from above, so it is stably stratified, Nu = 1),
    and gray-body radiation between parallel plates.
  * Top loss: resistance network absorber -> 25 mm air layer (Hollands correlation)
    -> twin-wall polycarbonate -> wind and sky.
  * Bottom: convection from plate and fins plus radiation to the ground.
  * Feed enters at ambient; each stage heats its own feed (feed-to-distillate
    ratio FR) to the wick temperature. That sensible heat is lost with the brine.
  * Hourly quasi-steady solution over a sinusoidal design day; thermal mass is
    treated as a warm-up deduction.
"""
from __future__ import annotations
import csv
import math
from pathlib import Path

import numpy as np
from scipy.optimize import fsolve, brentq

ROOT = Path(__file__).resolve().parents[2]
SIG = 5.670e-8          # W/m2K4
R_U = 8.314             # J/mol K
M_W = 0.018015          # kg/mol
P_ATM = 101325.0        # Pa
G_ACC = 9.81            # m/s2

# ---------------------------------------------------------------- parameters
P = dict(
    # geometry (match cad/src/model.py)
    aperture=1.0,           # m, square aperture side
    n_stages=4,
    gap=0.006,              # m, vapor gap between wick face and condensing face
    wick_t=0.001,           # m
    plate_t=0.0005,         # m, aluminum plates
    air_gap=0.025,          # m, absorber to glazing
    tilt_deg=20.0,
    fin_n=10, fin_depth=0.030, fin_len=0.96,
    # optics
    tau=0.80,               # 6 mm twin-wall clear polycarbonate, typical solar transmittance
    alpha=0.95,             # high-temperature matte black paint
    # emissivities
    eps_abs=0.90, eps_pc=0.90, eps_wick=0.95, eps_cond=0.90, eps_bottom=0.10,   # bottom: bare rolled aluminum underside and fins
    h_twin=9.3,             # W/m2K across the twin-wall cells (from a typical U of 3.6 W/m2K less surface films)
    # site and design day
    H_day_kwh=5.5,          # kWh/m2/day on the tilted aperture
    day_len_h=10.0,         # effective sunshine hours of the sinusoidal profile
    T_amb=30.0,             # degC, mean daytime ambient
    wind=1.0,               # m/s, light wind
    # wick and feed
    k_wick=0.45,            # W/mK, wet cotton or viscose nonwoven
    FR=2.5,                 # feed-to-distillate ratio (R6 minimum)
    feed_salinity=35.0,     # g/L seawater
    feed_salinity_max=40.0, # g/L, R6 upper bound
    # edges
    U_edge=1.07,            # W/m2K, 12 mm plywood + 25 mm foil-faced stone wool (k about 0.035) + surface films
    stage_h=0.008,          # m of frame wall per stage
    # spacer ribs
    rib_w=0.007,            # m, silicone cord rib diameter
    plate_clear=0.002,      # m, plate clearance to the frame each side (thermal growth)
    wall=0.037,             # m, 12 mm plywood plus 25 mm stone wool
    wick_break=0.010,       # m, dry break each side of a rib (R4 air break)
    rail_w=0.012,           # m, side rail width (150 degC polymer in stages 1 and 2, printed PC in 3 and 4)
    budget=355.0,           # USD, project.yaml budget_usd (DDR-002 v0.2, 2026-09-26)
    rating_hot=150.0,       # degC, R8 rating for materials in stages 1 and 2 (DDR-002)
    rating_cool=110.0,      # degC, R8 rating for all other internal materials
    sag_allow=0.001,        # m, allowed plate sag (one sixth of the gap)
)
A = P["aperture"] ** 2
BETA = math.radians(P["tilt_deg"])


# ---------------------------------------------------------------- properties
def psat(T):
    """Saturation pressure of water, Pa (Buck 1981), T in degC."""
    return 611.21 * math.exp((18.678 - T / 234.5) * (T / (257.14 + T)))


def hfg(T):
    """Latent heat of vaporization, J/kg (linear fit, 0 to 100 degC)."""
    return (2501.0 - 2.361 * T) * 1e3


def k_air(T):
    return 0.0241 * ((T + 273.15) / 273.15) ** 0.81


def nu_air(T):
    return 1.33e-5 * ((T + 273.15) / 273.15) ** 1.75


def d_va(T):
    """Diffusivity of water vapor in air, m2/s."""
    return 2.26e-5 * ((T + 273.15) / 273.15) ** 1.81


CP_W = 4180.0


# ---------------------------------------------------------------- gap transfer
F_GAP = 1.0 / (1 / P["eps_wick"] + 1 / P["eps_cond"] - 1)


def gap_flux(Tw, Tc, phi=1.0, dry=False):
    """Heat flux terms across one vapor gap per m2 of aperture.
    Tw: wick face temperature, Tc: condensing face temperature (degC).
    phi: fraction of area with wet wick. Returns (q_latent, q_cond, q_rad, m_evap kg/s)."""
    Tm = 0.5 * (Tw + Tc)
    TK = Tm + 273.15
    if dry or Tw <= Tc:
        m = 0.0
    else:
        p1 = min(psat(min(Tw, 99.0)), 0.99 * P_ATM)
        p2 = min(psat(min(Tc, 99.0)), p1)
        m = P_ATM * M_W * d_va(Tm) / (R_U * TK * P["gap"]) * math.log((P_ATM - p2) / (P_ATM - p1))
        m *= phi
    q_lat = m * hfg(Tw)
    q_cond = k_air(Tm) / (P["gap"] + (1 - phi) * P["wick_t"]) * (Tw - Tc)
    q_rad = F_GAP * SIG * ((Tw + 273.15) ** 4 - (Tc + 273.15) ** 4)
    return q_lat, q_cond, q_rad, m


# ---------------------------------------------------------------- top loss
def hollands_nu(Ra, beta):
    """Nusselt number for an inclined air layer heated from below (Hollands et al. 1976)."""
    rc = Ra * math.cos(beta)
    a = max(0.0, 1 - 1708 / rc) if rc > 0 else 0.0
    b = 1 - 1708 * (math.sin(1.8 * beta)) ** 1.6 / rc if rc > 0 else 0.0
    c = max(0.0, (rc / 5830) ** (1 / 3) - 1)
    return 1 + 1.44 * a * b + c


def h_wind(v, L=1.0):
    return max(5.0, 8.6 * v ** 0.6 / L ** 0.4)


def q_top(Tp, Ta, v):
    """Top heat loss W/m2 from an absorber at Tp through the air layer and twin-wall glazing."""
    Tsky = 0.0552 * (Ta + 273.15) ** 1.5 - 273.15
    Fs, Fg = (1 + math.cos(BETA)) / 2, (1 - math.cos(BETA)) / 2
    hw = h_wind(v)

    def resid(x):
        Tc1, Tc2 = x
        Tm = 0.5 * (Tp + Tc1)
        L = P["air_gap"]
        Ra = G_ACC * (1 / (Tm + 273.15)) * max(Tp - Tc1, 0.01) * L ** 3 / nu_air(Tm) ** 2 * 0.71
        hc = hollands_nu(Ra, BETA) * k_air(Tm) / L
        hr = SIG * ((Tp + 273.15) ** 2 + (Tc1 + 273.15) ** 2) * ((Tp + 273.15) + (Tc1 + 273.15)) / (
            1 / P["eps_abs"] + 1 / P["eps_pc"] - 1)
        q1 = (hc + hr) * (Tp - Tc1)
        q2 = P["h_twin"] * (Tc1 - Tc2)
        q3 = hw * (Tc2 - Ta) + P["eps_pc"] * SIG * (
            Fs * ((Tc2 + 273.15) ** 4 - (Tsky + 273.15) ** 4) + Fg * ((Tc2 + 273.15) ** 4 - (Ta + 273.15) ** 4))
        return [q1 - q2, q2 - q3], q1

    x = fsolve(lambda x: resid(x)[0], [Ta + 0.5 * (Tp - Ta), Ta + 0.2 * (Tp - Ta)])
    return resid(x)[1], x


# ---------------------------------------------------------------- bottom rejection
def fin_area():
    return A + P["fin_n"] * 2 * P["fin_depth"] * P["fin_len"]


def q_bottom(Tb, Ta, v, eps=None):
    """Heat rejected from the bottom plate underside and fins, W per m2 of aperture."""
    eps = P["eps_bottom"] if eps is None else eps
    dT = max(Tb - Ta, 1e-3)
    Tf = 0.5 * (Tb + Ta)
    L = 1.0 / math.cos(0)  # slope length of the plate, m
    # natural convection, heated surface facing down, 70 deg from vertical (Fujii and Imura)
    Ra = G_ACC * dT / (Tf + 273.15) * L ** 3 / nu_air(Tf) ** 2 * 0.71
    h_nat = 0.56 * (Ra * math.cos(math.pi / 2 - BETA)) ** 0.25 * k_air(Tf) / L
    # sheltered wind under the panel at half the free-stream speed
    h_frc = h_wind(0.5 * v)
    h_c = (h_nat ** 3 + h_frc ** 3) ** (1 / 3)
    # fin efficiency, 0.5 mm aluminum, 30 mm deep
    m = math.sqrt(2 * h_c / (205 * P["plate_t"]))
    eta = math.tanh(m * P["fin_depth"]) / (m * P["fin_depth"])
    A_conv = A + eta * (fin_area() - A)
    q_conv = h_c * A_conv * dT
    q_rad = eps * SIG * ((Tb + 273.15) ** 4 - (Ta + 273.15) ** 4) * A   # projected area sees the ground
    return (q_conv + q_rad) / A


# ---------------------------------------------------------------- spacer ribs and plate sag
def rib_design():
    """Rib pitch so that a 0.5 mm plate with a wet wick sags no more than sag_allow between ribs."""
    E, t = 69e9, P["plate_t"]
    EI = E * t ** 3 / 12 / (1 - 0.33 ** 2)          # plate bending stiffness per m width
    w = (2700 * t + 1.0 + 0.1) * G_ACC * math.cos(BETA)   # plate + wet wick (1.0 kg/m2) + condensate film, N/m2
    span_free = P["aperture"] - 2 * P["plate_clear"] - 2 * P["rail_w"]     # clear span between side rails
    sag_free = 5 * w * span_free ** 4 / (384 * EI)
    s_max = (384 * EI * P["sag_allow"] / (5 * w)) ** 0.25   # simply supported strip, conservative
    n_spans = math.ceil(span_free / s_max)
    n_ribs = n_spans - 1
    pitch = span_free / n_spans
    sag = 5 * w * pitch ** 4 / (384 * EI)
    wet_w = span_free - n_ribs * P["rib_w"] - 2 * (n_ribs + 1) * P["wick_break"]
    wet_l = P["aperture"] - 2 * P["plate_clear"] - 0.020        # wick stops 20 mm short of the low edge
    phi = wet_w * wet_l / P["aperture"] ** 2
    # thermal expansion of a plate relative to the frame
    dL = 23e-6 * P["aperture"] * 60.0
    return dict(EI=EI, w=w, sag_free=sag_free, s_max=s_max, n_ribs=n_ribs, pitch=pitch, sag=sag,
                phi=phi, dL=dL)


RIB = rib_design()


# ---------------------------------------------------------------- stack solver
def solve_stack(G, Ta=None, v=None, n=None, FR=None, phi=None, dry=False, eps_bottom=None, guess=None):
    """Quasi-steady stack solution at irradiance G (W/m2). Returns a dict of temperatures and fluxes."""
    Ta = P["T_amb"] if Ta is None else Ta
    v = P["wind"] if v is None else v
    n = P["n_stages"] if n is None else n
    FR = P["FR"] if FR is None else FR
    phi = RIB["phi"] if phi is None else phi
    S = P["tau"] * P["alpha"] * G
    Rw = P["wick_t"] / P["k_wick"]
    rib_cond = (RIB["n_ribs"] * P["rib_w"] + 2 * P["rail_w"]) * 0.20 / (P["gap"] + P["wick_t"])   # W/K per m2, ribs and rails, k about 0.2 W/mK
    q_edge = lambda T: P["U_edge"] * 4 * P["aperture"] * P["stage_h"] * (T - Ta)

    def unpack(x):
        return x[:n + 1], x[n + 1:]

    def resid(x):
        Tp, Tw = unpack(x)
        r = []
        qt, _ = q_top(Tp[0], Ta, v)
        r.append(S - qt - q_edge(Tp[0]) - (Tp[0] - Tw[0]) / Rw)
        gaps = []
        for k in range(n):
            ql, qc, qr, m = gap_flux(Tw[k], Tp[k + 1], phi, dry)
            qrib = rib_cond * (Tw[k] - Tp[k + 1])
            sens = 0.0 if dry else FR * m * CP_W * (Tw[k] - Ta)
            gaps.append((ql, qc, qr, qrib, m, sens))
            r.append((Tp[k] - Tw[k]) / Rw - (ql + qc + qr + qrib + sens))
        for k in range(1, n):
            ql, qc, qr, qrib, m, sens = gaps[k - 1]
            r.append(ql + qc + qr + qrib - q_edge(Tp[k]) - (Tp[k] - Tw[k]) / Rw)
        ql, qc, qr, qrib, m, sens = gaps[-1]
        r.append(ql + qc + qr + qrib - q_edge(Tp[n]) - q_bottom(Tp[n], Ta, v, eps_bottom))
        return r, gaps, qt

    if guess is None:
        hot = 0.10 if dry else 0.045
        Tp0 = np.linspace(Ta + hot * G, Ta + 0.02 * G, n + 1)
        guess = np.concatenate([Tp0, Tp0[:-1] - 0.5])
    x, info, ier, msg = fsolve(lambda x: resid(x)[0], guess, full_output=True)
    r, gaps, qt = resid(x)
    Tp, Tw = unpack(x)
    m = [g[4] for g in gaps]
    return dict(Tp=Tp, Tw=Tw, gaps=gaps, q_top=qt, S=S, m=m, ok=(ier == 1 and max(abs(np.array(r))) < 1e-3),
                q_bot=q_bottom(Tp[n], Ta, v, eps_bottom), x=x,
                sens=[g[5] for g in gaps], edge=sum(q_edge(T) for T in Tp))


def design_day(n=None, FR=None, phi=None, H_kwh=None, v=None, eps_bottom=None, dt_h=0.25):
    """Integrate a sinusoidal design day. Returns daily totals."""
    H = (P["H_day_kwh"] if H_kwh is None else H_kwh) * 3.6e6
    D = P["day_len_h"] * 3600
    Gmax = H * math.pi / (2 * D)
    t = np.arange(dt_h / 2, P["day_len_h"], dt_h) * 3600
    tot = dict(E_sun=0.0, E_abs=0.0, E_top=0.0, E_sens=0.0, E_edge=0.0, E_bot=0.0, E_lat=0.0,
               stage=np.zeros(n or P["n_stages"]), stage_in=np.zeros(n or P["n_stages"]),
               stage_sens=np.zeros(n or P["n_stages"]), T0max=0.0, Tbmax=0.0, Gmax=Gmax, peak=None)
    guess = None
    for ti in t:
        G = Gmax * math.sin(math.pi * ti / D)
        s = solve_stack(G, n=n, FR=FR, phi=phi, v=v, eps_bottom=eps_bottom, guess=guess)
        guess = s["x"]
        dt = dt_h * 3600
        tot["E_sun"] += G * dt
        tot["E_abs"] += s["S"] * dt
        tot["E_top"] += s["q_top"] * dt
        tot["E_sens"] += sum(s["sens"]) * dt
        tot["E_edge"] += s["edge"] * dt
        tot["E_bot"] += s["q_bot"] * dt
        tot["stage"] += np.array(s["m"]) * dt
        tot["stage_in"] += np.array([sum(g[:4]) + g[5] for g in s["gaps"]]) * dt
        tot["stage_sens"] += np.array([g[5] for g in s["gaps"]]) * dt
        tot["E_lat"] += sum(g[0] for g in s["gaps"]) * dt
        if s["Tp"][0] > tot["T0max"]:
            tot["T0max"], tot["Tbmax"], tot["peak"] = s["Tp"][0], s["Tp"][-1], s
    tot["yield"] = tot["stage"].sum()           # kg/m2/day
    tot["GOR"] = tot["E_lat"] / tot["E_sun"]
    return tot


# ---------------------------------------------------------------- helpers
def line(label, value, unit=""):
    print(f"  {label:<58s} {value:>12s} {unit}")


def f(x, d=1):
    return f"{x:,.{d}f}"


def main():
    print("StillStack SSK-CAL-001 sizing results")
    print("=" * 78)

    # 1. Solar resource and optics
    Hj = P["H_day_kwh"] * 3.6
    D = P["day_len_h"] * 3600
    Gmax = P["H_day_kwh"] * 3.6e6 * math.pi / (2 * D)
    print("\n1. Solar resource and optics")
    line("Daily irradiation on aperture", f(Hj, 1), "MJ/m2")
    line("Peak irradiance of sinusoidal day (10 h)", f(Gmax, 0), "W/m2")
    line("Transmittance x absorptance", f(P["tau"] * P["alpha"], 3))
    line("Optical loss per day", f(Hj * (1 - P["tau"] * P["alpha"]), 1), "MJ/m2")

    # 2. Gap transfer and evaporation fraction
    print("\n2. Vapor gap transfer, 6 mm gap, 5 K across the gap")
    print(f"  {'Wick T (degC)':>14s} {'latent W/m2':>12s} {'cond W/m2':>10s} {'rad W/m2':>9s} {'evap fraction':>14s}")
    for Tw in (40, 50, 60, 70, 80):
        ql, qc, qr, m = gap_flux(Tw, Tw - 5, phi=1.0)
        print(f"  {Tw:>14d} {ql:>12.0f} {qc:>10.1f} {qr:>9.1f} {ql / (ql + qc + qr):>14.2f}")

    # 3. Spacer ribs
    print("\n3. Plate support and spacer ribs")
    line("Load on plate (plate, wet wick, condensate), normal", f(RIB["w"], 1), "N/m2")
    line("Sag of the 0.972 m free span (beam theory)", f(RIB["sag_free"] * 1000, 0), "mm")
    line("Maximum rib pitch for 1.0 mm sag", f(RIB["s_max"] * 1000, 0), "mm")
    line("Intermediate ribs per gap", str(RIB["n_ribs"]))
    line("Rib pitch used", f(RIB["pitch"] * 1000, 0), "mm")
    line("Sag at that pitch", f(RIB["sag"] * 1000, 2), "mm")
    line("Wet wick area fraction after rib breaks", f(RIB["phi"], 3))
    line("Plate thermal growth, 1 m at 60 K rise", f(RIB["dL"] * 1000, 2), "mm")

    # 4. Design day
    dd = design_day()
    pk = dd["peak"]
    print("\n4. Design day, 4 stages, FR 2.5, wind 1 m/s, 30 degC ambient, bare underside")
    line("Distillate per stage", ", ".join(f"{x:.2f}" for x in dd["stage"]), "L/m2/day")
    line("Total distillate", f(dd["yield"], 1), "L/m2/day")
    line("Gained output ratio (latent in distillate / sun)", f(dd["GOR"], 2))
    line("Absorbed", f(dd["E_abs"] / 1e6, 1), "MJ/m2")
    line("Top loss", f(dd["E_top"] / 1e6, 1), "MJ/m2")
    line("Feed sensible heat lost with brine", f(dd["E_sens"] / 1e6, 1), "MJ/m2")
    line("Edge loss", f(dd["E_edge"] / 1e6, 2), "MJ/m2")
    line("Heat rejected at the bottom", f(dd["E_bot"] / 1e6, 1), "MJ/m2")
    line("Heat into each stage wick", ", ".join(f"{x / 1e6:.1f}" for x in dd["stage_in"]), "MJ/m2")
    line("Feed sensible heat per stage", ", ".join(f"{x / 1e6:.2f}" for x in dd["stage_sens"]), "MJ/m2")
    line("Peak absorber temperature", f(pk["Tp"][0], 1), "degC")
    line("Peak plate temperatures", ", ".join(f"{t:.1f}" for t in pk["Tp"]), "degC")
    line("Peak heat rejected at the bottom", f(pk["q_bot"], 0), "W/m2")
    line("Peak bottom plate rise above ambient", f(pk["Tp"][-1] - P["T_amb"], 1), "K")
    ev = [g[0] / (g[0] + g[1] + g[2] + g[3]) for g in pk["gaps"]]
    line("Evaporation fraction per stage at noon", ", ".join(f"{e:.2f}" for e in ev))
    line("Top loss at noon", f(pk["q_top"], 0), "W/m2")
    line("Solver converged at noon", str(pk["ok"]))

    # thermal mass warm-up deduction
    C = 5 * 2700 * P["plate_t"] * 900 + 4 * 1.0 * CP_W + 4 * 0.25 * 1300 + 1.3 * 1200
    dT_w = pk["Tp"].mean() - P["T_amb"]
    E_warm = C * dT_w
    y_adj = dd["yield"] * (1 - E_warm / dd["E_abs"])
    print("\n5. Thermal mass")
    line("Stack heat capacity (plates, wet wicks, glazing)", f(C / 1e3, 1), "kJ/K per m2")
    line("Warm-up energy to mean noon stack temperature", f(E_warm / 1e6, 2), "MJ/m2")
    line("Distillate after warm-up deduction", f(y_adj, 1), "L/m2/day")
    line("Gained output ratio after warm-up deduction", f(dd["GOR"] * y_adj / dd["yield"], 2))

    # sensitivity
    print("\n6. Sensitivity (daily distillate, L/m2/day; GOR)")
    cases = [("3 stages", dict(n=3)), ("4 stages (base)", dict()), ("6 stages", dict(n=6)),
             ("No rib breaks (phi = 1)", dict(phi=1.0)), ("FR 3.5", dict(FR=3.5)),
             ("Wind 3 m/s", dict(v=3.0)), ("Painted underside (eps 0.90)", dict(eps_bottom=0.90)),
             ("Sunny day 6.5 kWh/m2", dict(H_kwh=6.5)), ("Hazy day 4.5 kWh/m2", dict(H_kwh=4.5))]
    sens = {}
    for name, kw in cases:
        d = design_day(**kw)
        sens[name] = d
        print(f"  {name:<40s} {d['yield']:>6.1f} L   GOR {d['GOR']:.2f}   peak absorber {d['T0max']:.0f} degC"
              f"   peak bottom {d['Tbmax']:.0f} degC")

    # 7. Stagnation and hot operation
    print("\n7. Temperatures at 1,000 W/m2 and 35 degC ambient, wind 1 m/s")
    wet = solve_stack(1000.0, Ta=35.0)
    dry = solve_stack(1000.0, Ta=35.0, dry=True)
    dry_calm = solve_stack(1000.0, Ta=35.0, dry=True, v=0.0)
    line("Wet operation: absorber, bottom plate", f"{wet['Tp'][0]:.1f}, {wet['Tp'][-1]:.1f}", "degC")
    line("Dry stagnation: absorber (stage 1 spacers, wick 1)", f(dry["Tp"][0], 1), "degC")
    line("Dry stagnation: plate temperatures", ", ".join(f"{t:.0f}" for t in dry["Tp"]), "degC")
    _, (tc1, tc2) = q_top(dry["Tp"][0], 35.0, 1.0)
    line("Dry stagnation: inner and outer glazing sheet", f"{tc1:.0f}, {tc2:.0f}", "degC")
    line("Dry stagnation, calm air: absorber", f(dry_calm["Tp"][0], 1), "degC")
    line("Dry stagnation, calm air: plate temperatures", ", ".join(f"{t:.0f}" for t in dry_calm["Tp"]), "degC")
    _, (tc1c, _) = q_top(dry_calm["Tp"][0], 35.0, 0.0)
    line("Dry stagnation, calm air: inner glazing sheet", f(tc1c, 0), "degC")
    # R8 as restated in DDR-002: stages 1 and 2 (absorber to plate 2) rated 150 degC, the rest 110 degC
    hot = max(dry["Tp"][0], dry_calm["Tp"][0])
    cool = max(dry["Tp"][2], dry_calm["Tp"][2])
    line("R8: hottest stage 1 and 2 material vs 150 degC rating", f"{hot:.0f} vs {P['rating_hot']:.0f}", "degC")
    line("R8: margin in stages 1 and 2", f(P["rating_hot"] - hot, 0), "K")
    line("R8: hottest stage 3 and 4 material vs 110 degC rating", f"{cool:.0f} vs {P['rating_cool']:.0f}", "degC")
    line("R8: margin in stages 3 and 4", f(P["rating_cool"] - cool, 0), "K")

    # 8. Wick feed capacity
    print("\n8. Wick feed capacity (stage 1 at noon)")
    m_peak = pk["m"][0]                       # kg/m2/s
    q_need = P["FR"] * m_peak * P["aperture"]  # kg/s per m width, 1 m slope length
    mu = 0.55e-3                              # Pa s, water near 50 degC
    grad = 1000 * G_ACC * math.sin(BETA) + 4000.0 / P["aperture"]   # gravity plus 4 kPa capillary pressure over 1 m
    k_need = q_need * mu / (1000 * P["wick_t"] * grad)
    line("Stage 1 evaporation at noon", f(m_peak * 3600, 2), "kg/m2/h")
    line("Feed needed per m of wick width (FR 2.5)", f(q_need * 3600, 2), "kg/h")
    line("Driving gradient (gravity at 20 deg plus capillary)", f(grad, 0), "Pa/m")
    line("Wick permeability needed", f"{k_need:.1e}", "m2")
    for kp in (1e-11, 3e-11, 1e-10):
        cap = kp * 1000 * P["wick_t"] * grad / mu * 3600
        line(f"Capacity with permeability {kp:.0e} m2", f(cap, 2), "kg/h per m")

    # 9. Salt balance and carryover
    print("\n9. Salt balance and carryover")
    for c in (P["feed_salinity"], P["feed_salinity_max"]):
        cb = c * P["FR"] / (P["FR"] - 1)
        line(f"Brine salinity at FR 2.5, feed {c:.0f} g/L", f(cb, 1), "g/L")
    cb = P["feed_salinity_max"] * P["FR"] / (P["FR"] - 1)
    line("Concentration factor vs NaCl saturation (317 g/L)", f(317 / cb, 1))
    frac = 0.050 / cb
    line("Allowed brine carryover for 50 mg/L distillate", f(frac * 100, 3), "% of distillate")
    line("Allowed brine carryover on the design day", f(frac * dd["yield"] * 1000, 1), "mL/day")
    line("Daily feed and brine on the design day", f"{P['FR'] * dd['yield']:.1f}, {(P['FR'] - 1) * dd['yield']:.1f}", "L/day")

    # 10. Mass
    print("\n10. Mass (dry panel, then wet)")
    ap = P["aperture"]
    frame_h = 0.0705                           # 5 mm ledge + 30.5 mm stack + 25 mm air + 6 mm glazing + 4 mm lip
    items = {
        "Plates, 5 x 0.5 mm aluminum (4 with 77 mm lips)": (1 + 4 * 1.077) * ap * P["plate_t"] * 2700,
        "Glazing, twin-wall PC 1.3 kg/m2": 1.3 * ap * ap,
        "Frame, 12 mm plywood (550 kg/m3)": 4 * (ap + 2 * P["wall"]) * frame_h * 0.012 * 550,
        "Liner, 25 mm stone wool board (140 kg/m3)": 4 * (ap + P["wall"]) * frame_h * 0.025 * 140,
        "Wicks, 4 x 1.25 m2 at 0.20 kg/m2 dry": 4 * 1.25 * ap * 0.20,
        "Side rails, 150 degC polymer and PC (8 x 12 x 7 mm)": 4 * 2 * P["rail_w"] * (P["gap"] + P["wick_t"]) * ap * 1200,
        "Intermediate ribs, 16 x 7 mm silicone cord": 4 * RIB["n_ribs"] * math.pi / 4 * 0.007 ** 2 * ap * 1150,
        "Fins, 10 folded strips 50 mm developed": P["fin_n"] * P["fin_len"] * 0.050 * P["plate_t"] * 2700,
        "Trough, manifold, gutter, fittings": 1.5,
        "Sealant, fasteners, tubing": 0.5,
    }
    for k, vv in items.items():
        line(k, f(vv, 2), "kg")
    dry_m = sum(items.values())
    wet_m = dry_m + 4 * 1.0 * ap * ap
    line("Panel mass, dry", f(dry_m, 1), "kg")
    line("Panel mass, wet wicks", f(wet_m, 1), "kg")
    stand_m = 6.0 * 0.045 * 0.045 * 500 + 1.0
    line("Adjustable stand (6 m of 45 x 45 mm timber, hardware)", f(stand_m, 1), "kg")

    # 11. Tilt and footprint
    print("\n11. Tilt range and footprint")
    L_slope = ap + 2 * P["wall"] + 0.075 + 0.135    # frame, trough outboard, manifold and brine gutter outboard
    for tdeg in (10, 20, 35):
        tb = math.radians(tdeg)
        plan = L_slope * math.cos(tb) + 0.10 * math.sin(tb)
        rise = L_slope * math.sin(tb)
        line(f"Plan depth and rise at {tdeg} deg", f"{plan:.2f}, {rise:.2f}", "m")
    line("Plan width (frame plus stand posts)", f(ap + 2 * P["wall"] + 2 * 0.045, 2), "m")
    front_h = 0.35
    for tdeg in (10, 20, 35):
        tb = math.radians(tdeg)
        line(f"Rear strut height at {tdeg} deg (front pivot 0.35 m)",
             f(front_h + (ap + 2 * P["wall"] - 0.045) * math.sin(tb), 2), "m")
    feed_h = front_h + (ap + 2 * P["wall"] + 0.08) * math.sin(math.radians(35)) + 0.06 * math.cos(math.radians(35))
    line("Highest feed trough at 35 deg", f(feed_h, 2), "m")

    # 12. Wind
    print("\n12. Wind overturning (safety)")
    Aw = (ap + 2 * P["wall"]) ** 2
    for vw in (10.0, 20.0):
        F = 0.5 * 1.2 * vw ** 2 * 1.2 * Aw
        line(f"Normal force at {vw:.0f} m/s, Cf 1.2", f(F, 0), "N")
    W = (wet_m + stand_m) * G_ACC
    line("Weight of wet panel and stand", f(W, 0), "N")
    v_lift = math.sqrt(W * math.cos(BETA) / (0.5 * 1.2 * 1.2 * Aw))
    line("Wind speed at which lift equals weight (approx.)", f(v_lift, 1), "m/s")

    # 13. Cost
    print("\n13. Cost from bom/bom.csv")
    rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
    total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
    line("BOM lines", str(len(rows)))
    line("Parts total", f(total, 2), "USD")
    line("Budget (project.yaml)", f(P["budget"], 2), "USD")
    line("Margin", f(P["budget"] - total, 2), "USD")


if __name__ == "__main__":
    main()
