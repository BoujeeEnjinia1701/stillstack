"""StillStack drawing sheets.

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/SSK-DWG-002 (general arrangement, Rev P1) as SVG, PDF and PNG
from the parametric model in cad/src/model.py. Never edit the sheet by hand.
(SSK-DWG-001 is the concept blueprint in media/.)
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Compound  # noqa: E402
from drawing import Sheet, project_views, _viewbox, _t, INK, MUTED  # noqa: E402
import model  # noqa: E402

DATE = "2026-09-25"
OUT = ROOT / "cad" / "drawings"
WORK = OUT / "_views"


def dim(s, x1, y1, x2, y2, text, off=6.0, vertical=False):
    """Simple dimension line with ticks and a centered value, in sheet mm."""
    g = []
    if vertical:
        xd = x1 - off
        g += [f'<line x1="{x1 - 1}" y1="{y1}" x2="{xd - 1.5}" y2="{y1}" stroke="{MUTED}" stroke-width="0.18"/>',
              f'<line x1="{x2 - 1}" y1="{y2}" x2="{xd - 1.5}" y2="{y2}" stroke="{MUTED}" stroke-width="0.18"/>',
              f'<line x1="{xd}" y1="{y1}" x2="{xd}" y2="{y2}" stroke="{INK}" stroke-width="0.25"/>',
              f'<line x1="{xd - 1}" y1="{y1 + 1}" x2="{xd + 1}" y2="{y1 - 1}" stroke="{INK}" stroke-width="0.35"/>',
              f'<line x1="{xd - 1}" y1="{y2 + 1}" x2="{xd + 1}" y2="{y2 - 1}" stroke="{INK}" stroke-width="0.35"/>']
        ym = (y1 + y2) / 2
        g.append(f'<g transform="rotate(-90 {xd - 1.2} {ym})">' + _t(xd - 1.2, ym, text, 2.4, 500, INK, "middle") + "</g>")
    else:
        yd = y1 + off
        g += [f'<line x1="{x1}" y1="{y1 + 1}" x2="{x1}" y2="{yd + 1.5}" stroke="{MUTED}" stroke-width="0.18"/>',
              f'<line x1="{x2}" y1="{y2 + 1}" x2="{x2}" y2="{yd + 1.5}" stroke="{MUTED}" stroke-width="0.18"/>',
              f'<line x1="{x1}" y1="{yd}" x2="{x2}" y2="{yd}" stroke="{INK}" stroke-width="0.25"/>',
              f'<line x1="{x1 - 1}" y1="{yd + 1}" x2="{x1 + 1}" y2="{yd - 1}" stroke="{INK}" stroke-width="0.35"/>',
              f'<line x1="{x2 - 1}" y1="{yd + 1}" x2="{x2 + 1}" y2="{yd - 1}" stroke="{INK}" stroke-width="0.35"/>']
        g.append(_t((x1 + x2) / 2, yd - 1.2, text, 2.4, 500, INK, "middle"))
    s._layers.extend(g)


def place(s, svg, x, y, k, label, sub):
    vw, vh = _viewbox(Path(svg).read_text())[2:]
    s.add_svg(svg, x, y, vw * k, vh * k, scale=k, label=label, sublabel=sub)
    return x, y, vw * k, vh * k


def main():
    p = model.PARAMS
    parts = model.build()
    asm = Compound(children=list(parts.values()))
    bb = asm.bounding_box()
    views = project_views(asm, WORK / "ga")
    detail = model.stack_detail(y=(80.0, 125.0))
    det = project_views(detail, WORK / "detail")

    s = Sheet(project="StillStack", title="General arrangement", dwg_no="SSK-DWG-002", rev="P1",
              author="Amish Chadha", date=DATE, scale=1 / 20,
              material="See bom/bom.csv. Plates 0.5 mm aluminum; rails PC; ribs silicone; frame plywood and PIR",
              concept=False, revisions=[("P1", "Preliminary general arrangement (TRL 3)", DATE, "AC")])
    s._layers.append(_t(16, 19, "PRELIMINARY, NOT FOR FABRICATION", 3.2, 600, "#B45309"))

    k = 1 / 20
    tx, ty, tw, th = place(s, views["top"], 26, 38, k, "Top view", "Scale 1:20")
    fx, fy, fw, fh = place(s, views["front"], 26, ty + th + 22, k, "Front view (side elevation)", "Scale 1:20")
    rx, ry, rw, rh = place(s, views["right"], fx + fw + 16, fy, k, "Right view (from low edge)", "Scale 1:20")
    dim(s, tx, ty, tx + tw, ty, f"{bb.size.X:.0f}", off=-5)
    dim(s, fx, fy, fx, fy + fh, f"{bb.size.Z:.0f}", off=4, vertical=True)
    dim(s, tx, ty, tx, ty + th, f"{bb.size.Y:.0f}", off=4, vertical=True)

    dx, dy, dw, dh = place(s, det["right"], 180, 40, 2.0, "Detail A: stack section at a rib",
                           "Scale 2:1, looking up the slope")
    dbb = detail.bounding_box()
    zmin, zmax = dbb.min.Z, dbb.max.Z
    z_levels = [("Absorber plate 0.5", 30.25), ("Wick 1 (stage 1)", 29.5), ("Vapor gap 6", 26.0),
                ("Condenser plate 0.5", 22.75), ("Silicone rib 7 dia", 19.0), ("Wick 4 (stage 4)", 6.9),
                ("Bottom plate 0.5", 0.25)]
    last = -1e9
    for name, zl in z_levels:
        yy = dy + (zmax - zl) / (zmax - zmin) * dh
        ty_ = max(yy, last + 3.6)
        last = ty_
        s._layers.append(f'<polyline points="{dx + dw + 1},{yy:.2f} {dx + dw + 4},{yy:.2f} {dx + dw + 6},{ty_:.2f}" '
                         f'fill="none" stroke="{MUTED}" stroke-width="0.18"/>')
        s._layers.append(_t(dx + dw + 7, ty_ + 0.9, name, 2.2, 400, INK))

    edge = model.stack_detail(x=(440.0, 690.0), y=(0.0, 20.0), z=(-90.0, 80.0),
                              keep=model.STACK + ["Insulated frame", "Glazing", "Distillate manifold", "Brine gutter"])
    ev = project_views(edge, WORK / "edge")
    bx, by, bw, bh = place(s, ev["front"], 40, 178, 0.5, "Detail B: low edge, distillate and brine",
                           "Scale 1:2, untilted; wick tails not shown")
    ebb = edge.bounding_box()
    outer = p["aperture"] / 2 + p["ply_t"] + p["foam_t"]
    def at(xm, zm):
        return bx + (xm - ebb.min.X) * 0.5, by + (ebb.max.Z - zm) * 0.5
    for text, (xm, zm), (lx, ly) in [
            ("Glazing", (470, 58), (-2, -8)), ("Condenser lips into manifold", (outer + 10, 8), (-30, 20)),
            ("Frame wall", (outer - 18, 60), (8, -12)), ("Distillate manifold, lidded", (outer + 40, 38), (10, -8)),
            ("Brine gutter (outboard, lower)", (outer + 130, -45), (22, 4))]:
        x0, y0 = at(xm, zm)
        s._layers.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x0 + lx:.2f}" y2="{y0 + ly:.2f}" '
                         f'stroke="{MUTED}" stroke-width="0.18"/>')
        s._layers.append(_t(x0 + lx, y0 + ly + (-0.8 if ly < 0 else 3.0), text, 2.2, 400, INK, "middle"))

    s.add_svg(views["iso"], 290, 34, 124, 92, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Key dimensions and figures (SSK-CAL-001)", [
        f"Aperture 1.0 x 1.0 m; tilt {p['tilt']:.0f} deg, stand 10 to 35 deg",
        f"{p['n_stages']} stages; {p['gap']:.0f} mm vapor gap; {p['wick_t']:.0f} mm wicks; 0.5 mm plates",
        f"Ribs: {p['n_ribs']} per gap at 194 mm pitch; sag 0.5 mm",
        f"Dry breaks {p['wick_break']:.0f} mm each side of ribs and rails",
        "Air gap 25 mm; 6 mm twin-wall PC glazing",
        f"Frame {p['ply_t']:.0f} mm plywood + {p['foam_t']:.0f} mm PIR; 1,074 mm square outside",
        "Front pivot 350 mm; rear strut 530 to 940 mm",
        "Design day: about 10.6 L/day, GOR about 1.3",
        "Dry stagnation: stage 1 about 140 C",
        "Panel about 16 kg dry, 20 kg wet",
        "Wick tails (0.25 m) and fasteners not shown",
    ], x=290, y=144, width=128)
    OUT.mkdir(parents=True, exist_ok=True)
    s.save(OUT / "SSK-DWG-002")
    shutil.rmtree(WORK, ignore_errors=True)
    print("Wrote cad/drawings/SSK-DWG-002.svg, .pdf and .png")


if __name__ == "__main__":
    main()
