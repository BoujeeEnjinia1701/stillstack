"""StillStack prototype build plan pictures (SSK-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|layouts ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components, plate, wick, stand), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/SSK-DWG-101 to 118        making sketches for the made and cut components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/low-edge.png        the plates' low edge and tongue layout (matplotlib)
    docs/05-build-plan/wall-openings.png   opening positions in the high and low walls (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
A single item can be drawn with, for example: python cad/src/build_plan_media.py sheet:105 joint:4 step:7
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as M  # noqa: E402
from model import PARAMS as P, derived, build_components, plate, wick, stand, stand_geometry, place, tongue_lengths, edge_points  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
DATE_P1 = "2026-10-01"
D = derived(P)
TILT = P["tilt"]

COL = {"wall": "#B08D57", "liner": "#C9CDD2", "ring": "#8B6B3E", "stop": "#7C2D12", "plate": "#A8B0B8",
       "bottom": "#7B8794", "absorber": "#1F2937", "wick": "#E2C98F", "rail12": "#D4A373", "rail34": "#0F766E",
       "rib": "#DC2626", "dam": "#F472B6", "fin": "#6B7280", "tape": "#111827", "glazing": "#93C5FD", "trim": "#64748B",
       "manifold": "#0EA5E9", "lid": "#0369A1", "gutter": "#C2410C", "bracket": "#334155", "trough": "#2563EB",
       "closure": "#F59E0B", "timber": "#8B5E34", "gusset": "#D6A46A", "prop": "#A0522D", "bolt": "#111827",
       "dtongue": "#0284C7", "btongue": "#EA580C", "clip": "#16A34A", "pps": "#C8A27A"}

_C = None


def C():
    global _C
    if _C is None:
        _C = build_components(P, local_only=True)
    return _C


def U(*shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & M._box(x0, x1, y0, y1, z0, z1)


def straight_plate(lvl):
    kind = "bottom" if lvl == 0 else ("absorber" if lvl == 4 else "cond")
    sh, _ = plate(kind, lvl, P, bent=False)
    return sh


def straight_wick(stage):
    return wick(stage, P, bent=False)


def clips_of(stage):
    return U(C()[f"clips_hi_{stage}"], C()[f"clips_lo_{stage}"])


def rv(n, what):
    """Revision P2 of a making sketch changed on 2026-10-02 (SSK-DEC-001)."""
    return dict(rev="P2", revisions=[("P1", "Making sketch for the prototype build plan", DATE_P1, "AC"), ("P2", what, DATE, "AC")])


def rot_local(off, tilt=TILT):
    """A pull-apart offset given in the panel frame, as a world vector."""
    s, c = math.sin(math.radians(tilt)), math.cos(math.radians(tilt))
    ox, oy, oz = off
    return (ox * c + oz * s, oy, -ox * s + oz * c)


# ----------------------------------------------------------------- overview
def overview():
    c = C()
    S = stand(P, TILT)
    W = lambda sh: place(sh, P, TILT)   # noqa: E731
    items = [
        ("Side walls (2) and prop blocks", U(c["wall_side_r"], c["wall_side_l"]), COL["wall"], (0, 0, 0)),
        ("High wall", c["wall_high"], COL["wall"], (-300, 0, 0)),
        ("Low wall comb and cap", U(c["wall_low"], c["wall_low_cap"]), COL["wall"], (320, 0, 0)),
        ("Base ring (4 strips)", U(c["ring_side_r"], c["ring_side_l"], c["ring_high"], c["ring_low"]), COL["ring"], (0, 0, -200)),
        ("Stone wool liner", U(c["liner_side_r"], c["liner_side_l"], c["liner_high"], c["liner_low"], c["liner_low_cap"]), COL["liner"], (0, 0, 150)),
        ("Stop blocks, PPS (2)", c["stops"], COL["stop"], (420, 0, 380)),
        ("Bottom plate with fins", U(c["plate_bottom"], c["fins"]), COL["bottom"], (-120, 0, 300)),
        ("Side rails, stages 3 and 4, printed PC (4)", U(c["rails_3"], c["rails_4"]), COL["rail34"], (-260, 0, 400)),
        ("Side rails, stages 1 and 2, PPS (4)", U(c["rails_1"], c["rails_2"]), COL["pps"], (-300, 0, 470)),
        ("Spacer ribs (16) and dams", U(*[c[f"ribs_{s}"] for s in range(1, 5)], *[c[f"dams_{s}"] for s in range(1, 4)]), COL["rib"], (-330, 0, 470)),
        ("Condenser plates (3)", U(c["plate_1"], c["plate_2"], c["plate_3"]), COL["plate"], (-520, 0, 600)),
        ("Wick strips (20)", U(*[c[f"wick_{s}"] for s in range(1, 5)]), COL["wick"], (-620, 0, 680)),
        ("Wick clips, stainless (40)", U(*[clips_of(s) for s in range(1, 5)]), COL["clip"], (-700, 0, 780)),
        ("Absorber plate", c["absorber"], COL["absorber"], (-800, 0, 880)),
        ("Glazing and tape", U(c["glazing"], c["tape"]), COL["glazing"], (-920, 0, 980)),
        ("Glazing trim (4)", c["trim"], COL["trim"], (-1040, 0, 1080)),
        ("Outlet brackets (2)", c["outlet_brackets"], COL["bracket"], (520, 0, -60)),
        ("Distillate manifold and lid", U(c["manifold"], c["lid"]), COL["manifold"], (560, 0, 80)),
        ("Brine gutter", c["gutter"], COL["gutter"], (680, 0, -180)),
        ("Feed trough, brackets, closure", U(c["trough"], c["trough_brackets"], c["closure"]), COL["trough"], (-480, 0, 60)),
    ]
    parts = [Part(n, W(sh), col, None, rot_local(off), 1.0) for n, sh, col, off in items]
    parts[0] = Part(parts[0].name, U(parts[0].shape, S["prop_blocks"]), COL["wall"], None, (0, 0, 0), 1.0)
    parts += [Part("Ground frame, posts, gussets", U(S["ground_rails"], S["cross_rails"], S["posts"], S["gussets"]), COL["timber"], None, (0, 0, -420), 1.0),
              Part("Props (2)", S["props"], COL["prop"], None, (-150, 0, -300), 1.0)]
    return bv.overview(parts, OUT / "overview.png", "StillStack prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Panel at 20 deg on its stand, seen from the front left and above",
                       elev=24, azim=-115, size=(13, 9.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def flat_xy(shape):
    return shape


def sheets(only=None):
    import build123d as b
    c = C()
    base = dict(project="StillStack", date=DATE)
    out = []
    OH, li, h = D["OH"], P["aperture"] / 2, D["half"]
    G = stand_geometry(P, TILT)
    S = stand(P, TILT)
    frame_ctx = [part("Walls", U(c["wall_side_r"], c["wall_side_l"], c["wall_high"], c["wall_low"]), COL["wall"])]

    def want(n):
        return only is None or n in only

    strips = D["strips"]
    op_hi = [f"{(a - 5):.0f} to {(b + 5):.0f}" for a, b in strips if a > -1]
    yd = sorted(set(round(abs(y), 1) for y in D["yd"]))
    yb = sorted(set(round(abs(y), 1) for y in D["yb"]))

    if want(101):
        blk = M._box(P["prop_hinge"][0] - 60, P["prop_hinge"][0] + 60, OH, OH + P["post"], D["FZ0"], D["FZ0"] + P["post"])
        sh = U(c["wall_side_r"], blk)
        for hx_, hz_ in (P["pivot"], P["prop_hinge"]):
            sh = sh - b.Pos(hx_, OH, hz_) * b.Rot(90, 0, 0) * b.Cylinder(5.25, 200)
        out.append(bv.component_sheet(
            part("Side wall", sh, COL["wall"]), [part("Base ring", c["ring_side_r"], COL["ring"]), part("Other walls", U(c["wall_high"], c["wall_low"], c["wall_side_l"]), COL["wall"])],
            dwg_no="SSK-DWG-101", title="StillStack side wall (make 2, a left and a right): making sketch",
            material="Exterior plywood 12 mm; prop block 45 x 45 mm timber",
            view_shape=b.Rot(90, 0, 0) * b.Pos(0, -(OH - 6), 0) * sh, inset_view=(25, -60),
            notes=[f"Rip a strip 1,074 x {D['wall_top']:.1f} mm from 12 mm exterior plywood.",
                   "Mark the low end (toward the outlets) and the high end (feed).",
                   "Pivot hole 10.5 mm: 25 mm from the low end, 10 mm up from the",
                   "  bottom edge. Prop hinge hole 10.5 mm: 67 mm from the high end,",
                   "  10 mm up. Drill square to the face.",
                   "Prop block: 45 x 45 mm timber 120 mm long, glued (exterior PU) and",
                   "  screwed (4 x 40 mm, 4 screws) to the outside face, 7 mm from the",
                   "  high end, its bottom 12 mm below the wall (over the base ring).",
                   "  Drill the prop hinge hole on through the block.",
                   "Fit: the end walls sit between the side walls; glue and three",
                   "  4 x 40 mm screws per corner through the side wall into the end wall.",
                   "Seal all edges with exterior paint before assembly.",
                   "Check: both walls the same length within 1 mm; holes mirror-imaged."],
            **base))

    if want(102):
        sh = c["wall_high"]
        out.append(bv.component_sheet(
            part("High wall", sh, COL["wall"]), [part("Side walls", U(c["wall_side_r"], c["wall_side_l"]), COL["wall"]), part("Trough", c["trough"], COL["trough"])],
            dwg_no="SSK-DWG-102", title="StillStack high wall (feed end): making sketch",
            material="Exterior plywood 12 mm", view_shape=b.Rot(0, 0, 90) * b.Rot(0, 90, 0) * b.Pos(OH - 6, 0, 0) * sh, inset_view=(25, 140),
            notes=[f"Rip a strip 1,050 x {D['wall_top']:.1f} mm from 12 mm exterior plywood.",
                   f"Five feed openings, one per wick strip, {D['open_top']:.0f} mm tall from the",
                   "  bottom edge. From the centre line, the same each side (mm):",
                   "  middle opening " + str(int(round(strips[2][1] + 5))) + " each side of centre; others "
                   + "; ".join(op_hi) + ".",
                   "Drill a 10 mm hole in each top corner of an opening, cut down to",
                   "  the bottom edge with a jigsaw, file square.",
                   "The posts left between openings are about 17 mm wide, on the rib",
                   "  lines; handle the wall flat until it is in the frame.",
                   "Cut the stone wool liner for this wall with the same openings.",
                   "Fit: between the side walls, its bottom edge on the base ring.",
                   "The wick tails pass out through the openings to the trough.",
                   "Check: openings line up with the wick strip positions."],
            **base))

    if want(103):
        sh = U(c["wall_low"], b.Pos(0, 0, 40) * c["wall_low_cap"])
        out.append(bv.component_sheet(
            part("Low wall comb and cap", sh, COL["wall"]), [part("Side walls", U(c["wall_side_r"], c["wall_side_l"]), COL["wall"]), part("Manifold", c["manifold"], COL["manifold"])],
            dwg_no="SSK-DWG-103", title="StillStack low wall comb and cap (outlet end): making sketch",
            material="Exterior plywood 12 mm", view_shape=b.Rot(0, 0, 90) * b.Rot(0, 90, 0) * b.Pos(-(OH - 6), 0, 0) * sh, inset_view=(25, -40),
            notes=[f"Comb: strip 1,050 x {D['open_top'] + 12:.0f} mm. Cap: strip 1,050 x {D['wall_top'] - D['open_top']:.1f} mm.",
                   "  (The views show the cap lifted 40 mm above the comb.)",
                   f"Eleven notches cut down from the comb's top edge, {D['open_top']:.0f} mm deep,",
                   "  leaving a 12 mm sill along the bottom. From the centre line:",
                   "  40 mm wide (distillate tongues) at " + ", ".join(f"{y:g}" for y in yd) + " each side;",
                   "  60 mm wide (brine tongues) at 0 and " + ", ".join(f"{y:g}" for y in yb if y > 0) + " each side.",
                   "Saw the notch sides, chop out with a chisel, file square.",
                   "Fit: the comb sits between the side walls, its sill on the same",
                   "  level as the base ring (inside it). The cap sits on the teeth,",
                   "  held by two 4 x 30 mm screws into the side walls' end grain.",
                   "Each plate drops in from above with its tongues in the notches;",
                   "  the cap closes the notches above the stack.",
                   "Check: every notch 33 mm deep; the cap sits flat on all teeth."],
            **base))

    if want(104):
        sh = U(c["ring_side_r"], c["ring_side_l"], c["ring_high"], c["ring_low"])
        out.append(bv.component_sheet(
            part("Base ring", sh, COL["ring"]), frame_ctx,
            dwg_no="SSK-DWG-104", title="StillStack base ring (4 strips): making sketch",
            material="Exterior plywood 12 mm", inset_view=(-30, -60), **rv(104, "Slots for the bottom plate's lip tabs (SSK-DEC-001)"),
            notes=["Four strips of 12 mm plywood, laid flat under the walls:",
                   "  two side strips 1,062 x 52 mm (flush with the outside of the side",
                   "  walls and the high wall, stopping at the low wall's inside face);",
                   "  high strip 52 x 970 mm; low strip 40 x 970 mm, between the sides.",
                   "High strip: four 4 mm wide slots 5 mm deep cut down from its top face,",
                   "  1.5 mm clear either side of each lip tab of the bottom plate (at the rib",
                   "  lines, from the centre line: 97.2 and 291.6 mm each side).",
                   "Each strip reaches 15 mm past the liner into the aperture: this",
                   "  ledge carries the edges of the bottom plate and the side rails.",
                   "The low wall comb stands outside the low strip, its sill level with it.",
                   "Fit: glue (exterior PU) and screw up into the wall bottom edges,",
                   "  4 x 40 mm screws every 150 mm, pilot drilled 2.5 mm.",
                   "Check: the inner ledge edges form a 970 mm square within 1 mm",
                   "  and lie flat (no step over 0.5 mm at the joints)."],
            **base))

    if want(105):
        sh = U(c["liner_low"], b.Pos(0, 0, 30) * c["liner_low_cap"]) & M._box(0, 1000, 0, 600, -50, 200)
        out.append(bv.component_sheet(
            part("Liner, low end", sh, COL["liner"]), [part("Low wall", c["wall_low"], COL["wall"]), part("Stop blocks", c["stops"], COL["stop"])],
            dwg_no="SSK-DWG-105", title="StillStack stone wool liner, low end pieces: making sketch",
            material="Foil-faced stone wool board 25 mm, rated well above 150 C",
            view_shape=b.Rot(0, 0, 90) * b.Rot(0, 90, 0) * b.Pos(-(li + 12.5), 0, 0) * sh, inset_view=(35, 150),
            notes=["Cut with a long bread knife or a fine saw; wear gloves, a dust mask",
                   "  and glasses. Foil face toward the stack.",
                   "Side pieces 1,050 x 52.5 mm; high piece 1,000 x 52.5 mm with the",
                   "  same five openings as the high wall.",
                   "Low end: ten blocks 33 mm tall that fill the spaces between the",
                   "  low wall's notches (the end ones stop 15 mm short of each side,",
                   "  for the stop blocks), and a cap piece 1,000 x 19.5 mm.",
                   "  Drawn: the right half, cap lifted 30 mm; the left is a mirror image.",
                   "Glue each piece to its wall with high-temperature silicone.",
                   "Pockets: cut a 30 mm hole 10 mm deep behind the pivot and prop",
                   "  hinge holes in the side pieces for the nut and washer.",
                   "Check: the foil face is unbroken except at the openings."],
            **base))

    if want(106):
        st = c["stops"] & M._box(0, 600, 0, 600, -50, 100)
        out.append(bv.component_sheet(
            part("Stop block", st, COL["stop"]), [part("Side rails", U(c["rails_1"], c["rails_2"], c["rails_3"], c["rails_4"]) & M._box(300, 600, 0, 600, -50, 100), COL["rail34"]),
                                                  part("Bottom plate", c["plate_bottom"] & M._box(300, 600, 0, 600, -50, 100), COL["plate"]),
                                                  part("Low wall and side liner", U(c["wall_low"], c["liner_side_r"], c["wall_side_r"]) & M._box(300, 600, 0, 600, -50, 100), COL["wall"])],
            dwg_no="SSK-DWG-106", title="StillStack stop block (make 2): making sketch",
            material="PPS, natural (tan), the stage 1 and 2 rail polymer, rated above 150 C", inset_view=(40, 215),
            notes=[f"Cut a block 27 x 15 x {D['open_top']:.0f} mm from the offcut of the 7 mm PPS",
                   "  sheet the stage 1 and 2 rails come from (or glue two pieces together).",
                   "It fills the low corner of the liner: its back face against the",
                   "  low wall comb, its side against the side liner.",
                   "Its front face is the stop the whole stack bears on: the plate",
                   "  corners and the rail ends touch it, 498 mm from the centre.",
                   "Fit: high-temperature silicone on the back and side faces.",
                   "Check: the front faces of the two blocks are square to the side",
                   "  walls and 996 mm from the high liner face (plates' length)."],
            **rv(106, "PPS named for the stop block (SSK-DEC-001)"), **base))

    if want(107):
        sh = U(c["plate_bottom"], c["fins"])
        flat = U(straight_plate(0))
        L = tongue_lengths(0)
        out.append(bv.component_sheet(
            part("Bottom plate", sh, COL["bottom"]), [part("Base ring", U(c["ring_low"], c["ring_side_r"], c["ring_side_l"], c["ring_high"]), COL["ring"])],
            dwg_no="SSK-DWG-107", title="StillStack bottom plate (last condenser): making sketch",
            material="Aluminium sheet 0.5 mm, 3003 or 1050; food-contact coating on top face",
            view_shape=flat, inset_view=(-25, -60),
            notes=["Cut from a 1.0 x 1.25 m sheet. The body is 996 x 996 mm; the low",
                   "  edge is a zigzag (see the low edge picture): tips at the six",
                   f"  distillate tongues, roots {P['v_depth']:.0f} mm shorter at the strip centres.",
                   f"Six distillate tongues 30 mm wide, {L['d_len']:.1f} mm long from the tip line",
                   "  (drawn straight here). They stay straight until the manifold is on.",
                   "Lip: four tabs 7 mm wide on the high edge, centred on the rib lines",
                   "  (97.2 and 291.6 mm each side of the centre line), 5 mm of metal",
                   "  each; bend each 90 deg down to hang 4 mm below the plate.",
                   "Cut with aviation snips; file the edges smooth; no burrs on top.",
                   "Coat the top face (condensing face) with the fluoropolymer coating,",
                   "  tongues included, after the lip is bent and before the fins go on.",
                   "Fins: ten, bonded under it at 99.6 mm pitch with high-temperature",
                   "  silicone adhesive along each 20 mm flange (sketch SSK-DWG-108).",
                   f"Later: bend each tongue down 90 deg {L['d_bend']:.0f} mm from the tip line.",
                   "Fit: its edges rest on the base ring's 13 mm ledge; the four lip",
                   "  tabs go down into the slots in the ring's high strip.",
                   "Check: flat within 2 mm on the bench; coating unbroken."],
            **rv(107, "High-edge lip tabs, fluoropolymer coating after bending (SSK-DEC-001)"), **base))

    if want(108):
        fin = c["fins"] & M._box(-600, 600, -500, -400, -50, 10)
        out.append(bv.component_sheet(
            part("Fin", fin, COL["fin"]), [part("Bottom plate", c["plate_bottom"], COL["bottom"])],
            dwg_no="SSK-DWG-108", title="StillStack heat-rejection fin (make 10): making sketch",
            material="Aluminium flashing or sheet 0.5 mm", view_shape=b.Pos(0, 449.0, 0) * fin, inset_view=(-30, -60),
            notes=[f"Cut ten strips 50 x {P['fin_len']:.0f} mm.",
                   "Fold each 90 deg along its length, 20 mm from one edge, between two",
                   "  hardwood battens clamped in a vice: a 20 mm flange and a 30 mm web.",
                   "Bond the flange under the bottom plate with high-temperature",
                   "  silicone adhesive, web hanging down, running down the slope.",
                   f"Pitch 99.6 mm; first fin 49.8 mm in from the side edge; ends {(D['half'] * 2 - P['fin_len']) / 2:.0f} mm",
                   "  in from the plate's high edge and clear of the low edge zigzag.",
                   "Check: each fin square to the plate within 5 deg; adhesive along",
                   "  the whole flange."],
            **base))

    if want(109):
        r = c["rails_1"] & M._box(-600, 600, 0, 600, -50, 100)
        out.append(bv.component_sheet(
            part("Side rail", r, COL["rail12"]), [part("Plate below it", c["plate_1"], COL["plate"])],
            dwg_no="SSK-DWG-109", title="StillStack side rail (make 8): making sketch",
            material="Stages 1, 2: PPS, natural (tan), above 150 C. Stages 3, 4: printed PC, teal",
            view_shape=b.Rot(0, 0, 90) * b.Pos(0, -492.0, -26.0) * r, inset_view=(30, -40),
            notes=["Eight rails, 996 x 12 x 7 mm, two per stage.",
                   "Stages 1 and 2 (the top two gaps): cut four strips 12 mm wide",
                   "  from 7 mm natural (tan) PPS sheet; keep the offcut for the stop blocks.",
                   "Stages 3 and 4: print four rails in teal polycarbonate in four 249 mm",
                   "  sections each, butt-joined with high-temperature silicone.",
                   "Mark each rail with its stage number on the outside face; stages",
                   "  1 and 2 must never swap with 3 and 4.",
                   "Fit: each rail lies along a side edge of the plate below, flush",
                   "  with it, and its low end touches the stop block.",
                   "The wick strips stop 10 mm short of the rail (dry break).",
                   "Check: 7.0 mm thick within 0.2 mm along the whole length."],
            **rv(109, "PPS named for stages 1 and 2, teal PC for stages 3 and 4 (SSK-DEC-001)"), **base))

    if want(110):
        sh = straight_plate(2)
        L1, L2, L3 = (tongue_lengths(k) for k in (1, 2, 3))
        out.append(bv.component_sheet(
            part("Condenser plate", sh, COL["plate"]), [part("Rails", U(c["rails_2"], c["rails_3"]), COL["rail34"]), part("Frame", c["wall_low"], COL["wall"])],
            dwg_no="SSK-DWG-110", title="StillStack condenser plates 1 to 3 (make 3): making sketch",
            material="Aluminium sheet 0.5 mm, 3003 or 1050; food-contact coating on top face", inset_view=(30, -40),
            notes=["Cut each from a 1.0 x 1.25 m sheet; body as the bottom plate:",
                   "  996 x 996 mm with the same zigzag low edge (drawn: plate 2).",
                   "Six distillate tongues 30 mm wide at the tips and five brine",
                   "  tongues 50 mm wide at the roots, all left straight. Lengths:",
                   f"  plate 3 (lowest): distillate {L1['d_len']:.0f}, brine {L1['b_len']:.0f} mm",
                   f"  plate 2: distillate {L2['d_len']:.0f}, brine {L2['b_len']:.0f} mm",
                   f"  plate 1 (highest): distillate {L3['d_len']:.0f}, brine {L3['b_len']:.0f} mm",
                   "  (distillate from the tip line, brine from the root line).",
                   "Lip: four 7 mm tabs on the high edge at the rib lines (97.2 and",
                   "  291.6 mm each side), bent 90 deg down 4 mm, before coating.",
                   "Coat the top face; clip the five wick strips under it (SSK-DWG-111).",
                   "After it is in the frame: a chevron of silicone on the top face at",
                   "  each brine tongue root (point up the slope, 3 mm high).",
                   "Later bends: distillate 51, 55, 59 mm from the tip line; brine",
                   "  143, 147, 151 mm from the root line (plates 3, 2, 1)."],
            **rv(110, "High-edge lip tabs, wick clips in place of bonding (SSK-DEC-001)"), **base))

    if want(111):
        stg = 2
        a, b_ = strips[2]
        body, tails = wick(stg, P, bent=False, split=True)
        sh = U(body, tails) & M._box(-OH - 0.5, 900, a - 1, b_ + 1, D["levels"][3] - 1.01, D["levels"][3] + 0.01)
        lv = derived(P)["levels"][3]
        hi_len = 498 - (-OH - stg) + 0  # body runs out to the rising tail
        out.append(bv.component_sheet(
            part("Wick strip", sh, COL["wick"]), [part("Plate above", straight_plate(3), COL["plate"]),
                                                  part("Wick clips", U(C()["clips_hi_2"], C()["clips_lo_2"]) & M._box(-OH - 1, 900, a - 20, b_ + 20, -50, 100), COL["clip"])],
            dwg_no="SSK-DWG-111", title="StillStack wick strip (make 20, 5 per stage): cutting sketch",
            material="Viscose-polyester or cotton nonwoven about 1 mm, 150 C dry",
            inset_view=(-35, -60),
            notes=["Five strips per stage: 171, 167, 167, 167 and 171 mm wide.",
                   "Cut from a 1.0 x 1.4 m piece; the views show the part that lies",
                   "  under the plate, from the high wall's outside face to the brine tail.",
                   "Low end: follow the plate's zigzag 13 mm inside it (10 mm dry",
                   "  break), then a 30 mm wide tail along the middle of the brine",
                   "  tongue, as long as the tongue (plus 10 mm).",
                   "High end: leave 150 mm extra beyond the plate's high edge for",
                   "  the feed tail (out through the opening, up the wall, into the trough).",
                   "Hold it under the plate with two stainless clips and no adhesive:",
                   "  a high-end clip (SSK-DWG-119) at the plate's high edge and a",
                   "  tongue clip over the brine tongue and the tail (SSK-DWG-120).",
                   "The strip edges stay 10 mm from the ribs and rails (dry breaks).",
                   "Check: no fibre bridges a dry break; tail centred on its tongue."],
            **rv(111, "Wick clips in place of silicone dots (SSK-DEC-001)"), **base))

    if want(112):
        sh = straight_plate(4)
        L = tongue_lengths(4)
        out.append(bv.component_sheet(
            part("Absorber plate", sh, COL["absorber"]), [part("Walls", U(c["wall_low"], c["wall_side_r"], c["wall_side_l"], c["wall_high"]), COL["wall"])],
            dwg_no="SSK-DWG-112", title="StillStack absorber plate: making sketch",
            material="Aluminium sheet 0.5 mm; high-temperature matte black paint on top", inset_view=(35, -40),
            notes=["Cut from a 1.0 x 1.25 m sheet: body 996 x 996 mm with the same",
                   "  zigzag low edge; five brine tongues 50 mm wide, "
                   f"{L['b_len']:.0f} mm long",
                   "  from the root line; no distillate tongues (cut the tips flush).",
                   "Paint the top face matte black (high-temperature, 600 C class),",
                   "  tongues excluded. Leave the underside bare.",
                   "Bond wick 1 (five strips) under it, as the condenser plates.",
                   f"Later bend: brine tongues down 90 deg {L['b_bend']:.0f} mm from the root line.",
                   "Fit: it rests on the stage 1 rails and ribs; its corners touch",
                   "  the stop blocks. Nothing is fixed to it.",
                   "Check: paint fully cured (bake at the maker's schedule) before",
                   "  it goes in; no paint on the underside."],
            **base))

    if want(113):
        gt = D["glaz_z"] + P["glaz_t"]
        xo = OH + P["trim"][2]
        tl = P["trim"][0]
        tr = M._prism([(-xo, xo), (xo, xo), (xo - tl, xo - tl), (-xo + tl, xo - tl)], gt, P["trim"][2])   # mitred top leg
        tr = tr + M._box(-OH - 1, OH + 1, OH, xo, gt + P["trim"][2] - P["trim"][1], gt + P["trim"][2])     # hanging leg
        out.append(bv.component_sheet(
            part("Glazing trim", tr, COL["trim"]), [part("Glazing", c["glazing"], COL["glazing"]), part("Side wall", c["wall_side_r"], COL["wall"])],
            dwg_no="SSK-DWG-113", title="StillStack glazing trim (make 4): making sketch",
            material="Aluminium unequal angle 25 x 20 x 2 mm", view_shape=b.Rot(0, 0, 90) * b.Pos(0, -(OH - 10), -60) * tr, inset_view=(35, -60),
            notes=["Four lengths of 25 x 20 x 2 mm angle, 1,078 mm long on the",
                   "  outside corner, mitred 45 deg at both ends.",
                   "The 25 mm leg lies on the glazing edge; the 20 mm leg hangs down",
                   "  the outside of the wall.",
                   "Drill the 20 mm leg 4.5 mm every 200 mm, 15 mm from the top",
                   "  (about 8 mm into the wall below the tape and glazing).",
                   "Run a bead of silicone under the 25 mm leg.",
                   "The leg's inner edge stops 14 mm outside the aperture: no shade.",
                   "The glazing edge sits 7 mm inside the hanging leg: room to grow.",
                   "Fit: 4 x 20 mm stainless screws into the plywood.",
                   "Check: the trim holds the glazing down without bowing it."],
            **base))

    if want(114):
        lid = c["lid"]
        out.append(bv.component_sheet(
            part("Manifold lid", lid, COL["lid"]), [part("Manifold", c["manifold"], COL["manifold"]), part("Low wall", c["wall_low"], COL["wall"])],
            dwg_no="SSK-DWG-114", title="StillStack distillate manifold lid: slotting sketch",
            material="Bought food-grade PP or HDPE channel lid, 56 mm wide", inset_view=(40, -50),
            notes=["Cut the bought lid to 1,000 mm.",
                   "Six slots 16 x 36 mm, 3 mm in from the edge that goes against",
                   "  the low wall, centred at " + ", ".join(f"{y:g}" for y in yd) + " mm each side",
                   "  of the centre line (the distillate tongue lines).",
                   "Drill a 6 mm hole at each slot corner and cut between with a",
                   "  sharp knife; deburr. No slot anywhere else: the brine tongues",
                   "  pass 10.5 mm above the closed lid.",
                   "Clean with water and mild detergent only.",
                   "Fit: snaps onto the channel; the bent distillate tongues go 3 mm",
                   "  down into the channel through the slots.",
                   "Check: the lid is tight on the channel all along its length."],
            **base))

    if want(115):
        ob = c["outlet_brackets"] & M._box(0, 800, 0, 600, -100, 100)
        out.append(bv.component_sheet(
            part("Outlet bracket", ob, COL["bracket"]), [part("Manifold", c["manifold"], COL["manifold"]), part("Brine gutter", c["gutter"], COL["gutter"]),
                                                         part("Low wall", c["wall_low"], COL["wall"])],
            dwg_no="SSK-DWG-115", title="StillStack outlet bracket (make 2): making sketch",
            material="Aluminium flat bar 30 x 4 mm, 6063", view_shape=b.Rot(-90, 0, 0) * b.Pos(0, -P["bracket_y"], 0) * ob, inset_view=(-25, -40),
            notes=["Cut 240 mm of 30 x 4 mm flat bar per bracket.",
                   "Bend 90 deg (in a vice, over a 4 mm radius) so the upright leg",
                   "  is 88 mm and the outward leg is 143 mm, outside sizes.",
                   "Upright leg: three 4.5 mm holes, 6, 22 and 36 mm down from its top",
                   "  (into a tooth of the low wall comb and its sill).",
                   f"Fit: at {P['bracket_y']:.0f} mm each side of the centre line, on a tooth.",
                   "The manifold sits on the outward leg against the upright; the",
                   "  brine gutter sits on its outer end, 7 mm further out.",
                   "Use stainless 4 x 25 mm screws.",
                   "Check: the outward leg is square to the wall; both brackets at",
                   "  the same height within 1 mm (the manifold must not tip)."],
            **base))

    if want(116):
        gr = S["ground_rails"] & M._box(-3000, 3000, 0, 3000, -10, 100)
        px = G["pivot"][0]
        hl = [f"{t:.0f} deg {abs(x - px):.0f}" for t, x in G["holes"].items()]
        out.append(bv.component_sheet(
            part("Ground rail", gr, COL["timber"]), [part("Post", S["posts"], COL["timber"]), part("Props", S["props"], COL["prop"])],
            dwg_no="SSK-DWG-116", title="StillStack ground rail (make 2) and cross rails: making sketch",
            material="45 x 45 mm treated timber, outdoor grade (not in the water path)",
            view_shape=b.Rot(-90, 0, 0) * b.Pos(0, -(OH + 22.5), 0) * gr, inset_view=(25, -60),
            notes=[f"Ground rails: two lengths of {gr.bounding_box().size.X:.0f} mm.",
                   "Mark the post centre 67.5 mm from the front end (760 mm from the rear).",
                   "Prop holes 10.5 mm through the side, mid-height, measured back",
                   "  from the post centre (tilt and distance in mm):",
                   "  " + ", ".join(hl[:3]) + ",",
                   "  " + ", ".join(hl[3:]) + ".",
                   "Cross rails: two lengths of 1,074 mm, between the ground rails at",
                   "  the front and rear ends; four galvanised corner brackets.",
                   "Drill a 12 mm hole near each end of each ground rail for a",
                   "  ground stake (or put ballast on the cross rails).",
                   "Check: the frame is square (diagonals equal within 3 mm)."],
            **base))

    if want(117):
        post = S["posts"] & M._box(-3000, 3000, 0, 3000, -10, 2000)
        gus = S["gussets"] & M._box(-3000, 3000, 0, 3000, -10, 2000)
        ph = post.bounding_box().size.Z
        out.append(bv.component_sheet(
            part("Post and gusset", U(post, gus), COL["timber"]), [part("Ground rail", S["ground_rails"], COL["timber"]), part("Side wall", place(c["wall_side_r"], P, TILT), COL["wall"])],
            dwg_no="SSK-DWG-117", title="StillStack front post and gusset (make 2 of each): making sketch",
            material="45 x 45 mm treated timber; gusset 12 mm exterior plywood",
            view_shape=b.Rot(-90, 0, 0) * b.Pos(0, -(OH + 22.5), 0) * U(post, gus), inset_view=(25, -60),
            notes=[f"Post: 45 x 45 mm, {ph:.0f} mm long, ends square.",
                   "Pivot hole 10.5 mm, 22 mm down from the top, through the side",
                   "  that faces the panel.",
                   f"Gusset: a right triangle of 12 mm plywood, legs {P['post'] + P['gusset']:.0f} mm.",
                   "Fit: the post stands on top of the ground rail at its post mark;",
                   "  the gusset is glued and screwed (8 x 4 x 40 mm) to the inside",
                   "  faces of both, behind the post, making the joint rigid.",
                   "The post's inside face touches the side wall; the pivot bolt",
                   "  (M10 x 70 stainless) goes through post and wall, nut and large",
                   "  washer inside the wall, in the liner pocket.",
                   "Check: the post is upright (spirit level) on a level rail."],
            **base))

    if want(118):
        pr = S["props"] & M._box(-3000, 3000, 0, 3000, -10, 2000)
        hx, hz = G["hinge"]; fx, fz = G["foot"]
        ang = math.atan2(fx - hx, hz - fz)
        pf = b.Rot(0, math.degrees(ang), 0) * b.Pos(-(hx + fx) / 2, -(OH + 67.5), -(hz + fz) / 2) * pr
        out.append(bv.component_sheet(
            part("Prop", pr, COL["prop"]), [part("Ground rail", S["ground_rails"], COL["timber"]), part("Side wall", place(c["wall_side_r"], P, TILT), COL["wall"]),
                                            part("Prop block", S["prop_blocks"], COL["wall"])],
            dwg_no="SSK-DWG-118", title="StillStack prop (make 2): making sketch",
            material="45 x 45 mm treated timber", view_shape=b.Rot(-90, 0, 0) * pf, inset_view=(20, 60),
            notes=[f"Cut two lengths of {P['prop_len'] + 44:.0f} mm; edges eased. Square the top end;",
                   "  round the foot end to a 22 mm radius about its hole (clears the ground).",
                   f"Two 10.5 mm holes through the side, 22 mm from each end:",
                   f"  {P['prop_len']:.0f} mm between centres. Drill both props clamped together.",
                   "Top: an M10 x 120 stainless bolt through the prop, the prop block",
                   "  and the side wall (nut and washer inside the wall).",
                   "Foot: lies against the outside face of the ground rail; an M10",
                   "  x 100 stainless bolt with a wing nut through the prop and the",
                   "  rail hole for the tilt you want (the stand pins).",
                   "To change the tilt: support the panel, pull both foot pins, swing",
                   "  the props to the new holes, refit the pins.",
                   "Check: hole centres 1,000 mm apart within 1 mm."],
            **base))

    if want(119):
        a2, b2 = strips[2]
        win_ = M._box(-600, -400, a2 - 12, b2 + 12, -100, 100)
        hi = C()["clips_hi_2"] & win_
        bar = (b2 - a2) + 2 * (P["clip_ear"] + 1.0)
        ear = (P["clip_t"] + 1.0) + (1.0 + P["plate_t"] + 2 * P["clip_t"]) + P["clip_flap"] + P["clip_t"]
        out.append(bv.component_sheet(
            part("High-end wick clip", hi, COL["clip"]),
            [part("Plate", C()["plate_1"] & win_, COL["plate"]), part("Wick", C()["wick_2"] & win_, COL["wick"]),
             part("Rib", C()["ribs_2"] & win_, COL["rib"]), part("High liner", C()["liner_high"] & win_, COL["liner"])],
            dwg_no="SSK-DWG-119", title="StillStack high-end wick clip (make 20): making sketch",
            material="304 stainless strip 0.4 x 8 mm (food contact)", view_shape=hi, inset_view=(30, -50),
            notes=[f"Cut 20 lengths of strip: {bar + 2 * ear:.0f} mm for the three 167 mm wide",
                   "  strips of a stage, 4 mm more for the two 171 mm ones; ends filed.",
                   f"Mark the bar: {bar:.0f} mm in the middle (the strip's width plus 9 mm",
                   "  past each edge). Beyond each bar end the strip makes three folds:",
                   "  first out 1.4 mm under the plate's high edge, then up 2.3 mm along",
                   f"  the edge, then {P['clip_flap']:.0f} mm flat over the plate's top face.",
                   "Fold each in a vice between two steel plates, springing the flap",
                   "  about 5 deg tighter than square so it grips the plate.",
                   "Fit: the bar lies under the wick strip, 1 to 9 mm in from the plate's",
                   "  high edge; each ear sits in the 8 mm dry break beside the strip,",
                   "  with the flap flat on the plate's top, clear of the rib and the lip tab.",
                   "No adhesive: the clip is slid on from the high edge and lifts off.",
                   "Check: the wick is pressed flat to the plate; no clip part touches a",
                   "  rib, a lip tab or the liner (1.5 mm to the nearest)."],
            **base))

    if want(120):
        lo = C()["clips_lo_2"] & M._box(400, 600, -40, 40, -100, 100)
        win2 = M._box(400, 700, -45, 45, -100, 100)
        out.append(bv.component_sheet(
            part("Brine tongue clip", lo, COL["clip"]),
            [part("Brine tongue (plate 1)", C()["plate_1"] & win2, COL["plate"]), part("Wick tail", C()["wick_2"] & win2, COL["wick"]),
             part("Chevron dam", C()["dams_1"] & win2, COL["dam"])],
            dwg_no="SSK-DWG-120", title="StillStack brine tongue clip (make 20): making sketch",
            material="304 stainless strip 0.4 x 8 mm (food contact)", view_shape=lo, inset_view=(35, -50),
            notes=["Cut 20 lengths of strip 62 mm long; ends filed.",
                   "Fold into a U that fits round a 50 mm wide tongue and the 30 mm",
                   "  wick tail under it: a 51 mm base, two 2.3 mm legs, and a 3.4 mm",
                   "  flange turned in over the top of the tongue at the top of each leg.",
                   "Spring the flanges about 5 deg tighter than square so they grip.",
                   "Fit: slid on from the tongue's tip before the tongue is bent, its",
                   "  8 mm width lying 7 to 15 mm past the tongue root line, which is",
                   "  clear of the chevron dam (7 mm or more) and of the wall notch.",
                   "The base lies under the wick tail, holding it against the tongue.",
                   "Slide it off the tip to lift the wick out; no adhesive.",
                   "Check: the tail is centred under the tongue and pressed flat;",
                   "  the clip is at least 10 mm from the lid once the tongue is bent."],
            **base))
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    c = C()
    out = []
    h, OH, li = D["half"], D["OH"], P["aperture"] / 2

    def want(n):
        return only is None or n in only

    def J(n, items, title, sub, **kw):
        out.append(bv.joint(items, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    stack = lambda: U(c["plate_1"], c["plate_2"], c["plate_3"])  # noqa: E731
    rails = lambda: U(*[c[f"rails_{s}"] for s in range(1, 5)])    # noqa: E731
    wicks = lambda: U(*[c[f"wick_{s}"] for s in range(1, 5)])     # noqa: E731
    if want(1):
        bx = (455, 545, 440, 545, -13, 56)
        J(1, [part("Side wall", win(c["wall_side_r"], *bx), COL["wall"]),
              part("Low wall comb", win(c["wall_low"], *bx), COL["wall"]),
              part("Low wall cap", win(c["wall_low_cap"], *bx), "#C9A36B"),
              part("Base ring", win(U(c["ring_side_r"], c["ring_low"]), *bx), COL["ring"]),
              part("Side liner", win(c["liner_side_r"], *bx), COL["liner"]),
              part("Stop block", win(c["stops"], *bx), COL["stop"])],
          "frame corner at the low end (right side)", "Seen from inside. Side wall overlaps the end wall; the base ring is under the side wall",
          elev=30, azim=-140, size=(8, 6))
    if want(2):
        bx = (-15, 15, 432, 545, -35, 66)
        J(2, [part("Glazing", win(U(c["glazing"]), *bx), COL["glazing"]),
              part("Glazing tape", win(c["tape"], *bx), COL["tape"]),
              part("Glazing trim", win(c["trim"], *bx), COL["trim"]),
              part("Side wall", win(c["wall_side_r"], *bx), COL["wall"]),
              part("Stone wool liner", win(c["liner_side_r"], *bx), COL["liner"]),
              part("Absorber plate", win(c["absorber"], *bx), COL["absorber"]),
              part("Side rails, stages 1 and 2 (150 C polymer)", win(U(c["rails_1"], c["rails_2"]), *bx), COL["rail12"]),
              part("Side rails, stages 3 and 4 (printed PC)", win(U(c["rails_3"], c["rails_4"]), *bx), COL["rail34"]),
              part("Condenser plates", win(stack(), *bx), COL["plate"]),
              part("Wick strips (10 mm dry break)", win(wicks(), *bx), COL["wick"]),
              part("Bottom plate", win(c["plate_bottom"], *bx), COL["bottom"]),
              part("Fin", win(c["fins"], *bx), COL["fin"]),
              part("Base ring ledge", win(c["ring_side_r"], *bx), COL["ring"])],
          "the stack at a side wall, cut across", "Cut across the slope. Plates rest on the rails; the bottom plate on the base ring ledge",
          elev=8, azim=-10, size=(9, 6.5))
    if want(3):
        bx = (440, 540, -495, -470, -13, 56)
        J(3, [part("Stop block", win(c["stops"], *bx), COL["stop"]),
              part("Side rails", win(rails(), *bx), COL["rail12"]),
              part("Absorber plate", win(c["absorber"], *bx), COL["absorber"]),
              part("Condenser plates", win(U(stack(), c["plate_bottom"]), *bx), COL["plate"]),
              part("Low wall comb", win(c["wall_low"], *bx), COL["wall"]),
              part("Low wall cap", win(U(c["wall_low_cap"], c["liner_low_cap"]), *bx), "#C9A36B"),
              part("Base ring", win(U(c["ring_low"], c["ring_side_l"]), *bx), COL["ring"])],
          "stop block at the low corner (left side)", "Cut along the rails, seen from the side. Plate corners and rail ends bear on the block; it bears on the low wall",
          elev=12, azim=-90, size=(8, 6))
    if want(4):
        y0 = 97.2
        bx = (470, 610, y0, y0 + 35, -60, 56)
        J(4, [part("Condenser plates and bottom plate", win(U(stack(), c["plate_bottom"]), *bx), COL["dtongue"]),
              part("Absorber plate", win(c["absorber"], *bx), COL["absorber"]),
              part("Low wall, liner and cap (beside the notch)", win(U(c["wall_low"], c["wall_low_cap"], c["liner_low"], c["liner_low_cap"]), *bx), COL["wall"]),
              part("Base ring", win(c["ring_low"], *bx), COL["ring"]),
              part("Manifold lid (slot)", win(c["lid"], *bx), COL["lid"]),
              part("Distillate manifold", win(c["manifold"], *bx), COL["manifold"]),
              part("Glazing and trim", win(U(c["glazing"], c["trim"]), *bx), COL["glazing"])],
          "distillate tongues into the manifold (cut on a rib line)", "Each condenser plate's tongue turns down through the lid slot; nested 4 mm apart",
          elev=12, azim=-90, size=(9, 6.5))
    if want(5):
        y0 = D["yb"][2]
        bx = (430, 690, y0, y0 + 35, -62, 56)
        J(5, [part("Brine tongues (absorber, plates 1 to 3)", win(U(c["absorber"], stack()), *bx), COL["btongue"]),
              part("Wick tails under the tongues", win(wicks(), *bx), COL["wick"]),
              part("Chevron dams", win(U(c["dams_1"], c["dams_2"], c["dams_3"]), *bx), COL["dam"]),
              part("Tongue clips (stainless)", win(U(*[c[f"clips_lo_{s_}"] for s_ in range(1, 5)]), *bx), COL["clip"]),
              part("Bottom plate", win(c["plate_bottom"], *bx), COL["bottom"]),
              part("Low wall, liner and cap (beside the notch)", win(U(c["wall_low"], c["wall_low_cap"], c["liner_low"], c["liner_low_cap"]), *bx), COL["wall"]),
              part("Manifold lid (closed here)", win(c["lid"], *bx), COL["lid"]),
              part("Distillate manifold", win(c["manifold"], *bx), COL["manifold"]),
              part("Brine gutter", win(c["gutter"], *bx), COL["gutter"]),
              part("Base ring", win(c["ring_low"], *bx), COL["ring"])],
          "brine tongues over the manifold into the brine gutter (cut at a strip centre)",
          "Wick tails ride under the brine tongues, 10.5 mm or more above the closed lid, and drop into the gutter",
          elev=12, azim=-90, size=(9, 6.5))
    if want(6):
        y0 = D["yb"][2]
        z1 = D["levels"][2]
        bx = (400, 545, y0 - 110, y0 + 110, z1 - 1, z1 + 4)
        pb, pd, pbt, _ = plate("cond", 2, P, split=True)
        J(6, [part("Condenser plate 2, top face", win(pb, *bx), COL["plate"]),
              part("Distillate tongues", win(pd, *bx), COL["dtongue"]),
              part("Brine tongue", win(pbt, *bx), COL["btongue"]),
              part("Chevron dam (silicone bead, 3 mm high)", win(c["dams_2"], *bx), COL["dam"]),
              part("Ribs lying on the plate", win(c["ribs_2"], *(400, 545, y0 - 110, y0 + 110, z1 + 0.4, z1 + 4)), COL["rib"]),
              part("Tongue clip (stainless)", win(c["clips_lo_3"], *(400, 545, y0 - 110, y0 + 110, z1 - 1.5, z1 + 4)), COL["clip"])],
          "brine tongue root and chevron dam, from above", "Low edge to the right. The dam turns condensate aside onto the zigzag edges, which lead it to the distillate tongues",
          elev=75, azim=-95, size=(8, 6))
    if want(7):
        y0 = 150.0
        bx = (-625, -470, y0, y0 + 30, -36, 66)
        J(7, [part("Wick tails, stages 1 to 4", win(wicks(), *bx), COL["wick"]),
              part("Plates (high ends)", win(U(stack(), c["absorber"], c["plate_bottom"]), *bx), COL["plate"]),
              part("High wall (opening)", win(c["wall_high"], *bx), COL["wall"]),
              part("Liner", win(c["liner_high"], *bx), COL["liner"]),
              part("Foam closure", win(c["closure"], *bx), COL["closure"]),
              part("Feed trough", win(c["trough"], *bx), COL["trough"]),
              part("Base ring", win(c["ring_high"], *bx), COL["ring"]),
              part("Glazing, tape and trim", win(U(c["glazing"], c["tape"], c["trim"]), *bx), COL["glazing"])],
          "feed end: wick tails out through the high wall into the trough", "Cut through a feed opening. The foam on the trough presses the tails against the wall",
          elev=12, azim=-90, size=(9, 6.5))
    if want(8):
        bx = (400, 545, 39.5, 80, -40, 15)
        J(8, [part("Bottom plate", win(c["plate_bottom"], *bx), "#9CA3AF"),
              part("Fin: flange bonded under the plate, web hanging down", win(c["fins"], *bx), "#374151"),
              part("Base ring ledge", win(c["ring_low"], *bx), COL["ring"]),
              part("Low wall sill and tooth", win(c["wall_low"], *bx), COL["wall"]),
              part("Stage 4 side of the gap: wick 4 and plate 3 above", win(U(c["plate_3"], c["wick_4"]), *bx), COL["plate"])],
          "fins and bottom plate on the base ring (low end)", "Cut beside a fin, seen from the side. The plate's edge rests on the ledge; the fin stops 15 mm short of it",
          elev=10, azim=-90, size=(8, 6))
    if want(9):
        y0 = P["bracket_y"]
        bx = (515, 690, y0, y0 + 25, -64, 56)
        J(9, [part("Outlet bracket", win(c["outlet_brackets"], *bx), COL["bracket"]),
              part("Distillate manifold and lid", win(U(c["manifold"], c["lid"]), *bx), COL["manifold"]),
              part("Brine gutter", win(c["gutter"], *bx), COL["gutter"]),
              part("Low wall tooth, sill and cap", win(U(c["wall_low"], c["wall_low_cap"], c["ring_low"]), *bx), COL["wall"])],
          "outlet bracket carrying the manifold and the brine gutter", "Cut at a bracket. Three screws into a tooth of the low wall; the gutter sits lower and further out",
          elev=12, azim=-90, size=(8, 6))
    S = stand(P, TILT)
    G = stand_geometry(P, TILT)
    Wc = lambda k: place(c[k], P, TILT)  # noqa: E731
    if want(10):
        px, pz = G["pivot"]
        bx = (px - 260, px + 90, 440, 640, -5, pz + 60)
        J(10, [part("Front post", win(S["posts"], *bx), COL["timber"]),
               part("Gusset (inside face)", win(S["gussets"], *bx), COL["gusset"]),
               part("Ground rail", win(S["ground_rails"], *bx), COL["timber"]),
               part("Front cross rail", win(S["cross_rails"], *bx), "#6B4423"),
               part("Side wall", win(Wc("wall_side_r"), *bx), COL["wall"]),
               part("Base ring", win(Wc("ring_side_r"), *bx), COL["ring"]),
               part("Pivot bolt M10", win(S["stand_bolts"], *bx), COL["bolt"])],
           "front pivot: post, gusset and ground rail (right side)", "Seen from inside the stand. The panel turns on the M10 pivot bolt through post and wall",
           elev=15, azim=-120, size=(8, 6.5))
    if want(11):
        hx, hz = G["hinge"]
        bx = (hx - 110, hx + 110, 500, 650, hz - 90, hz + 80)
        J(11, [part("Prop", win(S["props"], *bx), COL["prop"]),
               part("Prop block (glued and screwed to the wall)", win(S["prop_blocks"], *bx), COL["gusset"]),
               part("Side wall", win(Wc("wall_side_r"), *bx), COL["wall"]),
               part("Hinge bolt M10", win(S["stand_bolts"], *bx), COL["bolt"]),
               part("Glazing trim", win(Wc("trim"), *bx), COL["trim"])],
           "prop top on its block (right side)", "Seen from outside. The block spaces the prop out so its foot meets the outside of the ground rail",
           elev=15, azim=60, size=(8, 6))
    if want(12):
        fx, fz = G["foot"]
        xs = list(G["holes"].values())
        bx = (min(xs) - 60, max(xs) + 60, 520, 650, -2, 140)
        J(12, [part("Prop foot", win(S["props"], *bx), COL["prop"]),
               part("Ground rail with six tilt holes", win(S["ground_rails"], *bx), COL["timber"]),
               part("Prop pin M10 with wing nut", win(S["stand_bolts"], *bx), COL["bolt"])],
           "prop foot pinned to the ground rail (20 deg hole)", "One hole per tilt: 10, 15, 20, 25, 30 and 35 deg from front to back of this row",
           elev=15, azim=60, size=(8, 6))
    if want(13):
        r0 = 97.2
        bx = (-515, -470, r0 - 36, r0 + 36, -36, 33)
        J(13, [part("Plates with lip tabs (4 mm); absorber has none", win(U(c["plate_1"], c["plate_2"], c["plate_3"], c["absorber"], c["plate_bottom"]), *bx), "#9CA3AF"),
               part("Wick strips (centre strip and the next)", win(wicks(), *bx), COL["wick"]),
               part("High-end clips (stainless): bar under the wick, ears over the edge", win(U(*[c[f"clips_hi_{s_}"] for s_ in range(1, 5)]), *bx), COL["clip"]),
               part("Ribs (start 6 mm in)", win(U(*[c[f"ribs_{s_}"] for s_ in range(1, 5)]), *bx), COL["rib"]),
               part("Base ring with slot under the bottom plate's tab", win(c["ring_high"], *bx), COL["ring"])],
           "high edge: lip tab beside the wick clip ears (cut at a rib line)",
           "Seen from the high end. The lip hangs 4 mm from the plate edge at the rib line; each wick's clip ears sit in the dry break beside it",
           elev=14, azim=-130, size=(9, 6.5))
    if want(14):
        y0 = D["yb"][2]
        z1 = D["levels"][3]
        bx = (455, 520, y0 - 35, y0 + 35, z1 - 3, z1 + 4)
        J(14, [part("Brine tongue, plate 1", win(c["plate_1"], *bx), COL["btongue"]),
               part("Wick tail (30 mm wide) under the tongue", win(c["wick_2"], *bx), COL["wick"]),
               part("Tongue clip (stainless): base under the tail, flanges over the tongue", win(c["clips_lo_2"], *bx), COL["clip"]),
               part("Chevron dam", win(c["dams_1"], *bx), COL["dam"])],
           "brine tongue clip holding the wick tail", "From above and the side. The clip sits 7 to 15 mm past the tongue root line, clear of the dam",
           elev=35, azim=-60, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    c = C()
    out = []

    def want(n):
        return only is None or n in only

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(name, shape, color, e):
        return Part(name, shape, color, None, tuple(e), 1.0)

    def g(name, shape):
        return Part(name, shape, bv.GHOST, None, (0, 0, 0), 1.0)
    walls_side = U(c["wall_side_r"], c["wall_side_l"])
    ends = U(c["wall_high"], c["wall_low"])
    ring = U(c["ring_side_r"], c["ring_side_l"], c["ring_high"], c["ring_low"])
    liner = U(c["liner_side_r"], c["liner_side_l"], c["liner_high"], c["liner_low"])
    S = stand(P, TILT)
    blocks_local = U(*[M._box(P["prop_hinge"][0] - 60, P["prop_hinge"][0] + 60, *sorted((sg * D["OH"], sg * (D["OH"] + P["post"]))),
                               D["FZ0"], D["FZ0"] + P["post"]) for sg in (-1, 1)])
    st(1, [g("Side walls", walls_side)], [mv("High wall", c["wall_high"], COL["wall"], (-200, 0, 0)),
                                          mv("Low wall comb", c["wall_low"], COL["wall"], (200, 0, 0))],
       "end walls between the side walls", "Glue and three 4 x 40 mm screws per corner through the side wall; check the diagonals",
       elev=35, azim=-60, label_done=True)
    box = [g("Walls", U(walls_side, ends))]
    st(2, box, [mv("Base ring (4 strips)", ring, COL["ring"], (0, 0, -150))], "base ring under the walls",
       "Turn the frame over. Glue and screw up into the wall edges every 150 mm; the low strip sits inside the comb's sill",
       elev=-30, azim=-60, label_done=False)
    box = box + [g("Base ring", ring)]
    st(3, box, [mv("Stone wool liner (foil inward)", liner, bv.NEW, (0, 0, 160))], "liner into the frame",
       "High-temperature silicone on the back of each piece; pockets behind the pivot and hinge holes",
       elev=40, azim=-60, label_done=False)
    box = box + [g("Liner", liner)]
    st(4, box + [g("Prop blocks", blocks_local)], [mv("Stop blocks (2)", c["stops"], COL["stop"], (0, 0, 120))], "stop blocks into the low corners",
       "High-temperature silicone on the back and side faces. Prop blocks already glued and screwed on the side walls",
       elev=45, azim=-150, label_done=False)
    box = box + [g("Stop blocks", c["stops"]), g("Prop blocks", blocks_local)]
    bottom_s = straight_plate(0)
    st(5, box, [mv("Bottom plate with fins (tongues straight)", U(bottom_s, c["fins"]), COL["bottom"], (0, 0, 220))],
       "bottom plate and fins onto the base ring", "Lower it level; the six tongues drop into the comb's notches and rest on the sill",
       elev=40, azim=-60, label_done=False)
    done = box + [g("Bottom plate", bottom_s), g("Fins", c["fins"])]
    names = {1: "plate 1", 2: "plate 2", 3: "plate 3"}
    n = 6
    for stage in (4, 3, 2, 1):
        lvl = 5 - stage                           # plate above this gap
        rail_col = COL["rail34"] if stage >= 3 else COL["rail12"]
        new = [mv(f"Stage {stage} side rails", c[f"rails_{stage}"], rail_col, (0, 0, 120)),
               mv(f"Stage {stage} ribs", c[f"ribs_{stage}"], COL["rib"], (0, 0, 160))]
        ptitle = "absorber" if lvl == 4 else names[4 - lvl]
        psh = U(straight_plate(lvl), straight_wick(stage))
        new.append(mv(f"{ptitle.capitalize()} with wick {stage} under it", psh, COL["absorber"] if lvl == 4 else "#475569", (0, 0, 480)))
        new.append(mv(f"Wick {stage} clips (10, stainless)", clips_of(stage), COL["clip"], (0, 0, 560)))
        psh = U(psh, clips_of(stage))
        sub = "Clip the wick strips under the plate on the bench first; rails and ribs, then the plate: tongues down into the notches, tails out through the high wall"
        st(n, done, new, f"stage {stage}: rails, ribs and {ptitle}", sub, elev=40, azim=-60, label_done=False)
        done = done + [g(f"rails {stage}", c[f"rails_{stage}"]), g(f"ribs {stage}", c[f"ribs_{stage}"]), g("plate", psh)]
        if lvl < 4:
            done.append(g("dams", c[f"dams_{4 - lvl}"]))
        n += 1
    # n == 10. From here the plates are kept apart as bodies and tongues, so the tongue bends can be shown.
    others = [q for q in done if q.name != "plate"]
    bodies = [plate("bottom" if l == 0 else ("absorber" if l == 4 else "cond"), l, P, bent=False, split=True) for l in range(5)]
    wick_bodies = [wick(s_, P, bent=False, split=True) for s_ in range(1, 5)]
    plate_bodies = U(*[b_[0] for b_ in bodies], *[w[0] for w in wick_bodies], *[clips_of(s_) for s_ in range(1, 5)])
    d_straight = U(*[b_[1] for b_ in bodies])
    b_straight = U(*[b_[2] for b_ in bodies], *[w[1] for w in wick_bodies])
    others = [g("plate bodies", plate_bodies)] + [q for q in others if q.name != "plate bodies"]
    straight = [g("straight tongues", U(d_straight, b_straight))]
    cap = U(c["wall_low_cap"], c["liner_low_cap"])
    st(10, others + straight, [mv("Low wall cap with its liner", cap, COL["wall"], (0, 0, 120))], "low wall cap",
       "Sits on the comb's teeth over the tongues; two 4 x 30 mm screws into the side walls' end grain",
       elev=35, azim=-60, label_done=False)
    others = others + [g("cap", cap)]
    st(11, others + straight, [mv("Glazing tape", c["tape"], COL["tape"], (0, 0, 80)), mv("Twin-wall glazing", c["glazing"], COL["glazing"], (0, 0, 220))],
       "glazing tape and glazing", "Tape on the wall tops; flutes running down the slope; ends sealed with breather tape; 7 mm clear of the outside all round",
       elev=35, azim=-60, label_done=False)
    others = others + [g("glazing", U(c["tape"], c["glazing"]))]
    st(12, others + straight, [mv("Glazing trim (4, mitred)", c["trim"], COL["trim"], (0, 0, 150))], "glazing trim",
       "Silicone bead under the top leg; 4 x 20 mm stainless screws every 200 mm into the walls",
       elev=35, azim=-60, label_done=False)
    others = others + [g("trim", c["trim"])]
    st(13, others + straight, [mv("Outlet brackets (2)", c["outlet_brackets"], COL["bracket"], (150, 0, 0))], "outlet brackets onto the low wall",
       "Three 4 x 25 mm stainless screws each, into a tooth of the comb and its sill, square to the wall",
       elev=20, azim=-30, label_done=False)
    others = others + [g("brackets", c["outlet_brackets"])]
    st(14, others + straight, [mv("Distillate manifold with its slotted lid", U(c["manifold"], c["lid"]), COL["manifold"], (170, 0, 0))],
       "distillate manifold and lid", "Lid snapped on first; slide the manifold in under the straight tongues onto the brackets, outlet at the right",
       elev=25, azim=-30, label_done=False)
    others = others + [g("manifold", U(c["manifold"], c["lid"]))]
    dt_bent = U(*[plate("bottom" if l == 0 else "cond", l, P, split=True)[1] for l in range(0, 4)])
    st(15, others + [g("brine tongues", b_straight)], [mv("Distillate tongues, bent down", dt_bent, COL["dtongue"], (0, 0, 40))],
       "bend the distillate tongues into the lid slots",
       "Bend each over a hardwood block at its bend mark, lowest plate first, so it drops 3 mm into the channel",
       elev=25, azim=-30, label_done=False)
    others = others + [g("tongues", dt_bent)]
    st(16, others + [g("brine tongues", b_straight)], [mv("Brine gutter", c["gutter"], COL["gutter"], (150, 0, -60))], "brine gutter onto the bracket ends",
       "Outboard of and lower than the manifold; drain at the left end, away from the distillate outlet",
       elev=25, azim=-30, label_done=False)
    others = others + [g("gutter", c["gutter"])]
    bt_bent = U(*[plate("absorber" if l == 4 else "cond", l, P, split=True)[2] for l in range(1, 5)],
                *[wick(s_, P, split=True)[1] for s_ in range(1, 5)])
    st(17, others, [mv("Brine tongues and wick tails, bent down", bt_bent, COL["btongue"], (0, 0, 40))], "bend the brine tongues into the gutter",
       "Lowest first, each 4 mm outside the one below; the wick tail stays under its tongue and ends in the gutter",
       elev=25, azim=-30, label_done=False)
    done = others + [g("brine", bt_bent)]
    st(18, done, [mv("Trough brackets (2)", c["trough_brackets"], COL["bracket"], (-120, 0, 0)),
                  mv("Feed trough with foam closure", U(c["trough"], c["closure"]), COL["trough"], (-200, 0, 60))],
       "feed trough and foam closure", "Brackets screwed to the high wall's solid ends; foam glued to the trough; tails led over the rim into it",
       elev=30, azim=-130, label_done=False)
    panel_local = U(*[s.shape for s in done], c["trough"], c["trough_brackets"], c["closure"])
    # stand, in the world
    st(19, [], [mv("Ground rails (2)", S["ground_rails"], COL["timber"], (0, 0, 0)), mv("Cross rails (2)", S["cross_rails"], "#6B4423", (0, 0, 150))],
       "ground frame", "Cross rails between the ground rails with four corner brackets; level it; stakes or ballast",
       elev=30, azim=-60, label_done=False)
    st(20, [g("Ground frame", U(S["ground_rails"], S["cross_rails"]))],
       [mv("Front posts with gussets", U(S["posts"], S["gussets"]), COL["timber"], (0, 0, 200))], "front posts and gussets",
       "Post on top of the rail at its mark; gusset glued and screwed to the inside faces behind the post",
       elev=25, azim=-120, label_done=False)
    frame_g = [g("Stand", U(S["ground_rails"], S["cross_rails"], S["posts"], S["gussets"]))]
    st(21, frame_g, [mv("Panel (two people)", place(panel_local, P, TILT), bv.NEW, (0, 0, 300))], "panel onto the front posts",
       "Two people, panel dry. M10 pivot bolt through each post and side wall, nut inside; support the high end on a trestle",
       elev=25, azim=-60, label_done=False)
    pl_ = S["props"] & M._box(-3000, 3000, -3000, 0, -100, 3000)
    pr_ = S["props"] & M._box(-3000, 3000, 0, 3000, -100, 3000)
    st(22, frame_g + [g("Panel", place(panel_local, P, TILT)), g("Prop blocks", S["prop_blocks"])],
       [mv("Prop, near side", pl_, COL["prop"], (0, -220, 0)), mv("Prop, far side", pr_, COL["prop"], (0, 220, 0))],
       "props from the prop blocks to the tilt holes", "Hinge bolt through prop, block and wall; foot pin with wing nut through the chosen rail hole (20 deg shown)",
       elev=20, azim=-70, label_done=False)
    return out


# ----------------------------------------------------------------- layout drawings (matplotlib)
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Polygon as MPoly
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    res = []
    OUT.mkdir(parents=True, exist_ok=True)
    # --- low edge of a condenser plate, seen from above, low edge at the bottom of the page
    pts = edge_points(P)
    fig = plt.figure(figsize=(13, 5.0), dpi=150)
    ax = fig.add_axes([0.03, 0.10, 0.94, 0.70]); ax.set_aspect("equal"); ax.set_axis_off()
    L = tongue_lengths(2)
    body = [(y, -(x - 498)) for y, x in pts]           # down the page = down the slope
    poly = [(-498, 60)] + body + [(498, 60)]
    ax.add_patch(MPoly(poly, closed=True, fc="#E5E7EB", ec=INK, lw=1.0))
    for y in D["yd"]:
        ax.add_patch(Rectangle((y - 15, -L["d_len"]), 30, L["d_len"], fc="#BAE6FD", ec="#0369A1", lw=0.8))
    for y in D["yb"]:
        ax.add_patch(Rectangle((y - 25, -L["b_len"] + 25), 50, L["b_len"], fc="#FED7AA", ec="#C2410C", lw=0.8, zorder=2))
        ax.add_patch(Rectangle((y - 15, -L["b_len"] + 26), 30, L["b_len"] + 9, fc="none", ec="#92400E", lw=0.8, ls="--", zorder=3))
        ax.plot([y, y - 26], [41, 26], color="#DB2777", lw=2.2, zorder=4); ax.plot([y, y + 26], [41, 26], color="#DB2777", lw=2.2, zorder=4)
    for y in M.rib_positions(P):
        ax.add_patch(Rectangle((y - 3.5, 8), 7, 52, fc="#FCA5A5", ec="#B91C1C", lw=0.6))
    for y in D["yb"]:      # tongue clips, 7 to 15 mm past the root line
        ax.add_patch(Rectangle((y - 25.4, 25 - P["clip_lo_x"][1]), 50.8, 8, fc="#86EFAC", ec="#166534", lw=0.8, zorder=5))
    for sg in (-1, 1):
        ax.add_patch(Rectangle((sg * 492 - 6, 0), 12, 60, fc="#D4A373", ec="#92400E", lw=0.6))
    ax.plot([-520, 520], [0, 0], color=MUT, lw=0.5, ls=(0, (6, 3)))
    ax.text(-528, 0, "tip line", ha="right", va="center", fontsize=8, color=MUT)
    ax.plot([-520, 520], [25, 25], color=MUT, lw=0.5, ls=(0, (2, 3)))
    ax.text(-528, 25, "root line, 25 up", ha="right", va="center", fontsize=8, color=MUT)
    for y in D["yd"]:
        ax.text(y, -L["d_len"] - 6, f"{y:+.1f}", ha="center", va="top", fontsize=7.5, color="#0369A1")
    for y in D["yb"]:
        ax.text(y, -L["b_len"] + 18, f"{y:+.1f}", ha="center", va="top", fontsize=7.5, color="#C2410C")
    ax.set_xlim(-600, 540); ax.set_ylim(-L["b_len"] - 20, 75)
    fig.text(0.03, 0.97, "Plates: the low edge and its tongues (plate 2 shown, tongues straight)", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.915, "Seen from above, low edge at the bottom. Positions across the plate in mm from the centre line. Blue: distillate tongues 30 wide at the rib lines and corners.\n"
             "Orange: brine tongues 50 wide at the strip centres; dashed: the 30 mm wick tail under each. Pink: silicone chevron dams. Green: tongue clips. Red: ribs. Tan: side rails.",
             fontsize=8.2, color=MUT, va="top")
    fig.text(0.03, 0.045, "Zigzag edges fall 25 mm from each tip to the next root, so condensate runs along them to the distillate tongues. "
             "Bottom plate: distillate tongues only. Absorber: brine tongues only.", fontsize=8.2, color=INK)
    fig.text(0.03, 0.01, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.01, "github.com/BoujeeEnjinia1701/stillstack", fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "low-edge.png", facecolor="white"); plt.close(fig); res.append(OUT / "low-edge.png")

    # --- wall openings, seen from outside, both end walls
    fig = plt.figure(figsize=(13, 5.6), dpi=150)
    for row, (title, items) in enumerate((
            ("High wall (feed end), seen from outside: five feed openings", [(a - 5, b + 5, "feed") for a, b in D["strips"]]),
            ("Low wall comb (outlet end), seen from outside: eleven notches", [(y - 20, y + 20, "d") for y in D["yd"]] + [(y - 30, y + 30, "b") for y in D["yb"]]))):
        ax = fig.add_axes([0.04, 0.47 - row * 0.42, 0.92, 0.36]); ax.set_aspect("equal"); ax.set_axis_off()
        z0 = -12 if row else 0
        ax.add_patch(Rectangle((-525, z0), 1050, D["wall_top"] - z0 if not row else D["open_top"] - z0, fc="#F5E6C8", ec=INK, lw=1.0))
        if row:
            ax.add_patch(Rectangle((-525, D["open_top"]), 1050, D["wall_top"] - D["open_top"], fc="#EADBC0", ec=INK, lw=0.8, ls="--"))
            ax.text(0, (D["open_top"] + D["wall_top"]) / 2, "cap (separate strip)", ha="center", va="center", fontsize=7.5, color=MUT)
            ax.plot([-525, 525], [0, 0], color=MUT, lw=0.5, ls=":")
            ax.text(530, -6, "sill 12", ha="left", va="center", fontsize=7.5, color=MUT)
        for a, b, kind in sorted(items):
            col = {"feed": "#FDE68A", "d": "#BAE6FD", "b": "#FED7AA"}[kind]
            ax.add_patch(Rectangle((a, 0), b - a, D["open_top"], fc=col, ec=INK, lw=0.8))
            ax.text((a + b) / 2, D["wall_top"] + 3, f"{abs((a + b) / 2):.1f}\n{b - a:.0f} wide", ha="center", va="bottom",
                    fontsize=6.8, color=INK, linespacing=1.1)
        ax.text(-540, D["open_top"] / 2, f"{D['open_top']:.0f}", ha="right", va="center", fontsize=8, color=AC)
        ax.set_xlim(-560, 560); ax.set_ylim(z0 - 8, D["wall_top"] + (30 if not row else 45))
        fig.text(0.04, 0.88 - row * 0.42, title, fontsize=10.5, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.98, "End walls: opening positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.94, "Centres in mm from the centre line (the layout is the same each side), widths in mm. Openings 33 mm tall. Cut the liner pieces to match.",
             fontsize=8.2, color=MUT, va="top")
    fig.text(0.04, 0.012, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.96, 0.012, "github.com/BoujeeEnjinia1701/stillstack", fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "wall-openings.png", facecolor="white"); plt.close(fig); res.append(OUT / "wall-openings.png")
    return res


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps"]
    for a in args:
        if ":" in a:
            kind, nums = a.split(":")
            only = {int(x) for x in nums.split(",")}
            r = {"sheet": sheets, "joint": joints, "step": steps}[kind](only)
        else:
            r = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "layouts": layouts}[a]()
        print(a, "->", r)
