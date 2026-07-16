# Style guide

## Voice

- First person, plain, and confident. No hype, emojis, or marketing language.
- The central narrative is that markets are engineered systems. Preston's mechanical engineering background leads naturally to market microstructure, where system design, incentives, and measured outcomes meet.
- Paper descriptions state the question, design, and finding directly.
- Academic hiring committees are the primary audience. Industry researchers and recruiters are secondary.
- Never use em dashes in public site copy. `build.py` enforces this rule.

## Design

- Five pages: Home, Research, Teaching, Tools, and About.
- Warm editorial palette: paper, deep navy, and restrained burgundy.
- Typography should feel bookish and credible, not ornamental. Use Charter-style serif stacks for research titles and a neutral system sans-serif for navigation and metadata.
- Avoid oversized italic display words, script fonts, gradients, excessive pills, generic SaaS layouts, and decorative stock imagery.
- The original headshot is the primary image. Do not alter Preston's identity or facial features.
- Light and dark themes must both remain legible.
- Desktop layout uses structured editorial grids. Mobile collapses cleanly with no horizontal page overflow.

## HTML conventions

- One `h1` per page, semantic sections, articles for papers, and accessible table headers.
- Papers link to SSRN via `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=<id>`.
- External links use `rel="noopener"` and open in the same tab.
- Abstracts stay collapsed in native `details` elements.
- Page content comes from YAML and `build.py`, not hand-edited generated HTML.

## File conventions

- Edit content in `data/`, layout in `templates/`, and assets in `static/`.
- `site/` is generated output and must be committed after every build.
- Paper IDs use kebab case. Dates in YAML use `YYYY-MM`.
