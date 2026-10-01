# Profile README — setup and maintenance notes

Notes for future-me. This file lives under `.github/` on purpose: GitHub only renders
the root `README.md` on the profile page, so nothing here shows up publicly.

---

## 1. Live links in the README

These are the external links the README depends on. If any of them move, update them here
and in `README.md`:

| Link | Points to |
| :--- | :--- |
| LinkedIn button | `linkedin.com/in/jayasankar-m-r-1483802a5` |
| Credly button (header) | `credly.com/users/jayasankar-m-r.eede608c` — public profile, all badges |
| AWS CCP verify (Certifications) | `credly.com/badges/7d2823e1-296d-4fbc-b71e-0c4e117b706b` — the specific credential |
| warm-pool-governor | `github.com/jayasankarmr/warm-pool-governor` — flagship section, diagram is `assets/governor-*.svg` |
| LifeDrop demo | `lifedrop-demo.onrender.com` — kept awake by an external HTTP ping |
| Photography | `jayasankarmr.github.io/Photography-Portfolio/` |

If `resume.pdf` ever gets linked from here, commit it into the repo rather than linking
Google Drive — Drive sharing settings are easy to change by accident.

Content sourced from `JAYASANKAR_M_R_Cloud_Engineer_Resume.pdf` — if you update the resume
(new cert, new role, new metric), the Experience, Certifications and Stack sections here,
and the facts in `scripts/build_assets.py`, should be updated to match, or the two will
drift apart.

---

## 2. Required repo setting (workflows fail without it)

**Settings → Actions → General → Workflow permissions → "Read and write permissions" → Save.**

All three workflows push (assets and Credly to `main`, activity to `output`). With the default
read-only token they fail with a 403. This cannot be set from code — it has to be clicked once
in the web UI.

---

## 3. The workflows

### `.github/workflows/assets.yml`

Rebuilds every themed SVG in `assets/` with `scripts/build_assets.py`.

- Runs on push to `main` that touches `scripts/`, `assets/src/` or `assets/photos/`, and on
  manual dispatch: `gh workflow run assets.yml`.
- **Commits only when an SVG actually changed**, as Jayasankar M R, with message
  `Rebuild profile assets`. The build is deterministic, so if you already ran it locally and
  committed the output, the workflow does nothing.
- A push made with `GITHUB_TOKEN` doesn't trigger other workflows, so it can't loop.

### `.github/workflows/activity.yml`

Builds the Activity panel (contribution grid, current and longest streak, language bar) with
`scripts/build_activity.py`, straight from the GitHub GraphQL API. It replaces the streak
card, the profile-view counter and the snake, so the section has no third-party host.

- Runs daily at 00:30 UTC, on manual dispatch (`gh workflow run activity.yml`), and on push
  to `main` that touches the script or its shared modules.
- `crazy-max/ghaction-github-pages@v4` force-pushes `dist/` to a dedicated **`output` branch**.
  The README points at `raw.githubusercontent.com/jayasankarmr/jayasankarmr/output/activity-*.svg`.

The `output` branch matters twice over: the daily refresh never touches `main`'s history,
and commits on a non-default branch don't count as contributions, so the job can't keep the
streak it draws alive by itself.

- Streaks use every contribution year, not just the last 12 months.
- Languages are bytes summed over public, non-fork repos I own. `EXCLUDE_LANGUAGES` at the
  top of the script drops Jupyter Notebook, whose bytes are mostly embedded output.
- The panel is blank until the workflow has run once.

Preview locally:

```
GITHUB_TOKEN=$(gh auth token) python3 scripts/build_activity.py --out /tmp/activity --png /tmp/activity
```

### `.github/workflows/credly.yml`

Rebuilds the **Certifications** block (between `<!--START_SECTION:credly-->` and
`<!--END_SECTION:credly-->`) from the public Credly profile's `badges.json`.

- Runs Mondays 02:00 UTC and on manual dispatch: `gh workflow run credly.yml`.
- Logic lives in `.github/scripts/credly.py` (stdlib only). Badges with `type_category ==
  "Certification"` become the cards; everything else goes in the training-badge row.
- **Commits only when the output changes**, as `github-actions[bot]`, with message
  `Update Credly badges`. Most weeks it does nothing.
