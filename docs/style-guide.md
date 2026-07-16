# Style guide

## Voice (site + materials)
- First person ("I study…"), plain and confident. No hype, no superlatives about self, no emojis, no marketing verbs ("leverage", "passionate").
- Paper descriptions: one sentence on the question, one on the finding. Findings stated as the paper states them, hedged as the paper hedges them.
- Audience is dual: academic hiring committees first, industry recruiters second. Lead with research; keep tools/background sections tight and concrete.

## Design (site)
- Single centered column, max-width ~46rem, generous whitespace.
- Typography: Georgia/serif stack for body, system sans for headings and metadata. Near-black `#1a1a1a` on white; dark mode via `prefers-color-scheme`.
- One accent color: muted navy `#1f4e79` (links, JMP badge). Avoid UC red — reads as a university page, not a personal one.
- Headshot: modest size (~150px), rounded, top of page.
- Abstracts collapse behind a `<details>` element — no custom JS needed.
- Badges (job market paper, awards, media) are small uppercase labels, not colorful pills.
- Mobile: everything single-column, no horizontal scroll. Test at 375px width.

## HTML conventions
- Semantic: one `<h1>` (name), `<h2>` per section, `<article>` per paper.
- Papers link to SSRN via `https://papers.ssrn.com/abstract=<id>`.
- All external links `rel="noopener"`, open in same tab (academic norm).
- The template uses `{{placeholder}}` markers replaced by `build.py`; loops are rendered in Python, not in the template.

## File conventions
- YAML in `data/` is the only place content is edited. `site/` is generated.
- kebab-case ids for papers (`round-lots`, `collaring`).
- Dates in YAML as `YYYY-MM`.
