"""Build the Activity panel (contribution grid, streaks, language bar) from the GitHub API.

    GITHUB_TOKEN=... python scripts/build_activity.py              # write dist/
    GITHUB_TOKEN=... python scripts/build_activity.py --png DIR    # also PNG previews

Writes activity-dark.svg and activity-light.svg. The workflow publishes them to the
`output` branch, so the daily refresh never commits to main. Standard library only.
"""
import argparse
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

from build_assets import MAX_BYTES, render_png
from svg_kit import line, rect, svg, text, text_width
from tokens import THEMES, check_contrast

ROOT = Path(__file__).resolve().parents[1]
USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "jayasankarmr")

# Notebook bytes are mostly embedded outputs, so they swamp the languages actually written.
EXCLUDE_LANGUAGES = {"Jupyter Notebook"}
TOP_LANGUAGES = 5

LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
TINTS = [None, 0.35, 0.55, 0.78, 1.0]        # amber over the panel, per level
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


# ── data ────────────────────────────────────────────────────────────────────────

def graphql(query, token, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-activity"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if body.get("errors"):
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]


CALENDAR = "contributionCalendar { totalContributions weeks { contributionDays { date contributionCount contributionLevel } } }"


def fetch(token):
    first = graphql(f"""
        query($login: String!) {{ user(login: $login) {{
          contributionsCollection {{ contributionYears {CALENDAR} }}
          repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {{
            nodes {{ languages(first: 20) {{ edges {{ size node {{ name }} }} }} }}
          }}
        }} }}""", token, login=USER)["user"]

    # Streaks can run across years, so pull every year's calendar, one alias per year
    # (the API caps a single range at one year).
    now = dt.datetime.now(dt.timezone.utc)
    years = first["contributionsCollection"]["contributionYears"]
    parts = []
    for y in years:
        end = min(dt.datetime(y, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc), now)
        parts.append(f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", '
                     f'to: "{end:%Y-%m-%dT%H:%M:%SZ}") {{ {CALENDAR} }}')
    history = graphql(f"query($login: String!) {{ user(login: $login) {{ {' '.join(parts)} }} }}",
                      token, login=USER)["user"]

    days = {}
    for coll in history.values():
        for week in coll["contributionCalendar"]["weeks"]:
            for d in week["contributionDays"]:
                days[d["date"]] = d["contributionCount"]

    langs = {}
    for repo in first["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            if name not in EXCLUDE_LANGUAGES:
                langs[name] = langs.get(name, 0) + e["size"]

    return first["contributionsCollection"]["contributionCalendar"], days, langs


def streaks(days, today):
    """(current, longest, last active day). Streaks are (length, first day, last day)."""
    dates = sorted(dt.date.fromisoformat(d) for d, n in days.items() if n > 0)
    runs = []
    for d in dates:
        if runs and d - runs[-1][1] == dt.timedelta(days=1):
            runs[-1][1] = d
        else:
            runs.append([d, d])
    runs = [((b - a).days + 1, a, b) for a, b in runs]
    longest = max(runs, default=None)
    # A streak is still alive if it ends today or yesterday (today may not have a commit yet).
    current = runs[-1] if runs and (today - runs[-1][2]).days <= 1 else None
    return current, longest, (dates[-1] if dates else None)


def languages(totals):
    """Top languages by bytes as (name, share), with the rest folded into Other."""
    total = sum(totals.values())
    if not total:
        return []
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    out = [(name, size / total) for name, size in ranked[:TOP_LANGUAGES]]
    rest = sum(size for _, size in ranked[TOP_LANGUAGES:])
    if rest:
        out.append(("Other", rest / total))
    return out


# ── drawing ─────────────────────────────────────────────────────────────────────

def mix(fg, bg, a):
    f, b = (tuple(int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) for c in (fg, bg))
    return "#" + "".join(f"{round(x * a + y * (1 - a)):02X}" for x, y in zip(f, b))


def fmt_day(d):
    return f"{MONTHS[d.month - 1]} {d.day}"


def span(run, last_active=None):
    if not run:
        return f"last active {fmt_day(last_active)}, {last_active.year}" if last_active else "none yet"
    _, a, b = run
    if a == b:
        return f"{fmt_day(a)}, {a.year}"
    if a.year == b.year:
        return f"{fmt_day(a)} – {fmt_day(b)}, {b.year}"
    return f"{fmt_day(a)}, {a.year} – {fmt_day(b)}, {b.year}"


def days_word(n):
    return "day" if n == 1 else "days"


def build(t, calendar, current, longest, last_active, langs, w=830, h=200):
    m, cell, pitch = 20, 10, 12
    shade = [t["line"]] + [mix(t["amber"], t["panel"], a) for a in TINTS[1:]]
    weeks = calendar["weeks"]
    grid_w = len(weeks) * pitch - (pitch - cell)
    gx, gy = m, 58
    split_x = gx + grid_w + 16          # rule between the grid and the streak readouts
    split_y = 156                       # rule above the language bar

    body = [
        rect(0.5, 0.5, w - 1, h - 1, fill=t["panel"], stroke=t["line"]),
        line(split_x, 1, split_x, split_y, stroke=t["line"]),
        line(1, split_y, w - 1, split_y, stroke=t["line"]),
        text(m, 28, f"CONTRIBUTIONS · {calendar['totalContributions']:,} IN THE LAST YEAR",
             size=11, fill=t["muted"], family="mono", ls=0.14),
    ]

    # Legend, right-aligned to the grid.
    lx = gx + grid_w
    body.append(text(lx, 28, "MORE", size=11, fill=t["muted"], family="mono", anchor="end"))
    lx -= text_width("MORE", 11, "mono") + 6 + 5 * pitch - 2
    for k, colour in enumerate(shade):
        body.append(rect(lx + k * pitch, 19, cell, cell, rx=2, fill=colour))
    body.append(text(lx - 6, 28, "LESS", size=11, fill=t["muted"], family="mono", anchor="end"))

    # Grid: one column per week, Sunday on top. Month names sit over the first full week.
    last_label = -9
    for col, week in enumerate(weeks):
        x = gx + col * pitch
        for d in week["contributionDays"]:
            date = dt.date.fromisoformat(d["date"])
            row = (date.weekday() + 1) % 7
            level = LEVELS.index(d["contributionLevel"])
            body.append(rect(x, gy + row * pitch, cell, cell, rx=2, fill=shade[level]))
        first = dt.date.fromisoformat(week["contributionDays"][0]["date"])
        if first.day <= 7 and col - last_label >= 3 and col < len(weeks) - 1:
            body.append(text(x, gy - 8, MONTHS[first.month - 1], size=11, fill=t["muted"],
                             family="mono"))
            last_label = col

    # Streak readouts.
    rx = split_x + 16
    for i, (label, run, colour) in enumerate((("CURRENT STREAK", current, t["amber"]),
                                               ("LONGEST STREAK", longest, t["text"]))):
        y = 28 + i * 66
        n = run[0] if run else 0
        num_w = text_width(str(n), 26, "mono")
        body += [
            text(rx, y, label, size=11, fill=t["muted"], family="mono", ls=0.14),
            text(rx, y + 28, str(n), size=26, fill=colour, family="mono", weight=700, ls=-0.02),
            text(rx + num_w + 4, y + 28, days_word(n), size=12.5, fill=t["muted"]),
            text(rx, y + 45, span(run, last_active), size=11, fill=t["muted"]),
        ]

    # Language bar: one bar, amber fading by rank, labels underneath.
    bar_y, label_y = 170, 188
    bar_w = w - 2 * m
    x = m
    label_x = m
    for i, (name, share) in enumerate(langs):
        colour = t["muted"] if name == "Other" else mix(t["amber"], t["panel"], 1 - i * 0.13)
        seg = bar_w * share
        body.append(rect(x, bar_y, max(seg - 2, 1), 6, fill=colour))
        x += seg
        pct = f"{share * 100:.1f}%"
        body += [
            rect(label_x, label_y - 8, 8, 8, fill=colour),
            text(label_x + 13, label_y, name, size=12, fill=t["text"]),
        ]
        nx = label_x + 13 + text_width(name, 12) + 5
        body.append(text(nx, label_y, pct, size=11, fill=t["muted"], family="mono"))
        label_x = nx + text_width(pct, 11, "mono") + 20
    if label_x - 20 > w - m:
        raise ValueError("language labels do not fit")

    cur = current[0] if current else 0
    best = longest[0] if longest else 0
    label = (f"{calendar['totalContributions']:,} contributions in the last year. "
             f"Current streak {cur} {days_word(cur)}, longest {best} {days_word(best)}. "
             "Languages by bytes: "
             + ", ".join(f"{n} {s * 100:.1f}%" for n, s in langs) + ".")
    return svg(w, h, body, label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "dist", help="output directory")
    ap.add_argument("--png", type=Path, help="also render PNG previews into this directory")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("set GITHUB_TOKEN (locally: GITHUB_TOKEN=$(gh auth token))")

    check_contrast()
    calendar, days, langs = fetch(token)
    today = dt.date.fromisoformat(calendar["weeks"][-1]["contributionDays"][-1]["date"])
    current, longest, last_active = streaks(days, today)
    langs = languages(langs)

    args.out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        out = args.out / f"activity-{theme}.svg"
        data = build(t, calendar, current, longest, last_active, langs).encode()
        if len(data) > MAX_BYTES:
            sys.exit(f"{out.name} is {len(data) // 1024} KB, over the 200 KB limit")
        out.write_bytes(data)
        if args.png:
            args.png.mkdir(parents=True, exist_ok=True)
            if not render_png(out, args.png / f"activity-{theme}.png"):
                sys.exit("no PNG renderer: install rsvg-convert or `pip install cairosvg`")
    print(f"activity-{{dark,light}}.svg in {args.out}")


if __name__ == "__main__":
    main()
