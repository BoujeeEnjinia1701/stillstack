"""StillStack product appearance model (build123d), TRL 3, constructable design.

Finished-product look for photoreal renders. The geometry is the constructable model of
model.py (build_components, plate lips, wick clips, comb low wall, base ring, trough, lidded
manifold, stand), given colours and a few appearance-only details: twin-wall glazing with
flutes running down the slope, trim screws, a nameplate, a drip valve at the front end of the
feed trough, DISTILLATE and BRINE labels, PPS rails in their own colour (stages 1 and 2) beside
the teal printed rails (stages 3 and 4), a stepped corner cutaway that shows all four stages,
and context parts (gravel, outlet tube, jar, brine hose).
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension comes from PARAMS and build_components() in model.py, and the panel is
placed exactly as model.build() places it (model.place). Axes as model.py: world X points down
the slope (low, collection edge at +X), Y across the panel, Z up, ground at Z = 0. The
appearance-only details are listed in docs/REVIEW.md (2026-10-02).

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
from model import PARAMS, build_components, derived, place as m_place, to_world

FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

TITLE = "StillStack: four-stage solar wick still"

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
C_RAIL_HT = "#C7AF7F"    # PPS, natural (tan): stages 1 and 2 rails and the stop blocks
C_RAIL_PC = C_ACCENT     # printed polycarbonate (teal): stages 3 and 4 rails
C_RIB = "#C65A3E"        # silicone cord
C_DAM = "#D98BA3"        # silicone chevron dams
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
C_TAPE = "#1F2937"
C_FOAM = "#E8E1D0"

# Appearance-only detail sizes (mm)
CUT0 = 440.0             # absorber cutaway corner size; each lower layer steps in by CUT_STEP
CUT_STEP = 45.0
FLUTE_PITCH = 10.0       # twin-wall glazing web pitch (visual)
SKIN = 0.8               # twin-wall skin thickness
CUT_X1 = 760.0           # cutaway region reaches past the tongues so none is left floating


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


def _union(shapes):
    shapes = [s for s in shapes if s is not None]
    out = shapes[0]
    for sh in shapes[1:]:
        out = out + sh
    return out


def _text(txt, size, plane, h=0.4):
    """Raised text on `plane` (x_dir reads left to right, z_dir out of the surface)."""
    try:
        t = extrude(plane * Text(txt, font_size=size, font_path=FONT, align=(Align.CENTER, Align.CENTER)),
                    amount=h)
        return t if t.is_valid else None
    except Exception:
        return None


def _corner(c, z0=-60.0, z1=90.0):
    """Cutaway region of size c at the local (+x, -y) corner of the panel, tongues included."""
    x0, x1 = 500.0 - c, CUT_X1
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
    D = derived(p)
    AP = p["aperture"]
    OH = D["OH"]
    ns = p["n_stages"]
    n = (s, 0.0, c)            # panel normal in world
    down = (c, 0.0, -s)        # down the slope in world

    def along(v, d):
        return tuple(d * a for a in v)

    def plus(a, b):
        return tuple(x + y for x, y in zip(a, b))

    def place(sh):
        return m_place(sh, p, tilt)

    def wp(xl, yl, zl):
        xw, zw = to_world(xl, zl, p, tilt)
        return (xw, yl, zw)

    C = build_components(p, local_only=True)          # panel parts in the local frame
    W = build_components(p)                           # panel parts tilted, and the stand
    out = []

    def add(name, shape, color, material, bom, group, explode, local_frame=True):
        if shape is None:
            return
        sh = place(shape) if local_frame else shape
        out.append({"name": name, "shape": sh, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # cut sizes and explode distances; level 0 is the bottom plate, level ns the absorber
    G, B = 66.0, 170.0

    def cut_wick(k):          # wick of gap k counted bottom up (stage ns - k)
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

    # ------------------------------------------------------------ the stack, bottom up
    layer("Absorber plate (matte black)", C["absorber"], CUT0, C_ABS, "painted", 3, "internal", along(n, ex_abs))
    plate_of = {0: C["plate_bottom"]}
    for lvl in range(1, ns):
        plate_of[lvl] = C[f"plate_{ns - lvl}"]
    for i in range(ns):
        nm = "Bottom condenser plate 4" if i == 0 else f"Condenser plate {ns - i}"
        sh = plate_of[i]
        if i > 0:
            sh = sh + C[f"dams_{ns - i}"]
        layer(nm + (" with chevron dams" if i > 0 else ""), sh, cut_plate(i), C_PLATE, "metal", 5, "internal",
              along(n, ex_plate(i)))
    for k in range(ns):
        stage = ns - k
        layer(f"Wick strips, stage {stage} (fabric)", C[f"wick_{stage}"], cut_wick(k), C_WICK, "fabric", 4, "internal",
              along(n, ex_wick(k)))
        layer(f"Wick clips, stage {stage} (stainless)", C[f"clips_hi_{stage}"] + C[f"clips_lo_{stage}"], cut_wick(k),
              C_STEEL, "metal", 18, "internal", along(n, ex_wick(k)))
        hot = stage <= 2
        layer(f"Side spacer rails, stage {stage}" + (" (PPS)" if hot else " (printed PC)"), C[f"rails_{stage}"],
              cut_wick(k), C_RAIL_HT if hot else C_RAIL_PC, "plastic", 6, "internal", along(n, ex_gap(k)))
        layer(f"Silicone spacer ribs, stage {stage}", C[f"ribs_{stage}"], cut_wick(k), C_RIB, "rubber", 7, "internal",
              along(n, ex_gap(k)))
    add("Stop blocks (PPS)", C["stops"], C_RAIL_HT, "plastic", 6, "internal", along(down, 60))
    add("Heat-rejection fins (folded aluminum)", C["fins"], C_FIN, "metal", 11, "internal", along(n, B - 170))

    # ------------------------------------------------------------ twin-wall glazing (BOM 1), flutes down the slope
    gs = p["glaz_size"] / 2
    z0, z1 = D["glaz_z"], D["glaz_z"] + p["glaz_t"]
    nweb = int(2 * gs // FLUTE_PITCH)
    webs = [_zbox(z0 + SKIN, z1 - SKIN, 2 * gs, 0.4, y=-gs + FLUTE_PITCH * (j + 0.5)) for j in range(nweb)]
    glaz = Compound(children=[_zbox(z0, z0 + SKIN, 2 * gs, 2 * gs), _zbox(z1 - SKIN, z1, 2 * gs, 2 * gs)] + webs)
    layer("Twin-wall polycarbonate glazing", glaz, CUT0 + 45.0, C_GLAZ, "clear", 1, "shell", along(n, ex_glaz))
    add("Glazing tape", C["tape"], C_TAPE, "rubber", 15, "shell", along(n, ex_glaz - 60))

    # ------------------------------------------------------------ frame: walls, liner, base ring
    walls = _union([C[k] for k in ("wall_side_r", "wall_side_l", "wall_high", "wall_low", "wall_low_cap")])
    add("Insulated frame, painted plywood", walls, C_FRAME, "painted", 2, "shell", (0, 0, 0))
    ring = _union([C[k] for k in ("ring_side_r", "ring_side_l", "ring_high", "ring_low")])
    add("Base ring, painted plywood", ring, C_FRAME, "painted", 2, "shell", (0, 0, 0))
    liner = _union([C[k] for k in ("liner_side_r", "liner_side_l", "liner_high", "liner_low", "liner_low_cap")])
    add("Stone wool liner, foil face", liner, C_LINER, "metal", 2, "shell", (0, 0, 0))

    # glazing trim and stainless screws on its hanging leg (BOM 15, 13)
    add("Glazing trim, anodized aluminum", C["trim"], C_TRIM, "metal", 15, "shell", along(n, ex_trim))
    gt = D["glaz_z"] + p["glaz_t"]
    xo = OH + p["trim"][2]
    zh = gt + p["trim"][2] - 15.0
    heads = []
    for t in (-400, -200, 0, 200, 400):
        for sg in (-1, 1):
            heads.append(Pos(t, sg * (xo + 0.75), zh) * Rot(90, 0, 0) * Cylinder(3.2, 1.5))
            heads.append(Pos(sg * (xo + 0.75), t, zh) * Rot(0, 90, 0) * Cylinder(3.2, 1.5))
    add("Stainless trim screws", _compound(heads), C_STEEL, "metal", 13, "shell", along(n, ex_trim + 60))

    # nameplate on the front (-Y) face of the frame, near the low end
    npx, npz = 250.0, D["wall_top"] / 2
    plate_ = Pos(npx, -OH - 0.4, npz) * Box(190.0, 0.8, 34.0)
    plate_ = _fillet_try(plate_, plate_.edges().filter_by(Axis.Y), [3.0, 2.0])
    add("Nameplate", plate_, C_ACCENT, "plastic", None, "shell", (0, 0, 0))
    txt = _text("STILLSTACK", 17.0, Plane(origin=(npx, -OH - 0.8, npz), x_dir=(1, 0, 0), z_dir=(0, -1, 0)))
    add("Nameplate lettering", txt, C_WHITE, "plastic", None, "shell", (0, 0, 0))

    # ------------------------------------------------------------ feed trough (BOM 8, 17), brackets, drip valve
    ex_tr = plus(along(down, -300), along(n, 120))
    add("Feed trough (PVC gutter)", C["trough"], C_TROUGH, "plastic", 8, "shell", ex_tr)
    add("Trough brackets", C["trough_brackets"], C_PLATE, "metal", 8, "shell", ex_tr)
    add("Foam closure", C["closure"], C_FOAM, "rubber", 17, "shell", ex_tr)
    xi, tw_, rim = p["trough"]
    tx = -xi - tw_ / 2
    tz = rim - tw_ / 2
    vy = -AP / 2
    valve = Pos(tx, vy - 9, tz) * Rot(90, 0, 0) * Cylinder(6.0, 18.0)
    valve = valve + Pos(tx, vy - 20, tz) * Rot(90, 0, 0) * Cylinder(3.5, 8.0)
    add("Drip valve body (front end of the trough)", valve, C_STEEL, "metal", 8, "shell", ex_tr)
    lever = _box(tx, vy - 12, tz + 14, 6.0, 4.0, 22.0)
    lever = _fillet_try(lever, lever.edges().filter_by(Axis.Y), [1.5, 1.0])
    add("Drip valve lever", lever, C_ACCENT, "plastic", 8, "shell", ex_tr)

    # ------------------------------------------------------------ distillate manifold (BOM 9), removable lid, brackets
    mx, mw, mh = p["manifold"]
    lz = p["lid_z"]
    ex_m = plus(along(down, 260), along(n, 140))
    add("Distillate manifold channel (food-grade PP)", C["manifold"], C_MANI, "plastic", 9, "shell", ex_m)
    lid = C["lid"]
    lid = lid + _compound([_box(mx + mw + 0.6, y, lz - 4, 1.2, 24, 10) for y in (-380, -130, 130, 380)])
    add("Distillate manifold lid (removable)", lid, C_MANI, "plastic", 9, "shell", plus(ex_m, along(n, 70)))
    add("Outlet brackets", C["outlet_brackets"], C_PLATE, "metal", 16, "shell", plus(ex_m, along(n, -40)))
    lx, lzc = mx + mw, lz - mh / 2
    add("Distillate label band", Pos(lx + 0.3, -AP / 2 + 170, lzc) * Box(0.6, 150, 20), C_ACCENT, "plastic", 19, "shell", ex_m)
    add("Distillate label lettering",
        _text("DISTILLATE", 11.0, Plane(origin=(lx + 0.6, -AP / 2 + 170, lzc), x_dir=(0, 1, 0), z_dir=(1, 0, 0)), h=0.3),
        C_WHITE, "plastic", 19, "shell", ex_m)
    barb = Pos(mx + mw / 2, AP / 2 - 30, lz - mh - 66) * (Cylinder(4.5, 12) - Cylinder(3.0, 14))
    add("Distillate outlet barb", barb, C_ACCENT, "plastic", 9, "shell", ex_m)

    # ------------------------------------------------------------ brine gutter (BOM 10) with label
    gx, gw, gh = p["gutter"]
    ex_b = plus(along(down, 420), along(n, -60))
    add("Brine gutter (PVC)", C["gutter"], C_BRINE, "plastic", 10, "shell", ex_b)
    gzc = lz - mh + gh / 2
    add("Brine label band", Pos(gx + gw + 0.3, -AP / 2 + 170, gzc) * Box(0.6, 110, 20), C_ACCENT, "plastic", 19, "shell", ex_b)
    add("Brine label lettering",
        _text("BRINE", 11.0, Plane(origin=(gx + gw + 0.6, -AP / 2 + 170, gzc), x_dir=(0, 1, 0), z_dir=(1, 0, 0)), h=0.3),
        C_WHITE, "plastic", 19, "shell", ex_b)

    # ------------------------------------------------------------ stand (BOM 12), as model.py
    ex_s = (0, 0, -520)
    add("Adjustable tilt stand (timber)", _union([W[k] for k in ("ground_rails", "cross_rails", "posts", "gussets", "prop_blocks", "props")]),
        C_TIMBER, "wood", 12, "shell", ex_s, local_frame=False)
    add("Stand bolts (M10 stainless)", W["stand_bolts"], C_STEEL, "metal", 12, "shell", ex_s, local_frame=False)

    # ------------------------------------------------------------ context: ground patch, outlet tube, brine hose, jar
    bb = Compound(children=list(W.values())).bounding_box()
    gx0, gx1 = bb.min.X - 90, bb.max.X + 200
    gy0, gy1 = bb.min.Y - 90, bb.max.Y + 90
    ground = _rrect(gx1 - gx0, gy1 - gy0, 60, -20.0, 20.0, x=(gx0 + gx1) / 2, y=(gy0 + gy1) / 2)
    ground = _fillet_try(ground, ground.faces().sort_by(Axis.Z)[-1].edges(), [8.0, 4.0])
    add("Ground patch (packed gravel)", ground, C_GROUND, "paper", None, "context", (0, 0, 0), local_frame=False)

    t0 = wp(mx + mw / 2, AP / 2 - 30, lz - mh - 71)
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

    b0 = wp(gx + gw / 2, -AP / 2 + 30, lz - mh - 41)
    hose = _pipe([b0, (b0[0], b0[1], 12.0), (b0[0] + 60, b0[1], 8.0), (gx1 - 40, b0[1] - 60, 8.0)], 7.0)
    add("Brine drain hose", hose, "#4B5563", "rubber", 10, "context", (0, 0, 0), local_frame=False)

    # ------------------------------------------------------------ accessory: stagnation cover (BOM 14), folded
    cvx, cvy = gx0 + 260, gy0 - 260
    cover = _rrect(360, 260, 30, 0.0, 44.0, x=cvx, y=cvy)
    cover = _fillet_try(cover, cover.faces().sort_by(Axis.Z)[-1].edges(), [12.0, 8.0, 4.0])
    add("Stagnation cover (folded tarpaulin)", cover, C_COVER, "fabric", 14, "accessory", (0, 0, -520),
        local_frame=False)
    cord = _compound([Pos(cvx, cvy + dy, 22.0) * Rot(0, 90, 0) * Cylinder(3.0, 366.0) for dy in (-70, 70)])
    add("Stagnation cover edge cord", cord, "#374151", "rubber", 14, "accessory", (0, 0, -520), local_frame=False)
    return out


if __name__ == "__main__":
    for q in product_parts():
        sh = q["shape"]
        print(f"{q['name']:52s} {q['group']:9s} {q['material']:8s} valid={sh.is_valid} vol={sh.volume / 1000:9.1f} cm3")
