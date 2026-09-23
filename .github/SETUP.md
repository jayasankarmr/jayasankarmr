# Profile README — setup and maintenance notes

Notes for future-me. This file lives under `.github/` on purpose: GitHub only renders
the root `README.md` on the profile page, so nothing here shows up publicly.

---

## 1. Live links in the README

All placeholders are filled in. These are the external links the README depends on —
if any of them move, they need updating here:

| Link | Points to |
| :--- | :--- |
| LinkedIn badge | `linkedin.com/in/jayasankar-m-r-1483802a5` |
| Credly badge (header) | `credly.com/users/jayasankar-m-r.eede608c` — public profile, all badges |
| AWS CCP verify (×2, Certifications) | `credly.com/badges/7d2823e1-296d-4fbc-b71e-0c4e117b706b` — the specific credential |
| warm-pool-governor | `github.com/jayasankarmr/warm-pool-governor` — featured project, diagram in `assets/` |
| LifeDrop status badge | `img.shields.io/website?url=https://lifedrop-demo.onrender.com` — kept green by an external HTTP ping |

If `resume.pdf` ever gets linked from here, commit it into the repo rather than linking
Google Drive — Drive sharing settings are easy to change by accident.

Content sourced from `JAYASANKAR_M_R_Cloud_Engineer_Resume.pdf` — if you update the resume
(new cert, new role, new metric), the Experience, Certifications and Tech Stack sections
here should be updated to match, or the two will drift apart.

---

## 2. Required repo setting (workflows fail without it)

**Settings → Actions → General → Workflow permissions → "Read and write permissions" → Save.**

Both workflows push (snake to `output`, Credly to `main`). With the default read-only token they fail with a 403.
This cannot be set from code — it has to be clicked once in the web UI.

---

## 3. The workflows

### `.github/workflows/snake.yml`

Renders the contribution graph as a snake eating your commits, in light and dark variants.

- Runs on push to `main`, twice daily on cron, and on manual dispatch.
- `Platane/snk@v3` writes `dist/github-snake.svg` and `dist/github-snake-dark.svg`.
- `crazy-max/ghaction-github-pages@v4` force-pushes `dist/` to a dedicated **`output` branch**.

The `output` branch matters: the generated SVGs never touch `main`, so `main`'s commit
history stays entirely hand-written. The README points at
`raw.githubusercontent.com/jayasankarmr/jayasankarmr/output/github-snake.svg`.

The snake images are blank until the workflow has run once. Kick it off with:

```
gh workflow run snake.yml
gh run watch
```

To change the snake's colours, edit the `?palette=` query on the dark output, or pass
`&color_snake=...&color_dots=...` — see https://github.com/Platane/snk.

### `.github/workflows/credly.yml`

Rebuilds the **Certifications** block (between `<!--START_SECTION:credly-->` and
`<!--END_SECTION:credly-->`) from the public Credly profile's `badges.json`.

- Runs Mondays 02:00 UTC and on manual dispatch: `gh workflow run credly.yml`.
- Logic lives in `.github/scripts/credly.py` (stdlib only). Badges with `type_category ==
  "Certification"` become the big cards; everything else goes in the small training-badge row.
- **Commits only when the output changes**, as `github-actions[bot]`, with message
  `Update Credly badges`. Most weeks it does nothing, so `main`'s history stays hand-written.
- `IN_PROGRESS` at the top of the script holds the SAA card. It disappears on its own once a
  Credly badge with that name shows up — no README edit needed when you pass.
- Don't hand-edit inside the markers; the next run overwrites it. Run the script locally to
  preview: `python3 .github/scripts/credly.py`.

The old "Recent Activity" workflow was removed on purpose: it committed to `main` most days
and duplicated the activity feed GitHub already shows under the README.

---

## 4. The image widgets

These are plain image URLs. No setup, no build step — GitHub fetches them on page load.

### Currently live

| Widget | URL | Status |
| :--- | :--- | :--- |
| Streak card | `streak-stats.demolab.com/?user=jayasankarmr` | working |
| Profile views | `komarev.com/ghpvc/?username=jayasankarmr` | working |
| Skill / status badges | `img.shields.io/badge/...` | working |
| Credly cert badges | `images.credly.com/size/340x340/images/<uuid>/image.png` | working |

Useful streak-card params: `theme=`, `hide_border=`, `date_format=`, `mode=weekly`,
`exclude_days=Sun`. Full list: https://github.com/DenverCoder1/github-readme-streak-stats

