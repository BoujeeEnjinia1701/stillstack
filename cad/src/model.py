"""StillStack parametric model (build123d), TRL 3 massing-plus level.

Run from the repo root:  python cad/src/model.py
Exports cad/step/stillstack-assembly.step, cad/stl/stillstack-assembly.stl and
cad/stl/side-rail.stl, prints part masses and checks the tilt range (R11).

Correct interfaces and main dimensions only; not fabrication detail.

The panel is modeled flat in a local frame and then tilted about the front pivot:
  local x runs down the slope (x < 0 is the high, feed edge; x > 0 the low, collection edge),
  local y runs across the panel, local z is the panel normal (toward the sun).
Stack, bottom up: bottom plate (last condenser, fins underneath), then for each stage
a vapor gap and a wick bonded under the plate above; the top plate is the absorber.
Spacers: printed PC side rails plus intermediate silicone-cord ribs (pitch from SSK-CAL-001).
"""
from __future__ import annotations
import math
from pathlib import Path

from build123d import Box, Compound, Cylinder, Pos, Rot, export_step, export_stl

# Top-level parameters (mm, deg). Edit these, not the geometry below.
PARAMS = {
    "tilt": 20.0,          # deg from horizontal; the stand allows 10 to 35 (R11)
    "aperture": 1000.0,    # square aperture side
    "n_stages": 4,
    "plate_t": 0.5,        # aluminum absorber and condenser plates
    "plate_clear": 2.0,    # clearance each side for thermal growth (about 1.4 mm at 60 K)
    "wick_t": 1.0,
    "gap": 6.0,            # vapor gap, wick face to condensing face
    "rail_w": 12.0,        # printed PC side rail width
    "rib_d": 7.0,          # silicone cord rib diameter (gap plus wick)
    "n_ribs": 4,           # intermediate ribs per gap (CAL-001 section 3)
    "wick_break": 10.0,    # dry break each side of a rib or rail (R4)
    "air_gap": 25.0,       # absorber to glazing
    "glaz_t": 6.0,         # twin-wall polycarbonate
    "ply_t": 12.0,         # plywood wall
    "foam_t": 25.0,        # PIR liner
    "lip": 4.0,            # frame lip above the glazing
    "fin_n": 10, "fin_depth": 30.0, "fin_t": 0.5,
    "lip_out": 40.0,       # condenser plate lip past the low wall into the distillate manifold
    "front_h": 350.0,      # height of the front pivot (low edge underside) above ground
    "post": 45.0,          # timber section
}

DENSITY = {  # kg/m3, for the mass cross-check against CAL-001
    "Absorber plate": 2700, "Condenser plates": 2700, "Heat-rejection fins": 2700,
    "Glazing": 217,  # twin-wall sheet: 1.3 kg/m2 over 6 mm
    "Wicks": 200, "Side spacer rails": 1200, "Spacer ribs": 1150,
    "Insulated frame": 200,  # plywood (12 mm, 550) and PIR (25 mm, 32) wall average
}


def _slab(z0, t, lx, ly, x=0.0, y=0.0):
    return Pos(x, y, z0 + t / 2) * Box(lx, ly, t)


def _union(shapes):
    out = shapes[0]
    for sh in shapes[1:]:
        out = out + sh
    return out


def rib_positions(p=PARAMS):
    span = p["aperture"] - 2 * p["plate_clear"] - 2 * p["rail_w"]    # clear span between side rails
    n = p["n_ribs"] + 1
    y0 = -span / 2
    return [y0 + span * i / n for i in range(1, n)]


def wick_strips(p=PARAMS):
    """(y_min, y_max) of each wick strip between rails and ribs, with dry breaks (R4)."""
    inner = p["aperture"] / 2 - p["plate_clear"] - p["rail_w"]
    edges = [-inner] + [y for r in rib_positions(p) for y in (r - p["rib_d"] / 2, r + p["rib_d"] / 2)] + [inner]
    strips = []
    for a, b in zip(edges[0::2], edges[1::2]):
        strips.append((a + p["wick_break"], b - p["wick_break"]))
    return strips


