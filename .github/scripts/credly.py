"""Rebuild the Certifications block in README.md from the public Credly profile.

Rewrites everything between <!--START_SECTION:credly--> and <!--END_SECTION:credly-->.
Standard library only, so the workflow needs no pip install.
"""
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

USER = "jayasankar-m-r.eede608c"
README = Path(__file__).resolve().parents[2] / "README.md"
START, END = "<!--START_SECTION:credly-->", "<!--END_SECTION:credly-->"

# Certifications being worked toward. Each one drops off automatically as soon as a
# Credly badge with the same name appears on the profile.
IN_PROGRESS = [
    {
        "name": "AWS Certified Solutions Architect – Associate",
        "match": "AWS Certified Solutions Architect - Associate",
        "issuer": "Amazon Web Services",
        "image": "0e284c3f-5164-4b21-8660-0d84737941bc",
        "note": "targeting Dec 2026",
    },
]

CERTS_PER_ROW = 2


def fetch():
    req = urllib.request.Request(
        f"https://www.credly.com/users/{USER}/badges.json?page=1&per=48",
        headers={"User-Agent": "Mozilla/5.0 (profile README sync)", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)["data"]
    return [b for b in data if b.get("state") == "accepted" and b.get("public", True)]


def image(uuid_or_url, size):
    m = re.search(r"images/([0-9a-f-]{36})/([^/?#]+)", uuid_or_url)
    uuid, name = (m.group(1), m.group(2)) if m else (uuid_or_url, "image.png")
    return f"https://images.credly.com/size/{size}x{size}/images/{uuid}/{name}"


def issuer(badge):
    for e in badge.get("issuer", {}).get("entities", []):
        if e.get("primary"):
            return e["entity"]["name"].replace(" Training and Certification", "")
    return ""


def short_date(iso):
    y, m, _ = iso.split("-")
    return f"{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m) - 1]} {y}"


def cert_cells(b):
    t = b["badge_template"]
    url = f"https://www.credly.com/badges/{b['id']}"
    name = html.escape(t["name"])
    valid = f"`EARNED {short_date(b['issued_at_date'])}`"
    if b.get("expires_at_date"):
        valid += f" · valid to {short_date(b['expires_at_date'])}"
    return (
        f'<td align="center" width="130">\n<a href="{url}">\n'
        f'<img src="{image(t["image_url"], 340)}" width="95" alt="{name}" />\n</a>\n</td>\n'
        f"<td>\n\n**{name}**\n{valid} · {issuer(b)}\n\n[Verify on Credly →]({url})\n\n</td>"
    )


def planned_cells(p):
    name = html.escape(p["name"])
    return (
        f'<td align="center" width="130">\n'
        f'<img src="{image(p["image"], 340)}" width="95" alt="{name}" />\n</td>\n'
        f"<td>\n\n**{name}**\n`IN PROGRESS` · {p['note']}\n\n</td>"
    )


def render(badges):
    certs = [b for b in badges if b["badge_template"].get("type_category") == "Certification"]
    training = [b for b in badges if b not in certs]
    earned = {b["badge_template"]["name"].replace("–", "-").lower() for b in certs}
    planned = [p for p in IN_PROGRESS if p["match"].lower() not in earned]

    cells = [cert_cells(b) for b in certs] + [planned_cells(p) for p in planned]
    rows = [cells[i:i + CERTS_PER_ROW] for i in range(0, len(cells), CERTS_PER_ROW)]
    out = ["<table>"] + ["<tr>\n" + "\n".join(r) + "\n</tr>" for r in rows] + ["</table>"]

    if training:
        icons = " ".join(
            f'<a href="https://www.credly.com/badges/{b["id"]}"><img src="{image(b["badge_template"]["image_url"], 110)}" '
            f'width="52" alt="{html.escape(b["badge_template"]["name"])}" title="{html.escape(b["badge_template"]["name"])}" /></a>'
            for b in training
        )
        out += ["", f"**Training badges** <sub>({len(training)} · hover for names)</sub>", "", icons]
    return "\n".join(out)


def main():
    readme = README.read_text()
    if START not in readme or END not in readme:
        sys.exit(f"markers {START} / {END} not found in README.md")
    block = render(fetch())
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: f"{START}\n{block}\n{END}", readme, flags=re.S)
    if new != readme:
        README.write_text(new)
        print("README.md updated")
    else:
        print("no change")


if __name__ == "__main__":
    main()