> Use `streak-stats.demolab.com`, **not** the `github-readme-streak-stats.herokuapp.com` URL
> most tutorials still show. Heroku killed its free tier; that host is dead.

### Dead — do not use

I tested these while building the README. All three are down, repeatedly, not intermittently:

| Host | Result |
| :--- | :--- |
| `github-readme-stats.vercel.app` | HTTP 503 |
| `github-readme-stats-sigma-five.vercel.app` (community mirror) | HTTP 200, but the SVG body is a "Maximum retries exceeded" error card — worse, because it looks fine to a link checker |
| `github-profile-trophy.vercel.app` | HTTP 402 (Payment Required — the whole deployment is over quota, for every user, not just us) |
| `github-readme-activity-graph.vercel.app` | HTTP 402 |

If you copy a widget from someone else's profile README, **fetch the URL and look at the actual
SVG body** before trusting it. A 200 does not mean it rendered your data.

### Enabling the stats cards (the self-host fix)

The stats + top-languages cards are commented out in `README.md`. The public instances are
rate-limited into uselessness; self-hosting is free and takes about five minutes:

1. Fork https://github.com/anuraghazra/github-readme-stats
2. Create a GitHub personal access token — classic, **no scopes ticked at all** (public data only).
3. Go to https://vercel.com, sign in with GitHub, **Add New → Project**, import your fork.
4. Under **Environment Variables** add `PAT_1` = the token from step 2. Deploy.
5. Vercel gives you `https://<something>.vercel.app`. In `README.md`, uncomment the block in
   the Contribution Tracker section and replace `YOUR-INSTANCE` with that hostname.

Your own instance has its own rate limit budget, so the cards stop erroring.

### Optional extras, if you want more

- **Contribution calendar:** `https://ghchart.rshah.org/0969da/jayasankarmr` — tested and working,
  renders a real 365-day calendar. Caveat: empty cells are hardcoded `#EEEEEE`, so it looks
  washed out on GitHub dark mode and there's no param to fix it. I left it out for that reason.
- **Animated typing header:** `https://readme-typing-svg.demolab.com/?lines=...` — tested, working.
  Left out because you chose the clean/professional look.
- **Dynamic repo shields:** `https://img.shields.io/github/last-commit/jayasankarmr/Downright`,
  `.../stars/...`, `.../followers/...` — all working. I skipped the followers badge because it
  currently reads `0`, which draws attention to the wrong number.

---

## 5. Dark mode

Every themed image uses this pattern:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="...&theme=github_dark" />
  <img src="...&theme=default" alt="..." />
</picture>
```

GitHub honours `<picture>` + `prefers-color-scheme` in READMEs, so the card follows the
viewer's theme. Without this, a card tuned for one theme is unreadable in the other.

The older `#gh-dark-mode-only` / `#gh-light-mode-only` URL-fragment trick still works but is
legacy — prefer `<picture>`.

---

## 6. Images not updating?

GitHub proxies every external image through its **camo** cache, so an updated SVG can keep
showing the old version for a while. To force a refresh:

- Append a throwaway query param that changes the URL: `&v=2`, `&t=20260914`.
- Or `curl -X PURGE https://camo.githubusercontent.com/<hash>` — get the hash by right-clicking
  the stale image → Copy image address.

Some widgets also support `&cache_seconds=1800` to shorten their own server-side cache.

---

## 7. Things GitHub strips from README HTML

Worth knowing before trying to make something look fancier:

- `style="..."` attributes are removed. You cannot set font sizes, colours, or spacing inline.
  "Bigger heading" means `#` / `<h1>`, not CSS.
- `<script>`, `<iframe>`, `<form>`, and CSS `<style>` blocks are stripped entirely.
- These **do** work: `<div align="center">`, `<table>`, `<picture>`, `<img width= height=>`,
  `<details><summary>`, `<br />`, `<a>`, `<h1>`–`<h6>`.
- Markdown syntax is **not** parsed inside an HTML block unless there's a blank line separating
  it — that's why the Certifications table has blank lines inside its `<td>` cells.

---

## 8. Local assets

- `assets/warm-pool-governor-{light,dark}.svg` — the Featured Projects diagram, swapped by
  `<picture>`. Thresholds (20% / 40%) and pool sizes match `governor/config.py` defaults in the
  project repo; if those change, the diagram should too.
- `assets/photos/*.jpg` — 600×600 square crops from the Photography Portfolio, ~100 KB each.
  Swap freely; keep them square and the same size so the strip lines up.
