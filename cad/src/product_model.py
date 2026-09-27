"""StillStack product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: painted plywood frame with eased edges, foil
liner, anodized glazing trim with stainless screws, twin-wall glazing with visible flutes,
a stepped corner cutaway that shows all four wick stages, split side rails and silicone ribs,
flanged fins, lidded distillate manifold with outlet tube, gutters with end caps and drip
valve, timber stand with hinges and tilt pins, and labels.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, rib_positions() and wick_strips() in
model.py, and the panel is placed exactly as model.build() places it. Axes as model.py:
world X points down the slope (low, collection edge at +X), Y across the panel, Z up, ground
at Z = 0. The panel parts are built in model.py's local frame and then tilted.

The corner cutaway is a render device, not a design change: the removed corner of each layer
is kept as a separate "cutaway fill" part in group "accessory", so the hero view (without
accessories) shows the cutaway and the exploded view (with accessories) shows whole layers.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build123d import (Align, Axis, Box, Compound, Cylinder, Plane, Pos, RectangleRounded, Rot,
                       Solid, Sphere, Text, Vector, extrude, fillet)
from model import PARAMS, build, rib_positions, wick_strips

FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

TITLE = "StillStack: four-stage solar wick still for drinking water"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); low collection edge "
             "with the distillate manifold and brine gutter at right, corner cutaway showing the four "
             "wick stages nearest the camera"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): glazing trim, "
             "twin-wall glazing, black absorber, then four stages of wick, spacer rails and ribs and "
             "condenser plate, fins, insulated frame, feed trough at left, distillate manifold and brine "
             "gutter at right, timber stand below"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 52, "az": -32,
     "note": "Detail view from the front right and high above (about 52 deg elevation): stepped corner "
             "cutaway through the glazing showing absorber, wicks, rails, ribs and condenser plates"},
]

# Colours (restrained product palette; accent from the kit)
C_ACCENT = "#0F766E"
C_FRAME = "#E4E2DC"      # exterior-painted plywood
C_LINER = "#C9CDD2"      # foil face of the stone wool liner
C_TRIM = "#3B424A"       # dark anodized glazing trim
C_STEEL = "#B4BAC1"      # stainless
C_GLAZ = "#DCEAF2"
C_ABS = "#1B1D20"        # matte black absorber paint
C_WICK = "#E8DFCC"
C_PLATE = "#C3C9D0"
C_RAIL_HT = "#C7AF7F"    # high-temperature polymer (PPS natural)
C_RAIL_PC = C_ACCENT     # printed polycarbonate
C_RIB = "#C65A3E"        # silicone cord
C_FIN = "#B8BEC6"
C_TROUGH = "#8F98A3"
C_CAP = "#5B6470"
C_MANI = "#F2F3F1"       # food-grade PP
C_BRINE = "#5B6470"
C_TIMBER = "#B8895A"
C_TUBE = "#E3DED3"
C_WHITE = "#F7F7F5"
C_GROUND = "#D6CFC0"
C_JAR = "#DDEBF2"
C_COVER = "#EEEEEA"

# Appearance-only detail sizes (mm)
CUT0 = 440.0             # absorber cutaway corner size; each lower layer steps in by CUT_STEP
CUT_STEP = 45.0
FLUTE_PITCH = 10.0       # twin-wall glazing web pitch (visual)
SKIN = 0.8               # twin-wall skin thickness
TRIM_OUT, TRIM_IN = 535.0, 490.0   # half sizes of the glazing trim ring
TRIM_T = 1.5


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, lx, ly, lz):
    return Pos(cx, cy, cz) * Box(lx, ly, lz)


def _zbox(z0, z1, lx, ly, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Box(lx, ly, z1 - z0)


def _rrect(lx, ly, r, z0, h, x=0.0, y=0.0):
    r = max(min(r, min(lx, ly) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(lx, ly, r), amount=h)


def _rod(p0, p1, r):
    """Cylinder of radius r from point p0 to point p1."""
    a, b = Vector(*p0), Vector(*p1)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    out = None
    for a, b in zip(points[:-1], points[1:]):
        seg = _rod(a, b, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out = out + Pos(*q) * Sphere(r)
    return out


def _compound(shapes):
    shapes = [s for s in shapes if s is not None]
    return shapes[0] if len(shapes) == 1 else Compound(children=shapes)


def _text(txt, size, plane, h=0.4):
    """Raised text on `plane` (x_dir reads left to right, z_dir out of the surface)."""
    try:
        t = extrude(plane * Text(txt, font_size=size, font_path=FONT, align=(Align.CENTER, Align.CENTER)),
                    amount=h)
        return t if t.is_valid else None
    except Exception:
        return None


def _corner(c, z0=-60.0, z1=90.0):
    """Cutaway region of size c at the local (+x, -y) corner of the panel (inside the frame only)."""
    x0, x1 = 500.0 - c, 500.5
    y0, y1 = -520.0, -500.0 + c
    return _box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, x1 - x0, y1 - y0, z1 - z0)


def _split(shape, c):
    """(kept part, cutaway fill) of a layer for a corner cut of size c."""
    if c <= 0:
        return shape, None
    reg = _corner(c)
    keep, fill = shape - reg, shape & reg
    if fill is None or fill.volume < 1e-3:
        fill = None
    return keep, fill


def product_parts(P=PARAMS):
    p = P
    tilt = p["tilt"]
    s, c = math.sin(math.radians(tilt)), math.cos(math.radians(tilt))
    AP = p["aperture"]
    PL = AP - 2 * p["plate_clear"]
    WALL = p["ply_t"] + p["foam_t"]
    outer = AP + 2 * WALL
    FZ0 = -5.0
    Hc = p["front_h"] + (outer / 2) * s - FZ0 * c          # as model.build()

    def place(sh):
        return Pos(0, 0, Hc) * Rot(0, tilt, 0) * sh

    def w(x, zl):                                          # local (x, z) to world (x, z), as model.build()
        return x * c + zl * s, -x * s + zl * c + Hc

    n = (s, 0.0, c)            # panel normal in world
    down = (c, 0.0, -s)        # down the slope in world

    def along(v, d):
        return tuple(d * a for a in v)

    def plus(a, b):
        return tuple(x + y for x, y in zip(a, b))

    local = build(p, local_only=True)
    world = build(p)
    out = []

    def add(name, shape, color, material, bom, group, explode, local_frame=True):
        if shape is None:
            return
        sh = place(shape) if local_frame else shape
        out.append({"name": name, "shape": sh, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ stack (model.py order, bottom up)
    lipped = PL + p["lip_out"] + WALL
    h_st = p["gap"] + p["wick_t"]
    z = 0.0
    plates_z = [z]
    z += p["plate_t"]
    gaps_z = []
    wicks_z = []
    for k in range(p["n_stages"]):
        gaps_z.append(z)
        z += p["gap"]
        wicks_z.append(z)
        z += p["wick_t"]
        if k < p["n_stages"] - 1:
            plates_z.append(z)
            z += p["plate_t"]
    abs_z = z
    stack_top = z + p["plate_t"]
    glaz_z = stack_top + p["air_gap"]
    top_z = glaz_z + p["glaz_t"] + p["lip"]

    # cut sizes and explode distances, top layer first; gap index k counts bottom up (stage 4 - k)
    G, B = 66.0, 170.0
    ns = p["n_stages"]

    def cut_wick(k):          # wick of gap k (stage ns - k)
        return CUT0 - CUT_STEP * (2 * (ns - 1 - k) + 1)

    def cut_plate(i):         # condenser plate i (0 = bottom plate, uncut)
        return 0.0 if i == 0 else CUT0 - CUT_STEP * 2 * (ns - i)

    def ex_gap(k):
        return B + G * (3 * k + 1)

    def ex_wick(k):
        return B + G * (3 * k + 2)

    def ex_plate(i):
        return B + G * 3 * i

    ex_abs = B + G * 3 * ns
    ex_glaz = ex_abs + 130
    ex_trim = ex_glaz + 110

    def layer(name, shape, cut, color, material, bom, group, ex):
        keep, fill = _split(shape, cut)
        add(name, keep, color, material, bom, group, ex)
        if fill is not None:
            add(f"{name} (cutaway fill)", fill, color, material, bom, "accessory", ex)

    # absorber (BOM 3)
    absorber = _zbox(abs_z, abs_z + p["plate_t"], PL, PL)
    layer("Absorber plate (matte black)", absorber, CUT0, C_ABS, "painted", 3, "internal", along(n, ex_abs))

    # condenser plates (BOM 5): bottom plate is condenser 4, top one is condenser 1
    for i, zp in enumerate(plates_z):
        pl = _zbox(zp, zp + p["plate_t"], lipped, PL, x=(lipped - PL) / 2)
        num = ns - i
        nm = "Bottom condenser plate 4" if i == 0 else f"Condenser plate {num}"
        layer(nm, pl, cut_plate(i), C_PLATE, "metal", 5, "internal", along(n, ex_plate(i)))

    # wicks (BOM 4), rails (BOM 6) and ribs (BOM 7) per stage
    strips = wick_strips(p)
    for k in range(ns):
        stage = ns - k
        zw = wicks_z[k]
        wk = _compound([_zbox(zw, zw + p["wick_t"], PL - 20, b - a, x=-10, y=(a + b) / 2) for a, b in strips])
        layer(f"Wick strips, stage {stage} (fabric)", wk, cut_wick(k), C_WICK, "fabric", 4, "internal",
              along(n, ex_wick(k)))
        zg = gaps_z[k]
        rails = _compound([_zbox(zg, zg + h_st, PL, p["rail_w"], y=sy * (PL / 2 - p["rail_w"] / 2))
                           for sy in (-1, 1)])
        rails = _compound([_fillet_try(r, r.edges().filter_by(Axis.X), [1.0, 0.5]) for r in rails.solids()])
        hot = stage <= 2
        layer(f"Side spacer rails, stage {stage}" + (" (150 C polymer)" if hot else " (printed PC)"),
              rails, cut_wick(k), C_RAIL_HT if hot else C_RAIL_PC, "plastic", 6, "internal",
              along(n, ex_gap(k)))
        ribs = _compound([Pos(0, ry, zg + h_st / 2) * Rot(0, 90, 0) * Cylinder(p["rib_d"] / 2, PL)
                          for ry in rib_positions(p)])
        layer(f"Silicone spacer ribs, stage {stage}", ribs, cut_wick(k), C_RIB, "rubber", 7, "internal",
              along(n, ex_gap(k)))

    # fins with flanges (BOM 11)
    pitch = PL / p["fin_n"]
    fins = []
    for i in range(p["fin_n"]):
        y = -PL / 2 + pitch * (i + 0.5)
        f = _zbox(-p["fin_depth"], 0.0, PL - 40, p["fin_t"], y=y)
        f = f + _zbox(-0.6, 0.0, PL - 40, 20.0, y=y + 10.0 - p["fin_t"] / 2)
        fins.append(f)
    add("Heat-rejection fins (folded aluminum)", _compound(fins), C_FIN, "metal", 11, "internal",
        along(n, B - 170))

    # ------------------------------------------------------------ twin-wall glazing (BOM 1)
    z0, z1 = glaz_z, glaz_z + p["glaz_t"]
    webs = [_zbox(z0 + SKIN, z1 - SKIN, AP, 0.4, y=-AP / 2 + FLUTE_PITCH * (j + 0.5))
            for j in range(int(AP // FLUTE_PITCH))]
    glaz = [_zbox(z0, z0 + SKIN, AP, AP), _zbox(z1 - SKIN, z1, AP, AP)] + webs
    # flutes run down the slope (along local x) so condensate drains; webs are across y
    glaz = Compound(children=glaz)
    layer("Twin-wall polycarbonate glazing", glaz, CUT0 + 45.0, C_GLAZ, "clear", 1, "shell",
          along(n, ex_glaz))

    # ------------------------------------------------------------ insulated frame (BOM 2)
    fh = top_z - FZ0
    ply_in = AP + 2 * p["foam_t"]
    shell = _zbox(FZ0, top_z, outer, outer)
    shell = _fillet_try(shell, shell.edges().filter_by(Axis.Z), [8.0, 5.0, 3.0])
    shell = _fillet_try(shell, shell.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 2.0, 1.0])
    shell = _fillet_try(shell, shell.faces().sort_by(Axis.Z)[0].edges(), [2.0, 1.0])
    ply = shell - _zbox(FZ0 - 1, top_z + 1, ply_in, ply_in)
    liner = _zbox(FZ0, top_z, ply_in, ply_in) - _zbox(FZ0 - 1, top_z + 1, AP, AP)
    liner = liner + _compound([_zbox(FZ0, FZ0 + 5.0, AP, 15.0, y=sy * (AP / 2 - 7.5)) for sy in (-1, 1)])
    for zp in plates_z:
        slot = Pos(AP / 2 + WALL / 2, 0, zp + p["plate_t"] / 2) * Box(WALL + 2, PL, 2.0)
        ply = ply - slot
        liner = liner - slot
    # shallow reveal grooves at the corner joints of the painted plywood (visual)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ply = ply - _box(sx * (outer / 2 - 12.0), sy * (outer / 2), FZ0 + fh / 2, 1.0, 1.2, fh + 2)
    add("Insulated frame, painted plywood", ply, C_FRAME, "painted", 2, "shell", (0, 0, 0))
    add("Stone wool liner, foil face", liner, C_LINER, "metal", 2, "shell", (0, 0, 0))

    # glazing trim ring with a downturned lip onto the glazing, and stainless screws (BOM 13)
    ring = _zbox(top_z, top_z + TRIM_T, 2 * TRIM_OUT, 2 * TRIM_OUT) - \
        _zbox(top_z - 1, top_z + TRIM_T + 1, 2 * TRIM_IN, 2 * TRIM_IN)
    ring = _fillet_try(ring, ring.faces().sort_by(Axis.Z)[-1].edges(), [0.8, 0.5])
    lip = _zbox(z1, top_z + 0.01, 2 * TRIM_IN + 6, 2 * TRIM_IN + 6) - \
        _zbox(z1 - 1, top_z + 1, 2 * TRIM_IN, 2 * TRIM_IN)
    add("Glazing trim, anodized aluminum", ring + lip, C_TRIM, "metal", 13, "shell", along(n, ex_trim))
    heads = []
    sp = (TRIM_OUT + 500.0) / 2 + 3.0
    pts = [(sx * sp, t) for sx in (-1, 1) for t in (-400, -200, 0, 200, 400)] + \
          [(t, sy * sp) for sy in (-1, 1) for t in (-400, -200, 0, 200, 400)] + \
          [(sx * sp, sy * sp) for sx in (-1, 1) for sy in (-1, 1)]
    for (x, y) in pts:
        hd = Pos(x, y, top_z + TRIM_T + 0.9) * Cylinder(3.5, 1.8)
        hd = _fillet_try(hd, hd.faces().sort_by(Axis.Z)[-1].edges(), [0.8, 0.5])
        hd = hd - Pos(x, y, top_z + TRIM_T + 1.8) * Box(3.6, 0.7, 1.4) - Pos(x, y, top_z + TRIM_T + 1.8) * Box(0.7, 3.6, 1.4)
        heads.append(hd)
    add("Stainless trim screws", _compound(heads), C_STEEL, "metal", 13, "shell", along(n, ex_trim + 60))

    # nameplate on the front (-Y) face of the frame, near the low end
    npx, npz = 250.0, FZ0 + fh / 2
    plate = Pos(npx, -outer / 2 - 0.4, npz) * Box(190.0, 0.8, 34.0)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Y), [3.0, 2.0])
    add("Nameplate", plate, C_ACCENT, "plastic", None, "shell", (0, 0, 0))
    txt = _text("STILLSTACK", 17.0, Plane(origin=(npx, -outer / 2 - 0.8, npz), x_dir=(1, 0, 0), z_dir=(0, -1, 0)))
    add("Nameplate lettering", txt, C_WHITE, "plastic", None, "shell", (0, 0, 0))

    # ------------------------------------------------------------ feed trough (BOM 8) with end caps and drip valve
    tx, tz = -outer / 2 - 40, 20.0
    body = _box(tx, 0, tz, 70, AP - 12, 70)
    body = _fillet_try(body, body.faces().sort_by(Axis.Z)[0].edges().filter_by(Axis.Y), [8.0, 5.0])
    body = body - _box(tx, 0, tz + 6, 60, AP + 10, 70)
    # rolled bead along both top edges
    for sx in (-1, 1):
        body = body + Pos(tx + sx * 32.5, 0, tz + 35) * Rot(90, 0, 0) * Cylinder(3.0, AP - 12)
    caps = []
    for sy in (-1, 1):
        cp = _box(tx, sy * (AP / 2 - 3), tz - 1, 76, 8, 72)
        cp = _fillet_try(cp, cp.faces().sort_by(Axis.Z)[0].edges().filter_by(Axis.Y), [9.0, 6.0])
        cp = cp - _box(tx, sy * (AP / 2 - 3) - sy * 2, tz + 6, 60, 8, 70)
        caps.append(cp)
    ex_tr = plus(along(down, -300), along(n, 120))
    add("Feed trough (PVC gutter)", body, C_TROUGH, "plastic", 8, "shell", ex_tr)
    add("Feed trough end caps", _compound(caps), C_CAP, "plastic", 8, "shell", ex_tr)
    vy = -AP / 2 - 7
    valve = Pos(tx, vy - 9, tz - 12) * Rot(90, 0, 0) * Cylinder(6.0, 18.0)
    valve = valve + Pos(tx, vy - 20, tz - 12) * Rot(90, 0, 0) * Cylinder(3.5, 8.0)
    add("Drip valve body", valve, C_STEEL, "metal", 8, "shell", ex_tr)
    lever = _box(tx, vy - 12, tz - 12 + 14, 6.0, 4.0, 22.0)
    lever = _fillet_try(lever, lever.edges().filter_by(Axis.Y), [1.5, 1.0])
    add("Drip valve lever", lever, C_ACCENT, "plastic", 8, "shell", ex_tr)

    # ------------------------------------------------------------ distillate manifold (BOM 9), lidded
    mx, mz = outer / 2 + 28, -12.0
    lid_z = mz + 45.0                                    # cavity top (as model.py) is the lid parting line
    m_out = _box(mx, 0, mz + 25, 56, AP, 50)
    m_out = _fillet_try(m_out, m_out.edges().filter_by(Axis.Y), [4.0, 2.5, 1.5])
    m_out = m_out - _box(mx, 0, mz + 25, 46, AP - 10, 40)
    m_out = m_out - Pos(outer / 2 + 1, 0, stack_top / 2 - 3) * Box(4, PL, stack_top + 4)
    m_out = m_out + Pos(mx, AP / 2 - 30, mz - 30) * Cylinder(8, 60)
    m_out = m_out - Pos(mx, AP / 2 - 30, mz - 25) * Cylinder(5, 80)
    lid_reg = _box(mx, 0, lid_z + 50, 200, AP + 20, 100)
    lid = m_out & lid_reg
    tub = m_out - lid_reg
    # parting-line groove just below the lid
    tub = tub - (_box(mx, 0, lid_z - 0.5, 60, AP + 4, 1.0) - _box(mx, 0, lid_z - 0.5, 55.0, AP - 1.0, 2.0))
    ex_m = plus(along(down, 260), along(n, 140))
    add("Distillate manifold channel (food-grade PP)", tub, C_MANI, "plastic", 9, "shell", ex_m)
    # lid clips
    clips = [_box(mx + 28.4, y, lid_z - 4, 1.2, 24, 10) for y in (-380, -130, 130, 380)]
    lid = lid + _compound(clips)
    add("Distillate manifold lid", lid, C_MANI, "plastic", 9, "shell", plus(ex_m, along(n, 70)))
    # label on the +X face
    lbl_plane = Plane(origin=(mx + 28.0, -AP / 2 + 170, mz + 20), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    band = Pos(mx + 28.3, -AP / 2 + 170, mz + 20) * Box(0.6, 150, 20)
    add("Distillate label band", band, C_ACCENT, "plastic", 9, "shell", ex_m)
    add("Distillate label lettering",
        _text("DISTILLATE", 11.0, Plane(origin=(mx + 28.6, -AP / 2 + 170, mz + 20), x_dir=(0, 1, 0),
                                        z_dir=(1, 0, 0)), h=0.3),
        C_WHITE, "plastic", 9, "shell", ex_m)
    del lbl_plane
    # outlet barb
    barb = Pos(mx, AP / 2 - 30, mz - 66) * (Cylinder(4.5, 12) - Cylinder(3.0, 14))
    add("Distillate outlet barb", barb, C_ACCENT, "plastic", 9, "shell", ex_m)

    # ------------------------------------------------------------ brine gutter (BOM 10)
    bx, bz = outer / 2 + 100, mz - 30
    br = _box(bx, 0, bz, 70, AP, 40)
    br = _fillet_try(br, br.faces().sort_by(Axis.Z)[0].edges().filter_by(Axis.Y), [6.0, 4.0])
    br = br - _box(bx, 0, bz + 5, 60, AP - 10, 40)
    for sx in (-1, 1):
        br = br + Pos(bx + sx * 32.5, 0, bz + 20) * Rot(90, 0, 0) * Cylinder(2.5, AP)
    br = br + Pos(bx, -AP / 2 + 30, mz - 80) * Cylinder(8, 60)
    br = br - Pos(bx, -AP / 2 + 30, mz - 75) * Cylinder(5, 80)
    ex_b = plus(along(down, 420), along(n, -60))
    add("Brine gutter (PVC)", br, C_BRINE, "plastic", 10, "shell", ex_b)
    add("Brine label lettering",
        _text("BRINE", 11.0, Plane(origin=(bx + 35.0, -AP / 2 + 170, bz), x_dir=(0, 1, 0), z_dir=(1, 0, 0)), h=0.3),
        C_WHITE, "plastic", 10, "shell", ex_b)

    # ------------------------------------------------------------ stand (BOM 12), as model.py, timber members
    P_ = p["post"]
    fx, fz = w(outer / 2 - P_ / 2, FZ0)
    rx, rz = w(-outer / 2 + P_ / 2, FZ0)
    ys = (-(outer / 2 + P_ / 2), outer / 2 + P_ / 2)

    def timber(sh):
        return _fillet_try(sh, sh.edges(), [3.0, 2.0, 1.0])

    members = []
    for yy in ys:
        members.append(timber(Pos(fx, yy, fz / 2) * Box(P_, P_, fz)))
        rs = timber(Pos(rx, yy, rz / 2) * Box(P_, P_, rz))
        for i in range(4):                               # tilt pin holes (10 to 35 deg settings)
            rs = rs - Pos(rx, yy, rz - 90 - 55 * i) * Rot(90, 0, 0) * Cylinder(5.0, P_ + 2)
        members.append(rs)
        members.append(timber(Pos((fx + rx) / 2, yy, P_ / 2) * Box(abs(fx - rx) + P_, P_, P_)))
    members.append(timber(Pos(rx, 0, 200) * Box(P_, outer + 2 * P_, P_)))
    ex_s = (0, 0, -520)
    add("Adjustable tilt stand (timber)", _compound(members), C_TIMBER, "wood", 12, "shell", ex_s, local_frame=False)

    hw = []
    for yy in ys:
        # front pivot hinge on the +X face of each front post
        leaf = _box(fx + P_ / 2 + 1.25, yy, fz - 42, 2.5, 38, 70)
        leaf = _fillet_try(leaf, leaf.edges().filter_by(Axis.X), [3.0, 1.5])
        knuckle = Pos(fx + P_ / 2 + 5.0, yy, fz - 4) * Rot(90, 0, 0) * Cylinder(5.0, 40)
        hw.append(leaf + knuckle)
        for zz in (fz - 62, fz - 28):
            hw.append(Pos(fx + P_ / 2 + 3.0, yy, zz) * Rot(0, 90, 0) * Cylinder(3.2, 1.5))
        # tilt pin through the second hole of each rear strut, head on the outer side
        side = -1 if yy < 0 else 1
        zp = rz - 90 - 55
        hw.append(_rod((rx, yy + side * (P_ / 2 + 3), zp), (rx, yy - side * (P_ / 2 + 8), zp), 4.5))
        hw.append(_rod((rx, yy + side * (P_ / 2), zp), (rx, yy + side * (P_ / 2 + 3), zp), 8.0))
        # ground anchor brackets at both ends of each ground rail
        for xx in (fx, rx):
            br_ = _box(xx, yy + side * (P_ / 2 + 1.5), 22, 40, 3, 40)
            hw.append(_fillet_try(br_, br_.edges().filter_by(Axis.Y), [3.0, 1.5]))
            hw.append(_box(xx, yy + side * (P_ / 2 + 12), 1.5, 40, 22, 3))
    add("Stand hardware (hinges, tilt pins, anchors)", _compound(hw), C_STEEL, "metal", 12, "shell", ex_s,
        local_frame=False)

    # ------------------------------------------------------------ context: ground patch, outlet tube, brine hose, jar
    bb = Compound(children=list(world.values())).bounding_box()
    gx0, gx1 = bb.min.X - 90, bb.max.X + 200
    gy0, gy1 = bb.min.Y - 90, bb.max.Y + 90
    ground = _rrect(gx1 - gx0, gy1 - gy0, 60, -20.0, 20.0, x=(gx0 + gx1) / 2, y=(gy0 + gy1) / 2)
    ground = _fillet_try(ground, ground.faces().sort_by(Axis.Z)[-1].edges(), [8.0, 4.0])
    add("Ground patch (packed gravel)", ground, C_GROUND, "paper", None, "context", (0, 0, 0), local_frame=False)

    def wp(xl, yl, zl):
        xw, zw = w(xl, zl)
        return (xw, yl, zw)

    # distillate outlet tube (BOM 13) to a covered container on the ground
    t0 = wp(mx, AP / 2 - 30, mz - 71)
    jar_x, jar_y = t0[0] + 170, t0[1] - 40
    tube = _pipe([t0, (t0[0], t0[1], 330.0), (jar_x, jar_y, 300.0), (jar_x, jar_y, 262.0)], 5.0)
    add("Silicone outlet tube", tube, C_TUBE, "rubber", 13, "context", (0, 0, 0), local_frame=False)
    jar = _rrect(150, 150, 30, 0.0, 240.0, x=jar_x, y=jar_y)
    jar = _fillet_try(jar, jar.faces().sort_by(Axis.Z)[-1].edges(), [20.0, 12.0, 6.0])
    jar = jar - _rrect(144, 144, 27, 3.0, 245.0, x=jar_x, y=jar_y)
    add("Distillate container, clear (user supplied)", jar, C_JAR, "clear", None, "context", (0, 0, 0),
        local_frame=False)
    water = _rrect(142, 142, 26, 3.0, 120.0, x=jar_x, y=jar_y)
    add("Distillate in container", water, "#CFE3EE", "clear", None, "context", (0, 0, 0), local_frame=False)
    jcap = Pos(jar_x, jar_y, 254.0) * Cylinder(34.0, 14.0)
    jcap = _fillet_try(jcap, jcap.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 1.5])
    jcap = jcap - Pos(jar_x, jar_y, 262.0) * Cylinder(6.0, 10.0)
    neck = Pos(jar_x, jar_y, 244.0) * Cylinder(30.0, 8.0)
    add("Container cap", jcap + neck, C_ACCENT, "plastic", None, "context", (0, 0, 0), local_frame=False)

    # brine drain hose (BOM 10) running out to a soak-away
    b0 = wp(bx, -AP / 2 + 30, mz - 111)
    hose = _pipe([b0, (b0[0], b0[1], 12.0), (b0[0] + 60, b0[1], 8.0), (gx1 - 40, b0[1] - 60, 8.0)], 7.0)
    add("Brine drain hose", hose, "#4B5563", "rubber", 10, "context", (0, 0, 0), local_frame=False)

    # ------------------------------------------------------------ accessory: stagnation cover (BOM 14), folded
    cvx, cvy = gx0 + 260, gy0 - 260
    cover = _rrect(360, 260, 30, 0.0, 44.0, x=cvx, y=cvy)
    cover = _fillet_try(cover, cover.faces().sort_by(Axis.Z)[-1].edges(), [12.0, 8.0, 4.0])
    add("Stagnation cover (folded tarpaulin)", cover, C_COVER, "fabric", 14, "accessory", (0, 0, -520),
        local_frame=False)
    cord = _compound([Pos(cvx, cvy + dy, 22.0) * Rot(0, 90, 0) * Cylinder(3.0, 366.0) for dy in (-70, 70)])
    add("Stagnation cover edge cord", cord, "#374151", "rubber", 14, "accessory", (0, 0, -520),
        local_frame=False)
    return out


if __name__ == "__main__":
    for q in product_parts():
        sh = q["shape"]
        print(f"{q['name']:52s} {q['group']:9s} {q['material']:8s} valid={sh.is_valid} vol={sh.volume / 1000:9.1f} cm3")