- `IN_PROGRESS` at the top of the script holds the SAA card, drawn with
  `assets/badge-saa-gray.png`. It disappears on its own once a Credly badge with that name
  shows up — no README edit needed when you pass. The gray PNG can be deleted then.
- Don't hand-edit inside the markers; the next run overwrites it. Run the script locally to
  preview: `python3 .github/scripts/credly.py`.

The old "Recent Activity" workflow was removed on purpose: it committed to `main` most days
and duplicated the activity feed GitHub already shows under the README.

---

## 4. Generated assets

Everything visual in the README is a local SVG, in `-dark` and `-light` pairs.

- `scripts/tokens.py` — both colour palettes and the font stacks. Change a colour here, never in
  an SVG. `python3 scripts/tokens.py` prints every text/background contrast ratio.
- `scripts/svg_kit.py` — shared drawing helpers (text, corner brackets, section header).
- `scripts/build_assets.py` — every static asset, and the facts printed in them (status strip,
  stat strips, project cards). Edit the text there, then run
  `python3 scripts/build_assets.py --png /tmp/preview` to check the PNGs.
- `scripts/prepare_photos.py` — resizes a full-size photo into `assets/src/` with `sips`
  (macOS). Run it locally when the hero photo changes; CI only base64-embeds the result.
- `assets/photos/*.jpg` — the three photography frames, embedded as-is.

Rules the builder enforces: every SVG under 200 KB, no text under 11 px at display size, and
all text pairs at 4.5:1 contrast or better.

### Third-party images

Only the Credly badge images (`images.credly.com`) are fetched from outside GitHub.

If you're ever tempted to add a widget from someone else's profile, these were all dead when
I last checked — **fetch the URL and look at the actual SVG body** before trusting one. A 200
does not mean it rendered your data.

| Host | Result |
| :--- | :--- |
| `github-readme-stats.vercel.app` | HTTP 503 |
| `github-readme-stats-sigma-five.vercel.app` (community mirror) | HTTP 200, but the SVG body is a "Maximum retries exceeded" error card |
| `github-profile-trophy.vercel.app` | HTTP 402 (deployment over quota) |
| `github-readme-activity-graph.vercel.app` | HTTP 402 |
| `github-readme-streak-stats.herokuapp.com` | Dead since Heroku's free tier ended |

---

## 5. Dark mode

Every themed image uses this pattern:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/name-dark.svg" />
  <img src="assets/name-light.svg" alt="..." />
</picture>
```

GitHub honours `<picture>` + `prefers-color-scheme` in READMEs, so the image follows the
viewer's theme. Without this, an image tuned for one theme is unreadable in the other.

The older `#gh-dark-mode-only` / `#gh-light-mode-only` URL-fragment trick still works but is
legacy — prefer `<picture>`.

---

## 6. Images not updating?

GitHub proxies every external image (Credly, and the activity panel on `raw.githubusercontent.com`)
through its **camo** cache, so an updated image can keep showing the old version for a while.
To force a refresh:

- Append a throwaway query param that changes the URL: `?v=2`, `?t=20260914`.
- Or `curl -X PURGE https://camo.githubusercontent.com/<hash>` — get the hash by right-clicking
  the stale image → Copy image address.

Images in `assets/` on `main` are served directly and update with the commit.

---

## 7. Things GitHub strips from README HTML

Worth knowing before trying to make something look fancier:

- `style="..."` attributes are removed. You cannot set font sizes, colours, or spacing inline.
  That's why every styled element is an SVG.
- `<script>`, `<iframe>`, `<form>`, and CSS `<style>` blocks are stripped entirely.
- These **do** work: `<div align="center">`, `<table>`, `<picture>`, `<img width= height=>`,
  `<details><summary>`, `<br />`, `<a>`, `<sub>`, `<h1>`–`<h6>`.
- SVGs shown through `<img>` can't load web fonts, scripts, external images, or follow links
  inside them. Photos are base64-embedded, fonts are system stacks, and links are `<a>` tags
  around the `<img>`.
- Markdown syntax is **not** parsed inside an HTML block unless there's a blank line separating
  it — that's why the Experience and Certifications table cells have blank lines inside them.
