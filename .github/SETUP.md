# Profile README — setup and maintenance notes

Notes for future-me. This file lives under `.github/` on purpose: GitHub only renders
the root `README.md` on the profile page, so nothing here shows up publicly.

---

## 1. Placeholders to fill in

Search `README.md` for these and replace them:

| Placeholder | Where | What to put |
| :--- | :--- | :--- |
| `YOUR-LINKEDIN-HANDLE` | header badge | your LinkedIn vanity URL slug |
| `YOUR-CREDLY-HANDLE` | header badge + Certifications (×3) | your Credly profile slug |
| `ADD-YOUR-PAPER-LINK-HERE` | Featured Projects, warm-pool row | the research paper (DOI, arXiv, Drive, or a PDF committed to this repo) |

Also check: the **Graduating May 2027** badge and the **Chennai, India** badge in the header,
and the `sihcivic` project description — that repo has no description on GitHub, so the line
in the table is my best guess from the repo name and stack. Correct it if it's wrong.

---

## 2. Required repo setting (workflows fail without it)

**Settings → Actions → General → Workflow permissions → "Read and write permissions" → Save.**

Both workflows push commits. With the default read-only token they fail with a 403.
This cannot be set from code — it has to be clicked once in the web UI.

---

## 3. The two workflows

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

### `.github/workflows/activity.yml`

Rewrites the block between `<!--START_SECTION:activity-->` and `<!--END_SECTION:activity-->`
in `README.md` with your 5 most recent public GitHub events. Daily cron + manual dispatch.

This one **does** commit to `main`, as `github-actions[bot]`. `COMMIT_MSG` is set to a plain
`Update recent activity` to match this repo's commit-message convention.

Note: it only ever sees **public** events. If most of your work is in private repos this
section will look sparse — that's a signal to make more work public, not a bug.

Change `MAX_LINES: 5` to show more or fewer entries.

To remove it entirely: delete the workflow file and the `## Recent Activity` section.

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
