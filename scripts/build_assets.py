"""Build every themed profile asset into assets/ as <name>-dark.svg and <name>-light.svg.

    python scripts/build_assets.py              # write assets/
    python scripts/build_assets.py --png DIR    # also render PNG previews into DIR

Standard library only. PNG previews use rsvg-convert or cairosvg if either is present.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from svg_kit import (arrow_marker, brackets, circle, header, image, line, linear_gradient,
                     path, rect, svg, text, text_width, tspan, wrap)
from tokens import DARK, THEMES, check_contrast

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SRC = ASSETS / "src"        # photo derivatives written by prepare_photos.py
PHOTOS = ASSETS / "photos"
MAX_BYTES = 200 * 1024

HEADERS = [
    ("flagship", "Flagship project", "./warm-pool-governor"),
    ("about", "About", "./about.md"),
    ("experience", "Experience", "./experience.log"),
    ("certifications", "Certifications", "./credly/badges.json"),
    ("projects", "More projects", "./projects/"),
    ("stack", "Stack", "./stack.txt"),
    ("activity", "Activity", "./contributions"),
    ("beyond", "Beyond code", "./off-hours/"),
]

LINKS = [
    ("linkedin", "LinkedIn", True),
    ("email", "Email", False),
    ("credly", "Credly", False),
]

STATUS = [
    ("OPEN TO", "Internship | 2027 Full-time", True),
    ("LOC", "Delhi-NCR · relocate Pan-India", False),
    ("B.TECH CSE", "Class of 2027", False),
]

STATS = [
    ("63.8%", "projected cost saving", "vs always-on"),
    ("2m43s", "sooner than", "a CPU alarm"),
    ("O(1)", "pure decision", "no forecast"),
    ("604", "tests", "run fully offline"),
]

HERO = {
    "rec": "jayasankarmr / profile",
    "name": ("Jayasankar", "M R"),
    "role": "Cloud & DevOps Engineer · Final-Year CSE Student",
    "tagline": "Making systems faster, cheaper, and more reliable.",
}

# About readout: the same cell strip as the flagship stats, facts from the About text.
ABOUT = [
    ("9.35", "CGPA out of 10", "SRM IST, Delhi-NCR"),
    ("6mo", "production ops", "industry internship"),
    ("2", "live client platforms", "DNS · routing · release"),
    ("CCP", "AWS Certified", "Cloud Practitioner"),
]

# Photography frames in Beyond code: (file in assets/photos, caption).
FRAMES = [("tower", "TOWER"), ("peacock", "PEACOCK"), ("cupola", "CUPOLA")]

# (slug, name, subtitle, description, tags)
PROJECTS = [
    ("lifedrop", "LifeDrop", "Blood bank management system",
     "Multi-role app connecting donors, hospitals and admins. Low-stock alerts, rate "
     "limiting, CSRF protection, CSP.",
     ["Flask", "SQLAlchemy", "SQLite", "Tailwind"]),
    ("downright", "Downright", "Chrome / Edge extension",
     "Copy any page as clean Markdown in one keystroke, with correct tables, code fences "
     "and math. No tracking, no network.",
     ["JavaScript", "Chrome Extension API"]),
    ("credit-risk", "Credit Risk Analyser", "Default-risk modelling",
     "End-to-end credit default risk pipeline: feature engineering on borrower and loan "
     "attributes, model comparison and evaluation.",
     ["scikit-learn", "Pandas", "Jupyter"]),
]


# ── section headers ─────────────────────────────────────────────────────────────

def build_headers(t):
    return {f"hdr-{i:02d}-{slug}": header(i, title, where, t)
            for i, (slug, title, where) in enumerate(HEADERS, 1)}


# ── link buttons ────────────────────────────────────────────────────────────────

def link_button(label, filled, t, w=268, h=44):
    fg = t["bg"] if filled else t["amber"]
    body = [
        rect(0.5, 0.5, w - 1, h - 1, fill=t["amber"] if filled else t["panel"], stroke=t["amber"]),
        text(w / 2, h / 2 + 5, f"{label.upper()} ↗", size=14, fill=fg, family="mono",
             weight=700, anchor="middle", ls=0.1),
    ]
    return svg(w, h, body, label)


def build_links(t):
    return {f"link-{slug}": link_button(label, filled, t) for slug, label, filled in LINKS}


# ── status strip ────────────────────────────────────────────────────────────────

def build_status(t, w=830, h=44):
    size_k, size_v, gap, pad = 11, 13.5, 10, 16
    widths = []
    for key, val, dot in STATUS:
        kw = text_width(key, size_k, "mono", ls=0.14 * size_k) + (14 if dot else 0)
        widths.append(kw + gap + text_width(val, size_v, "sans", 500))
    spare = (w - sum(widths) - 2 * pad * len(STATUS)) / len(STATUS)
    body = [rect(0.5, 0.5, w - 1, h - 1, fill=t["panel"], stroke=t["line"])]
    x = 0
    for i, ((key, val, dot), cw) in enumerate(zip(STATUS, widths)):
        cell = cw + 2 * pad + spare
        if i:
            body.append(line(x, 1, x, h - 1, stroke=t["line"]))
        tx = x + pad
        if dot:
            body.append(circle(tx + 4, h / 2, 4, fill=t["green"]))
            tx += 14
        body.append(text(tx, h / 2 + 4, key, size=size_k, fill=t["muted"], family="mono",
                         ls=0.14))
        tx += text_width(key, size_k, "mono", ls=0.14 * size_k) + gap
        body.append(text(tx, h / 2 + 4.5, val, size=size_v, fill=t["text"], weight=500))
        x += cell
    label = " · ".join(f"{k}: {v}" for k, v, _ in STATUS)
    return {"status": svg(w, h, body, label)}


# ── flagship stat strip ─────────────────────────────────────────────────────────

def stat_strip(cells, t, w=830, h=96):
    """Four readout cells: big mono number (amber in the first), label, muted sub-label."""
    cell = w / len(cells)
    body = [rect(0.5, 0.5, w - 1, h - 1, fill=t["panel"], stroke=t["line"])]
    for i, (num, label, sub) in enumerate(cells):
        x = i * cell
        if i:
            body.append(line(x, 1, x, h - 1, stroke=t["line"]))
        body += [
            text(x + 20, 46, num, size=34, fill=t["amber"] if i == 0 else t["text"],
                 family="mono", weight=700, ls=-0.02),
            text(x + 20, 68, label, size=13, fill=t["text"], weight=500),
            text(x + 20, 84, sub, size=11.5, fill=t["muted"]),
        ]
    return svg(w, h, body, " · ".join(f"{n} {a} {b}" for n, a, b in cells))


def build_stats(t):
    return {"stats": stat_strip(STATS, t)}


def build_about(t):
    return {"about": stat_strip(ABOUT, t)}


# ── warm-pool-governor control loop ─────────────────────────────────────────────

def build_governor(t, w=830, h=250):
    m = 20
    mono = dict(family="mono")
    defs = arrow_marker("am", t["muted"]) + arrow_marker("aa", t["amber"])

    def box(x, y, bw, bh, name, sub, stroke=None, name_raw=None):
        cx = x + bw / 2
        return [
            rect(x + 0.5, y + 0.5, bw - 1, bh - 1, fill=t["panel"], stroke=stroke or t["line"],
                 sw=1.5 if stroke else 1),
            text(cx, y + 22, name_raw or name, size=13.5, fill=t["text"], weight=600,
                 anchor="middle", raw=bool(name_raw)),
            text(cx, y + 40, sub, size=11.5, fill=t["muted"], anchor="middle", **mono),
        ]

    body = [
        text(m, 14, "CONTROL LOOP", size=11, fill=t["muted"], ls=0.14, **mono),
        text(w - m, 14, "two reads, zero writes in steady state", size=11.5, fill=t["muted"],
             anchor="end"),
    ]

    # Row of three, EventBridge above the Lambda.
    ry, rh = 86, 52
    cw_x, cw_w = m, 180
    lb_x, lb_w = 310, 210
    as_x, as_w = w - m - 180, 180
    lb_cx = lb_x + lb_w / 2
    eb_w = 164
    body += [
        rect(lb_cx - eb_w / 2 + 0.5, 26.5, eb_w - 1, 39, fill=t["panel"], stroke=t["line"]),
        text(lb_cx, 42, "EventBridge", size=13.5, fill=t["text"], weight=600, anchor="middle"),
        text(lb_cx, 58, "rate(1 minute)", size=11.5, fill=t["muted"], anchor="middle", **mono),
        line(lb_cx, 66, lb_cx, ry - 2, stroke=t["muted"], sw=1.25, marker="am"),
    ]
    body += box(cw_x, ry, cw_w, rh, "CloudWatch", "CPU · Maximum / 60 s")
    lambda_name = "Lambda · " + tspan("decide(cpu)", family="mono", fill=t["amber"])
    body += box(lb_x, ry, lb_w, rh, "", "pure · O(1) · no I/O", stroke=t["amber"],
                name_raw=lambda_name)
    body += box(as_x, ry, as_w, rh, "Auto Scaling group", "in service ⇄ warm pool")

    mid = ry + rh / 2
    body += [
        line(cw_x + cw_w, mid, lb_x - 3, mid, stroke=t["muted"], sw=1.25, marker="am"),
        text((cw_x + cw_w + lb_x) / 2, mid - 7, "GetMetricData", size=11, fill=t["muted"],
             anchor="middle", **mono),
        line(lb_x + lb_w, mid, as_x - 3, mid, stroke=t["amber"], sw=1.5, marker="aa"),
        text((lb_x + lb_w + as_x) / 2, mid - 7, "PutWarmPool", size=11, fill=t["amber"],
             anchor="middle", **mono),
        text((lb_x + lb_w + as_x) / 2, mid + 16, "if changed", size=11, fill=t["muted"],
             anchor="middle", **mono),
    ]

    # Feedback: the group's CPU flows back into CloudWatch.
    fy = ry + rh + 16
    as_cx, cw_cx = as_x + as_w / 2, cw_x + cw_w / 2
    gap = 62
    body += [
        path(f"M{as_cx} {ry + rh}V{fy}H{lb_cx + gap}M{lb_cx - gap} {fy}H{cw_cx}V{ry + rh + 3}",
             stroke=t["muted"], sw=1.1, dash="4 4", marker="am"),
        text(lb_cx, fy + 4, "CPUUtilization", size=11, fill=t["muted"], anchor="middle", **mono),
    ]

    # Phase bar.
    by = 187
    bw = w - 2 * m
    px = lambda pct: m + bw * pct / 100
    phases = [
        (0, 20, "COST_SAVING", "drain the pool", t["green"], 1, 0),
        (20, 40, "PRE_WARM", "boot 2 off-traffic", t["amber"], 1, 2),
        (40, 100, "MITIGATE", "pull warm into service, re-prepare behind", t["red"], 2, 2),
    ]
    body.append(text(m, by - 10, "PHASE, CHOSEN FROM ONE NUMBER", size=11, fill=t["muted"],
                     ls=0.14, **mono))
    for a, b, *_rest, color, _s, _w in phases:
        body.append(rect(px(a) + (1 if a else 0), by, px(b) - px(a) - (1 if a else 0), 6,
                         fill=color))
    for pct in (0, 20, 40, 100):
        anchor = "start" if pct == 0 else "end" if pct == 100 else "middle"
        body.append(text(px(pct), by + 20, f"{pct}%", size=11, fill=t["muted"], anchor=anchor,
                         **mono))
        if pct in (20, 40):
            body.append(line(px(pct), by - 4, px(pct), by + 10, stroke=t["text"], sw=1.25))

    ny, dy = by + 40, by + 56
    for a, _b, name, desc, color, solid, warm in phases:
        x = px(a) + (10 if a else 0)
        body.append(text(x, ny, name, size=12.5, fill=color, weight=700, **mono))
        sx = x + text_width(name, 12.5, "mono") + 10
        for k in range(solid + warm):
            if k < solid:
                body.append(rect(sx, ny - 10, 11, 11, fill=color))
            else:
                body.append(rect(sx + 0.6, ny - 9.4, 9.8, 9.8, stroke=color, sw=1.2, dash="2.5 1.5"))
            sx += 15
        body.append(text(x, dy, desc, size=11.5, fill=t["muted"]))

    lx = w - m - 176
    body += [
        rect(lx, ny - 9, 9, 9, fill=t["muted"]),
        text(lx + 16, ny, "in service", size=11.5, fill=t["muted"]),
        rect(lx + 0.6, dy - 8.4, 7.8, 7.8, stroke=t["muted"], sw=1.2, dash="2.5 1.5"),
        text(lx + 16, dy, "warm, stopped (EBS only)", size=11.5, fill=t["muted"]),
    ]

    label = ("Control loop: EventBridge triggers a Lambda every minute; it reads CPU from "
             "CloudWatch, picks COST_SAVING (under 20%), PRE_WARM (20–40%) or MITIGATE (40% "
             "and up), and writes the warm pool size to the Auto Scaling group only when it "
             "changes.")
    return {"governor": svg(w, h, body, label, defs)}


# ── hero banner ─────────────────────────────────────────────────────────────────

def build_hero(t, w=830, h=400):
    inset, x0 = 14, 48
    photo_x = w * 0.36                  # photo fills the right 64%
    photo_w = w - photo_x
    # Background colour fades the photo out over its left 60%. The curve stays nearly
    # solid early so the role and tagline, which run over the photo edge, keep contrast.
    fade = [(o / 10 * 0.6, t["bg"], round(1 - (o / 10) ** 2, 3)) for o in range(11)]
    defs = (linear_gradient("fade", fade)
            + f'<clipPath id="onphoto"><rect x="{w * 0.7}" y="0" width="{w * 0.3}" height="{h}"/></clipPath>')
    # The photo is dark in both themes, so marks drawn over it use the bright amber.
    on_photo = DARK["amber"]

    af = 44                             # AF bracket over the photo at 70% x, 50% y
    afx, afy = w * 0.70 - af / 2, h / 2 - af / 2
    ccx, ccy = w * 0.70, h / 2

    body = [
        rect(0, 0, w, h, fill=t["bg"]),
        image(photo_x, 0, photo_w, h, SRC / "hero.jpg"),
        rect(photo_x, 0, photo_w, h, fill="#000", opacity=0.2),   # brightness 0.8
        rect(photo_x - 1, 0, photo_w + 1, h, fill="url(#fade)"),
        brackets(inset, inset, w - 2 * inset, h - 2 * inset, 14, stroke=t["amber"]),
        '<g clip-path="url(#onphoto)">',
        brackets(inset, inset, w - 2 * inset, h - 2 * inset, 14, stroke=on_photo),
        "</g>",
        brackets(afx, afy, af, af, 10, stroke=on_photo, sw=1.5),
        line(ccx - 5, ccy, ccx + 5, ccy, stroke=on_photo, sw=1.25),
        line(ccx, ccy - 5, ccx, ccy + 5, stroke=on_photo, sw=1.25),

        circle(x0 + 4, 52 - 4, 4, fill=t["red"]),
        text(x0 + 14, 52, "REC", size=12, fill=t["red"], family="mono", weight=700, ls=0.14),
        text(x0 + 14 + text_width("REC", 12, "mono", ls=0.14 * 12) + 12, 52, HERO["rec"],
             size=12, fill=t["muted"], family="mono", ls=0.14),

        text(x0 - 2, 172, HERO["name"][0], size=44, fill=t["text"], weight=700, ls=-0.03),
        text(x0 - 2, 220, HERO["name"][1], size=44, fill=t["text"], weight=700, ls=-0.03),
        text(x0, 266, HERO["role"], size=14, fill=t["amber"], family="mono", weight=600),
        text(x0, 298, HERO["tagline"], size=16, fill=t["text"], weight=600),
    ]
    label = (f"{' '.join(HERO['name'])}. {HERO['role']}. {HERO['tagline']}")
    return {"hero": svg(w, h, body, label, defs)}


# ── Beyond code: photo frames ───────────────────────────────────────────────────

def build_frames(t, w=268, h=335, inset=8):
    out = {}
    for i, (slug, caption) in enumerate(FRAMES, 1):
        chip = f"{i:02d} · {caption}"
        cw = text_width(chip, 11, "mono", ls=0.14 * 11) + 16
        body = [
            image(inset, inset, w - 2 * inset, h - 2 * inset, PHOTOS / f"{slug}.jpg"),
            brackets(0, 0, w, h, 16, stroke=t["amber"]),
            rect(inset + 8, h - inset - 30, cw, 22, fill=t["bg"]),
            text(inset + 16, h - inset - 15, chip, size=11, fill=t["text"], family="mono",
                 ls=0.14),
        ]
        out[f"frame-{slug}"] = svg(w, h, body, f"Photograph {chip}")
    return out


# ── More projects: cards ────────────────────────────────────────────────────────

def build_projects(t, w=268, h=220, pad=18):
    out = {}
    inner = w - 2 * pad
    for slug, name, sub, desc, tags in PROJECTS:
        lines = wrap(desc, inner, 12.5)
        tag_lines = [""]
        for tag in tags:            # wrap between tags, never inside one
            trial = f"{tag_lines[-1]} · {tag}" if tag_lines[-1] else tag
            if text_width(trial, 11, "mono") > inner:
                tag_lines.append(tag)
            else:
                tag_lines[-1] = trial
        if len(lines) > 4 or len(tag_lines) > 2:
            raise ValueError(f"{slug}: card text does not fit")
        body = [
            rect(0, 0, w, h, fill=t["panel"]),
            brackets(0, 0, w, h, 14, stroke=t["amber"]),
            text(pad, 38, name, size=16, fill=t["text"], family="mono", weight=700),
            text(pad, 57, sub, size=12, fill=t["muted"]),
        ]
        body += [text(pad, 84 + 17 * k, ln, size=12.5, fill=t["text"])
                 for k, ln in enumerate(lines)]
        ty = h - 50 - 15 * (len(tag_lines) - 1)
        body += [text(pad, ty + 15 * k, ln, size=11, fill=t["muted"], family="mono")
                 for k, ln in enumerate(tag_lines)]
        body.append(text(pad, h - 20, "VIEW REPO ↗", size=11, fill=t["amber"], family="mono",
                         weight=700, ls=0.12))
        label = f"{name}: {sub}. {desc} Built with {', '.join(tags)}."
        out[f"project-{slug}"] = svg(w, h, body, label)
    return out


BUILDERS = [build_headers, build_links, build_status, build_stats, build_governor,
            build_hero, build_about, build_frames, build_projects]


def render_png(src, dst):
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-o", str(dst), str(src)], check=True)
        return True
    try:
        import cairosvg
    except ImportError:
        return False
    cairosvg.svg2png(url=str(src), write_to=str(dst))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", type=Path, help="also render PNG previews into this directory")
    args = ap.parse_args()

    check_contrast()
    ASSETS.mkdir(exist_ok=True)
    written = []
    for theme, t in THEMES.items():
        for build in BUILDERS:
            for name, doc in build(t).items():
                out = ASSETS / f"{name}-{theme}.svg"
                data = doc.encode()
                if len(data) > MAX_BYTES:
                    sys.exit(f"{out.name} is {len(data) // 1024} KB, over the 200 KB limit")
                if not out.exists() or out.read_bytes() != data:
                    out.write_bytes(data)
                written.append(out)
    print(f"{len(written)} assets in {ASSETS.relative_to(ROOT)}/")

    if args.png:
        args.png.mkdir(parents=True, exist_ok=True)
        for src in written:
            if not render_png(src, args.png / (src.stem + ".png")):
                sys.exit("no PNG renderer: install rsvg-convert or `pip install cairosvg`")
        print(f"PNG previews in {args.png}")


if __name__ == "__main__":
    main()
