# CV & application-material generation (spec — not yet built)

Goal: the YAML in `data/` is the single source of truth; CVs, resumes, and application materials are rendered from it so nothing drifts.

## Current state (July 2026)
- The live CV is a manually maintained LaTeX/PDF: `archive/annual-reports/2026/preston_mantel_cv.pdf`. The web-published copy at `static/files/Mantel_CV.pdf` must have home address + phone stripped (see `docs/content-rules.md`).
- `data/*.yaml` already contains everything the CV needs except coursework and the graduate-assistant line (both in `docs/facts.md`).

## Target pipeline
1. `cv.py` (sibling of `build.py`) reads `data/*.yaml` + a `data/cv-extras.yaml` (cv-only items: GPAs, coursework, GA line, journal names for under-review papers).
2. Renders Markdown → PDF via pandoc, or a LaTeX template mirroring the current CV's layout (preferred if Preston supplies the .tex source — ask).
3. Two variants from one command: `--web` (address/phone stripped → `static/files/Mantel_CV.pdf`) and `--full` (complete, for applications, written to `applications/`).

## Application materials
Agents drafting cover letters / research statements / teaching statements should:
- Pull facts only from `data/*.yaml` + `docs/facts.md` (audience tags apply).
- Confirm current paper statuses with Preston first (they change fast).
- Write drafts into `applications/<YYYY-MM>-<school-or-purpose>/` (gitignored).
- Reuse the narratives in `archive/fellowship-2025/statement_of_goals.pdf` and the video script as raw material for research-statement framing (content reuse is fine; republishing the PDFs is not).
