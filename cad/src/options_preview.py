"""StillStack concept options picture, provisional shaded version (kit 1.9).

Run from the repo root:  python cad/src/options_preview.py
Writes media/options.png from the D3 models of every option in cad/src/model.py (components(option)), shaded with
the kit's matplotlib renderer (.kit/concept.py), each panel with the same 1.75 m figure for scale. Fasteners are left
out of this preview for speed. It is a stand-in until the coordinator renders the Cycles picture with
`python .kit/options.py` on Amish's Mac (STANDARDS section 24); `render.py --check` needs media/options.png to exist.
CONCEPT OPTIONS, NOT FOR FABRICATION.
"""
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad/src"), str(ROOT / ".kit")]

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402
import concept  # noqa: E402
import model  # noqa: E402

INK, MUTED, ACCENT, WARN = "#111827", "#4B5563", "#0F766E", "#B45309"


def panel(key, path):
    parts = [concept.Part(p["name"], p["shape"], p["color"]) for p in model.components(key) if p["kind"] != "fastener"]
    from build123d import Compound
    bb = Compound(children=[q.shape for q in parts]).bounding_box()
    parts = parts + [concept.human_figure(1750.0, x=bb.min.X - 700.0, y=bb.center().Y, z=0.0)]   # on the ground, by the high edge
    v = model.OPTION_VIEWS.get(key, {})
    concept._render(parts, path, elev=v.get("el", 24), azim=v.get("az", -50), size=(5, 5), dpi=160)
    return Image.open(path).convert("RGB")


def main():
    keys = list(model.OPTIONS)
    with tempfile.TemporaryDirectory() as tmp:
        imgs = [panel(k, Path(tmp) / f"opt-{k}.png") for k in keys]
    n = len(keys)
    fig = plt.figure(figsize=(5.2 * n, 6.6), dpi=160)
    fig.text(0.015, 0.975, f"{model.TITLE}: concept options", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.015, 0.935, "CONCEPT OPTIONS, NOT FOR FABRICATION. Same scale reference in every panel. Provisional shaded "
             "preview of the D3 models (fasteners not drawn); Cycles render to follow.", fontsize=8, color=WARN, va="top")
    fig.text(0.985, 0.975, "github.com/" + "BoujeeEnjinia1701/stillstack", fontsize=8, color=ACCENT, va="top", ha="right",
             family="monospace")
    for i, (k, im) in enumerate(zip(keys, imgs)):
        ax = fig.add_axes([i / n + 0.01, 0.2, 1 / n - 0.02, 0.68])
        ax.imshow(im)
        ax.axis("off")
        fig.text(i / n + 0.02, 0.17, f"Option {k}: {model.OPTIONS[k]}", fontsize=11, fontweight="bold", color=INK, va="top")
        fig.text(i / n + 0.02, 0.12, textwrap.fill(model.PRINCIPLES.get(k, ""), 60), fontsize=8, color=MUTED, va="top")
        if k == model.CHOSEN:
            fig.text((i + 1) / n - 0.02, 0.17, "CURRENT DESIGN", fontsize=8, fontweight="bold", color=ACCENT, va="top", ha="right")
    out = ROOT / "media/options.png"
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
