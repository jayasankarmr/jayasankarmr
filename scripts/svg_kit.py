"""Small SVG helpers shared by the asset builders.

Coordinates are display pixels (the README shows everything at 830 wide); `svg()` sets
width/height at 2x so rasterisers and hi-dpi screens get full resolution.
"""
import base64
from html import escape

from tokens import MIN_FONT, MONO, SANS, SCALE

FAMILIES = {"mono": MONO, "sans": SANS}

# Helvetica advance widths (/1000 em) for rough sans layout. System UI fonts are close
# enough for deciding where things go; nothing depends on an exact fit.
_HELV = dict(zip(
    " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,-|·&()/:%'",
    [278, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556,
     556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 667, 667, 722, 722, 667, 611, 778,
     722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667,
     667, 611] + [556] * 10 + [278, 278, 333, 260, 278, 667, 333, 333, 278, 278, 889, 191],
))


def esc(s):
    return escape(str(s), quote=True)


def fmt(v):
    """Compact number formatting for attributes."""
    if isinstance(v, float):
        v = round(v, 2)
        return str(int(v)) if v == int(v) else str(v)
    return str(v)


def text_width(s, size, family="sans", weight=400, ls=0):
    if family == "mono":
        w = len(s) * 0.6 * size
    else:
        w = sum(_HELV.get(c, 556) for c in s) / 1000 * size
        if weight >= 600:
            w *= 1.07
    return w + ls * len(s)


def attrs(**kw):
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        out.append(f'{k.rstrip("_").replace("_", "-")}="{esc(fmt(v))}"')
    return " ".join(out)


def text(x, y, s, *, size, fill, family="sans", weight=None, anchor=None, ls=None,
         opacity=None, raw=False):
    """A <text> element. `ls` is letter-spacing in em. `raw=True` passes `s` through
    unescaped so callers can include <tspan>s built with `tspan()`."""
    if size < MIN_FONT:
        raise ValueError(f"font-size {size} below {MIN_FONT}px minimum: {s!r}")
    a = attrs(
        x=x, y=y, font_family=FAMILIES[family], font_size=size, font_weight=weight,
        text_anchor=anchor, letter_spacing=(f"{fmt(ls * size)}" if ls else None),
        fill=fill, opacity=opacity,
    )
    return f"<text {a}>{s if raw else esc(s)}</text>"


def tspan(s, **kw):
    if "family" in kw:
        kw["font_family"] = FAMILIES[kw.pop("family")]
    if "weight" in kw:
        kw["font_weight"] = kw.pop("weight")
    return f"<tspan {attrs(**kw)}>{esc(s)}</tspan>"


def rect(x, y, w, h, *, fill="none", stroke=None, sw=None, rx=None, dash=None, opacity=None):
    return f"<rect {attrs(x=x, y=y, width=w, height=h, rx=rx, fill=fill, stroke=stroke, stroke_width=sw, stroke_dasharray=dash, opacity=opacity)}/>"


def line(x1, y1, x2, y2, *, stroke, sw=1, dash=None, marker=None):
    m = f"url(#{marker})" if marker else None
    return f"<line {attrs(x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, stroke_width=sw, stroke_dasharray=dash, marker_end=m)}/>"


def path(d, *, stroke, sw=1, fill="none", dash=None, marker=None, cap=None):
    m = f"url(#{marker})" if marker else None
    return f"<path {attrs(d=d, fill=fill, stroke=stroke, stroke_width=sw, stroke_dasharray=dash, stroke_linecap=cap, marker_end=m)}/>"


def circle(cx, cy, r, *, fill):
    return f"<circle {attrs(cx=cx, cy=cy, r=r, fill=fill)}/>"


def arrow_marker(mid, color):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" '
            f'fill="{color}"/></marker>')


def brackets(x, y, w, h, length, *, stroke, sw=1.5):
    """Four corner crop marks. The stroke sits inside the (x, y, w, h) box."""
    o = sw / 2
    x0, y0, x1, y1 = x + o, y + o, x + w - o, y + h - o
    L = length
    d = (f"M{fmt(x0)} {fmt(y0 + L)}V{fmt(y0)}H{fmt(x0 + L)}"
         f"M{fmt(x1 - L)} {fmt(y0)}H{fmt(x1)}V{fmt(y0 + L)}"
         f"M{fmt(x1)} {fmt(y1 - L)}V{fmt(y1)}H{fmt(x1 - L)}"
         f"M{fmt(x0 + L)} {fmt(y1)}H{fmt(x0)}V{fmt(y1 - L)}")
    return path(d, stroke=stroke, sw=sw, cap="square")


def wrap(s, width, size, family="sans", weight=400):
    """Greedy word wrap to `width` display px using the same estimate as `text_width`."""
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and text_width(trial, size, family, weight) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur] if cur else lines


def image(x, y, w, h, src, *, clip=None, opacity=None):
    """A JPEG embedded as a data URI (SVGs in <img> cannot load external files), cropped
    to fill the box like CSS `object-fit: cover`."""
    data = base64.b64encode(src.read_bytes()).decode()
    c = f"url(#{clip})" if clip else None
    a = attrs(x=x, y=y, width=w, height=h, preserveAspectRatio="xMidYMid slice",
              clip_path=c, opacity=opacity)
    return f'<image {a} href="data:image/jpeg;base64,{data}"/>'


def linear_gradient(gid, stops, *, x2=1, y2=0):
    """Horizontal by default. `stops` is a list of (offset, colour, opacity)."""
    st = "".join(f'<stop offset="{fmt(o)}" stop-color="{c}" stop-opacity="{fmt(a)}"/>'
                 for o, c, a in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{fmt(x2)}" y2="{fmt(y2)}">{st}</linearGradient>'


def svg(w, h, body, label, defs=""):
    """Root element. `label` becomes both <title> and aria-label."""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(w)} {fmt(h)}" '
        f'width="{fmt(w * SCALE)}" height="{fmt(h * SCALE)}" role="img" aria-label="{esc(label)}">',
        f"<title>{esc(label)}</title>",
    ]
    if defs:
        parts.append(f"<defs>{defs}</defs>")
    parts += body if isinstance(body, list) else [body]
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def header(n, title, where, t, width=830, height=32):
    """Section header: `NN  TITLE ———— ./path`, one template for every section."""
    y = 21
    num = f"{n:02d}"
    size_num, size_title, size_path = 14, 14, 12
    x_title = 8 + text_width(num, size_num, "mono", ls=0.1 * size_num) + 14
    title_w = text_width(title.upper(), size_title, "mono", ls=0.16 * size_title)
    path_w = text_width(where, size_path, "mono")
    body = [
        text(8, y, num, size=size_num, fill=t["amber"], family="mono", weight=700, ls=0.1),
        text(x_title, y, title.upper(), size=size_title, fill=t["text"], family="mono",
             weight=700, ls=0.16),
        line(x_title + title_w + 14, 16.5, width - 8 - path_w - 14, 16.5, stroke=t["line"]),
        text(width - 8, y, where, size=size_path, fill=t["muted"], family="mono", anchor="end"),
    ]
    return svg(width, height, body, f"{num} {title}")
