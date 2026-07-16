# Roadmap — projects not yet public

These are real plans that are **deliberately absent from the website** until built (per `docs/content-rules.md`: no vaporware in front of hiring committees). Each entry says where it will slot in when ready.

## 1. Agentic grading & feedback environment → Claude skill
- **What:** Preston's agent-assisted workflow for grading and delivering individualized student feedback (a contributor to his strong course evaluations). Goal: package it as a reusable Claude skill other instructors can install.
- **Status (July 2026):** Not fully built. No public repo yet. (Note: it is NOT in the `Cheating Analysis` repo — that repo is only proftools.com.)
- **When ready:** add an entry to `data/projects.yaml` with `show_on_site: true` (Tools section, alongside proftools), linking to the skill's repo/marketplace page. If it warrants depth, add a `tools/grading.html` sub-page (build.py would need a second template — keep it just as simple). Also add a line to the Teaching section connecting it to the eval scores.

## 2. Finance-journal Claude skills + journal-fit chatbot
- **What:** Ingest published research from top finance journals into Claude skills for professors; longer-term, a chatbot where a professor submits a paper/idea and receives a **journal fit report** (fit with different journals' tastes, comparable published papers).
- **Status:** Idea stage; ingestion experiments planned.
- **When ready:** the chatbot would live as its own app/domain (it needs a backend; this site is static). The site links to it from the Tools section via `data/projects.yaml`. The skills could be linked directly once published.

## 3. proftools.com growth items (context)
That repo's own `docs/future-features.md` tracks its roadmap (OAuth, email hub, payments). Site copy for proftools should describe only shipped features.

## 4. Site itself
- CV generator (`docs/cv-generation.md`).
- Google Scholar profile link once Preston creates one (hero link row has a slot).
- Per-paper pages if abstracts/appendices outgrow the single page.
