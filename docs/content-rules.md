# Content rules — privacy & accuracy

The repo is **public** and the site is the public face of Preston's academic career. These rules protect both.

## Never public (site, repo, or any published material)
- The recommendation letter (`archive/fellowship-2025/letter_of_recommendation.pdf`) — confidential, written for one purpose. Never quote, summarize publicly, or republish.
- Home address and phone number. Any PDF published on the site (CV included) must have them stripped. Email is fine.
- Contents of `archive/` and `applications/`.
- Video files (too large for git regardless; the public copy lives on YouTube).
- Names of journals where papers are under review — site says "Under review" only. (CV may name journals if Preston chooses; default to his current CV's practice.)
- Unbuilt projects (grading agent, journal-fit chatbot) — announcing vaporware reads poorly to hiring committees. They live in `docs/roadmap.md` until real.

## CV-only (fine in application materials, not on the website)
- GPAs (3.98 PhD, 3.7 undergrad) — website GPA-listing is against academic-site norms.
- Graduate assistant line, coursework list, granular employment metrics.

## Accuracy
- **Sources of truth, in order:** (1) verified SSRN abstracts (see `abstract_verified` in `data/papers.yaml`), (2) the current CV in `archive/annual-reports/<latest>/`, (3) `docs/facts.md`. Local research-repo drafts are NOT sources — figures differ across draft versions (the Robinhood paper's PFOF magnitudes were explicitly flagged as needing verification).
- SSRN blocks automated fetching (HTTP 403). To verify an abstract, ask Preston to paste it. Record the verification date in `papers.yaml`.
- Paper status changes fast (submissions, R&Rs, acceptances). When drafting anything status-dependent, confirm current status with Preston rather than trusting file dates.
- Every quantitative claim on the site must be traceable to a tagged fact in `facts.md` or a verified abstract in `papers.yaml`.

## Tone boundaries
- No hype, no marketing language, no emojis on the site. First person, plain, confident. See `docs/style-guide.md`.