def build(p=PARAMS, tilt=None, local_only=False):
    """Return {part name: shape in world coordinates} for the assembly.
    With local_only, return the panel parts untilted in the local frame (no stand)."""
    tilt = p["tilt"] if tilt is None else tilt
    s, c = math.sin(math.radians(tilt)), math.cos(math.radians(tilt))
    AP = p["aperture"]
    PL = AP - 2 * p["plate_clear"]
    WALL = p["ply_t"] + p["foam_t"]
    outer = AP + 2 * WALL
    FZ0 = -5.0

    # ---- stack, bottom up
    z = 0.0
    condensers, wicks, rails, ribs = [], [], [], []
    lipped = PL + p["lip_out"] + WALL            # condenser plates run through the low wall
    condensers.append(_slab(z, p["plate_t"], lipped, PL, x=(lipped - PL) / 2)); z += p["plate_t"]
    for k in range(p["n_stages"]):
        h = p["gap"] + p["wick_t"]
        for sy in (-1, 1):
            rails.append(_slab(z, h, PL, p["rail_w"], y=sy * (PL / 2 - p["rail_w"] / 2)))
        for ry in rib_positions(p):
            ribs.append(Pos(0, ry, z + h / 2) * Rot(0, 90, 0) * Cylinder(p["rib_d"] / 2, PL))
        z += p["gap"]
        for a, b in wick_strips(p):
            wicks.append(_slab(z, p["wick_t"], PL - 20, b - a, x=-10, y=(a + b) / 2))
        z += p["wick_t"]
        if k < p["n_stages"] - 1:
            condensers.append(_slab(z, p["plate_t"], lipped, PL, x=(lipped - PL) / 2)); z += p["plate_t"]
    absorber = _slab(z, p["plate_t"], PL, PL); z += p["plate_t"]
    stack_top = z
    glaz_z = z + p["air_gap"]
    glazing = _slab(glaz_z, p["glaz_t"], AP, AP)
    top_z = glaz_z + p["glaz_t"] + p["lip"]

    # ---- insulated frame with slots for the condenser lips in the low wall
    fh = top_z - FZ0
    frame = (Pos(0, 0, FZ0 + fh / 2) * Box(outer, outer, fh)) - (Pos(0, 0, FZ0 + fh / 2) * Box(AP, AP, fh + 2))
    ledge = _union([_slab(FZ0, 5.0, AP, 15.0, y=sy * (AP / 2 - 7.5)) for sy in (-1, 1)])
    frame = frame + ledge
    for cp in condensers:
        bb = cp.bounding_box()
        frame = frame - Pos(AP / 2 + WALL / 2, 0, (bb.min.Z + bb.max.Z) / 2) * Box(WALL + 2, PL, 2.0)

    # ---- fins under the bottom plate, running down the slope
    pitch = PL / p["fin_n"]
    fins = _union([_slab(-p["fin_depth"], p["fin_depth"], PL - 40, p["fin_t"], y=-PL / 2 + pitch * (i + 0.5))
                   for i in range(p["fin_n"])])

    # ---- feed trough (high edge), distillate manifold with lid, brine gutter outboard (low edge)
    trough = Pos(-outer / 2 - 40, 0, 20) * (Box(70, AP, 70) - Pos(0, 0, 6) * Box(60, AP - 10, 70))
    mz = -12.0
    dist = Pos(outer / 2 + 28, 0, mz + 25) * (Box(56, AP, 50) - Pos(0, 0, 0) * Box(46, AP - 10, 40))
    dist = dist - Pos(outer / 2 + 1, 0, stack_top / 2 - 3) * Box(4, PL, stack_top + 4)  # entry slot for plate lips
    dist = dist + Pos(outer / 2 + 28, AP / 2 - 30, mz - 30) * Cylinder(8, 60)
    brine = Pos(outer / 2 + 100, 0, mz - 30) * (Box(70, AP, 40) - Pos(0, 0, 5) * Box(60, AP - 10, 40))
    brine = brine + Pos(outer / 2 + 100, -AP / 2 + 30, mz - 80) * Cylinder(8, 60)

    local = {
        "Glazing": glazing, "Insulated frame": frame, "Absorber plate": absorber,
        "Wicks": _union(wicks), "Condenser plates": _union(condensers),
        "Side spacer rails": _union(rails), "Spacer ribs": _union(ribs),
        "Feed trough": trough, "Distillate manifold": dist, "Brine gutter": brine,
        "Heat-rejection fins": fins,
    }

    if local_only:
        return local

    # ---- place: low-edge underside of the frame sits on the front pivot at front_h
    Hc = p["front_h"] + (outer / 2) * s - FZ0 * c
    place = lambda sh: Pos(0, 0, Hc) * Rot(0, tilt, 0) * sh
    world = {k: place(v) for k, v in local.items()}

    # ---- adjustable stand: front posts with pivot, rear struts set by tilt, ground rails, brace
    P_ = p["post"]
    def w(x, zl):
        return x * c + zl * s, -x * s + zl * c + Hc
    fx, fz = w(outer / 2 - P_ / 2, FZ0)
    rx, rz = w(-outer / 2 + P_ / 2, FZ0)
    ys = (-(outer / 2 + P_ / 2), outer / 2 + P_ / 2)
    st = []
    for yy in ys:
        st.append(Pos(fx, yy, fz / 2) * Box(P_, P_, fz))
        st.append(Pos(rx, yy, rz / 2) * Box(P_, P_, rz))
        st.append(Pos((fx + rx) / 2, yy, P_ / 2) * Box(abs(fx - rx) + P_, P_, P_))
    st.append(Pos(rx, 0, 200) * Box(P_, outer + 2 * P_, P_))
    world["Adjustable tilt stand"] = _union(st)
    return world


