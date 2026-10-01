"""Design tokens for the profile assets. Both palettes live here and nowhere else.

Accents share lightness and chroma and differ only by hue: amber is the one accent,
green means healthy/earned, red means REC/mitigate.
"""

DARK = {
    "bg": "#0D0B09",      # ink: banners, code blocks
    "panel": "#14110E",   # boxes inside SVGs
    "panel2": "#1B1712",  # secondary fill
    "line": "#2B251E",    # rules, strokes
    "text": "#ECE4D8",
    "muted": "#9B9080",   # captions, labels
    "amber": "#F0A040",
    "green": "#6FCB7F",
    "red": "#F0685A",
}

LIGHT = {
    "bg": "#F4EFE6",      # paper
    "panel": "#FAF6EE",
    "panel2": "#EBE4D7",
    "line": "#D6CCBB",
    "text": "#1C1712",
    "muted": "#6A6053",
    # Plan values were #A85A06 / #2A7D3F, which land at 4.44 and 4.47:1 on paper.
    # Darkened ~4% in lightness to clear 4.5:1 on paper and panel.
    "amber": "#A15606",
    "green": "#28783C",
    "red": "#B93A2B",
}

THEMES = {"dark": DARK, "light": LIGHT}

# Web fonts do not load inside <img> SVGs, so these are system stacks only.
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

# Every SVG is laid out in display pixels (830 wide) and drawn at 2x.
DISPLAY_WIDTH = 830
SCALE = 2
MIN_FONT = 11  # display px


def _luminance(hex_color):
    h = hex_color.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = out
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    a, b = sorted((_luminance(fg), _luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


# Text colour → backgrounds it is allowed to sit on.
TEXT_PAIRS = {
    "text": ("bg", "panel", "panel2"),
    "muted": ("bg", "panel", "panel2"),
    "amber": ("bg", "panel"),
    "green": ("bg", "panel"),
    "red": ("bg", "panel"),
}


def check_contrast(minimum=4.5):
    """Raise if any allowed text/background pair drops below `minimum`."""
    bad = []
    for name, t in THEMES.items():
        for fg, bgs in TEXT_PAIRS.items():
            for bg in bgs:
                r = contrast(t[fg], t[bg])
                if r < minimum:
                    bad.append(f"{name}: {fg} on {bg} = {r:.2f}")
        # Filled amber button: bg-coloured text on amber.
        r = contrast(t["bg"], t["amber"])
        if r < minimum:
            bad.append(f"{name}: bg on amber = {r:.2f}")
    if bad:
        raise SystemExit("contrast below %.1f:1\n  " % minimum + "\n  ".join(bad))


if __name__ == "__main__":
    check_contrast()
    for name, t in THEMES.items():
        for fg, bgs in TEXT_PAIRS.items():
            print(f"{name:5} {fg:6}", "  ".join(f"{bg}={contrast(t[fg], t[bg]):.2f}" for bg in bgs))
