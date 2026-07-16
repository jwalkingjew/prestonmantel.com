# Preston Mantel — PhD Home Base & prestonmantel.com

This repo is two things:
1. **The source for prestonmantel.com**: a five-page academic site generated from YAML data.
2. **Preston's PhD home base**: canonical career data and docs that future agents use to update the site, generate CVs, and draft application materials.

Preston is a finance PhD candidate at the University of Cincinnati (Lindner College of Business), advisor Mehmet Sağlam, expected graduation May 2027. Research area: market microstructure, retail investor protection, market regulation.

## HARD RULES (read before doing anything)

1. **This repo is PUBLIC on GitHub.** Never commit or publish: anything in `archive/` or `applications/`, the recommendation letter, video files, Preston's home address, or phone number. GPA goes on the CV only, never the website. `.gitignore` enforces most of this — do not weaken it.
2. **Never put empirical numbers on the site or in materials unless they match a verified SSRN abstract (`abstract_verified` date in `data/papers.yaml`) or the current CV.** Local paper drafts in the research repos contain figures that vary across versions (the Robinhood paper's PFOF figures were specifically flagged as unverified). When in doubt, ask Preston.
3. **SSRN returns 403 to automated fetches.** Abstract verification requires Preston pasting the text. Ask; don't guess or reconstruct from drafts.
4. **Never name the journal a paper is under review at on the public site** — "Under review" only. Journal names are fine in `private_notes` and on the CV if Preston asks.
5. `site/` is **generated output** — never hand-edit it. Edit `data/` or `templates/`, then rebuild.
6. **Never use em dashes in public site copy.** `build.py` rejects them in generated text assets.

## The update loop

```
edit data/*.yaml (or templates/, static/)
python3 build.py            # regenerates site/ — fails loudly on missing fields
python3 -m http.server 8000 -d site   # preview at http://localhost:8000
git add -A && git commit && git push  # push to main = deploy (GitHub Pages Action)
```

Commit both the data change AND the regenerated `site/` output. Deploy status: `gh run list --limit 3`.

## Map

| Path | What it is |
|---|---|
| `data/profile.yaml` | Name, title, engineering narrative, links, bio, and video URL |
| `data/papers.yaml` | Canonical paper metadata. Feeds site now, CV generation later |
| `data/teaching.yaml` | Courses, evals, service |
| `data/projects.yaml` | Tools (proftools.com live; roadmap items have `show_on_site: false`) |
| `docs/facts.md` | Verified biography, each fact tagged with source + audience |
| `docs/content-rules.md` | Full privacy + accuracy rules |
| `docs/style-guide.md` | Voice + design conventions |
| `docs/deploy.md` | Hosting, DNS, verification commands, rollback |
| `docs/cv-generation.md` | Spec for future YAML→CV pipeline |
| `docs/roadmap.md` | Unbuilt projects (grading skill, journal-fit chatbot) and how they'll slot in |
| `archive/` | GITIGNORED. Fellowship 2025 application, annual reports, videos, CV PDFs |
| `applications/` | GITIGNORED. Workspace for cover letters, statements, drafts |
| `build.py` | Builds Home, Research, Teaching, Tools, and About pages from YAML |

## Related local repos (context for research/application work)

- `~/environments/ResearchEnv/round_lot_size` — job market paper (When Lots Matter)
- `~/environments/ResearchEnv/collaring` — Robinhood order-collaring paper
- `~/environments/ResearchEnv/prediction_markets_research` — prediction-market taker-delay paper
- `~/environments/ResearchEnv/Data from Mehmet` — institutional market-making paper
- `~/environments/ResearchEnv/Cheating Analysis` — proftools.com (Canvas quiz-integrity tool)