STACK = ["Absorber plate", "Wicks", "Condenser plates", "Side spacer rails", "Spacer ribs", "Heat-rejection fins"]


def stack_detail(p=PARAMS, x=(-10.0, 10.0), y=(72.0, 122.0), z=(-32.0, 36.0), keep=None):
    """Slice of the untilted panel (local frame) for drawing detail views."""
    cut = Pos(sum(x) / 2, sum(y) / 2, sum(z) / 2) * Box(x[1] - x[0], y[1] - y[0], z[1] - z[0])
    keep = STACK if keep is None else keep
    local = build(p, local_only=True)
    out = []
    for k in keep:
        sh = local[k] & cut
        if sh.volume > 1e-6:
            out.append(sh)
    return Compound(children=out)


def assembly(parts):
    kids = []
    for name, sh in parts.items():
        sh.label = name
        kids.append(sh)
    return Compound(children=kids, label="StillStack assembly")


def masses(parts):
    out = {}
    for name, rho in DENSITY.items():
        out[name] = parts[name].volume * 1e-9 * rho
    return out


def check_tilt_range(p=PARAMS):
    """R11: build at the ends of the tilt range and report clearances and heights."""
    rows = []
    for t in (10.0, 20.0, 35.0):
        parts = build(p, tilt=t)
        zmin = min(sh.bounding_box().min.Z for k, sh in parts.items() if k != "Adjustable tilt stand")
        bb = Compound(children=list(parts.values())).bounding_box()
        trough_top = parts["Feed trough"].bounding_box().max.Z
        rows.append((t, zmin, bb.size.X, bb.size.Y, trough_top))
    return rows


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parts = build()
    asm = assembly(parts)
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    export_step(asm, str(root / "step" / "stillstack-assembly.step"))
    export_stl(asm, str(root / "stl" / "stillstack-assembly.stl"))
    rail = Box(PARAMS["aperture"] - 2 * PARAMS["plate_clear"], PARAMS["rail_w"], PARAMS["gap"] + PARAMS["wick_t"])
    export_stl(rail, str(root / "stl" / "side-rail.stl"))
    bb = asm.bounding_box()
    print(f"Assembly envelope at {PARAMS['tilt']:.0f} deg: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print("Rib centers (mm):", ", ".join(f"{y:.0f}" for y in rib_positions()))
    print("Wick strip widths (mm):", ", ".join(f"{b - a:.0f}" for a, b in wick_strips()))
    ws = sum(b - a for a, b in wick_strips())
    print(f"Wet wick fraction of aperture width: {ws / PARAMS['aperture']:.3f}")
    m = masses(parts)
    for k, v in m.items():
        print(f"  {k:<22s} {v:6.2f} kg")
    print(f"Modeled panel mass (excl. trough, manifold, gutter, fasteners): {sum(m.values()):.1f} kg")
    print("Tilt check (tilt deg, lowest panel part above ground mm, plan X, plan Y, feed trough top mm):")
    for t, zmin, sx, sy, tt in check_tilt_range():
        print(f"  {t:4.0f}  {zmin:6.0f}  {sx:6.0f}  {sy:6.0f}  {tt:6.0f}")
    print("Exported cad/step/stillstack-assembly.step, cad/stl/stillstack-assembly.stl, cad/stl/side-rail.stl")
