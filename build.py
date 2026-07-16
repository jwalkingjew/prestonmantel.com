#!/usr/bin/env python3
"""Build prestonmantel.com: render data/*.yaml through templates/index.html into site/.

Usage: python3 build.py
The only dependency is PyYAML. site/ is fully regenerated on every run.
"""
import html
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DOMAIN = "prestonmantel.com"

STATUS_GROUPS = [
    ("job_market_paper", "Job Market Paper"),
    ("under_review", "Under Review"),
    ("working", "Working Papers"),
]


def esc(s):
    return html.escape(str(s), quote=False)


def load(name, required):
    path = ROOT / "data" / f"{name}.yaml"
    data = yaml.safe_load(path.read_text())
    items = data if isinstance(data, list) else [data]
    for item in items:
        for key in required:
            if key not in item:
                sys.exit(f"ERROR: {path.name}: entry missing required field '{key}': {item}")
    return data


def render_links(links):
    parts = [f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>'
             for l in links if l.get("url")]
    return '<span class="sep">·</span>'.join(parts)


def render_authors(paper):
    others = [a for a in paper["authors"] if a != "Preston Mantel"]
    if not others:
        return ""
    affil = paper.get("author_affiliations") or {}
    names = [f"{esc(a)} ({esc(affil[a])})" if a in affil else esc(a) for a in others]
    joined = " and ".join(names) if len(names) < 3 else ", ".join(names[:-1]) + ", and " + names[-1]
    return f'<p class="authors">with {joined}</p>'


def render_paper(paper):
    title = esc(paper["title"])
    if paper.get("ssrn"):
        title_html = f'<a href="https://papers.ssrn.com/abstract={paper["ssrn"]}">{title}</a>'
    else:
        title_html = title

    badges = "".join(f'<span class="badge">{esc(b)}</span>' for b in paper.get("awards", []))
    for m in paper.get("media", []):
        label = f"Media: {esc(m['outlet'])}"
        badges += (f'<span class="badge"><a href="{esc(m["url"])}">{label}</a></span>'
                   if m.get("url") else f'<span class="badge">{label}</span>')

    body = ""
    if paper.get("abstract") and paper.get("abstract_verified"):
        body = (f'<details><summary>Abstract</summary>'
                f'<p>{esc(paper["abstract"])}</p></details>')
    elif paper.get("bullets"):
        lis = "".join(f"<li>{esc(b)}</li>" for b in paper["bullets"])
        body = f'<ul class="paper-points">{lis}</ul>'

    extras = []
    if paper.get("presentations"):
        extras.append("Presented at: " + "; ".join(esc(p) for p in paper["presentations"]))
    if not paper.get("ssrn"):
        extras.append("Draft available upon request.")
    extras_html = "".join(f'<p class="paper-meta">{e}</p>' for e in extras)

    return (f'<article class="paper">'
            f'<h4>{title_html}</h4>'
            f'{render_authors(paper)}'
            f'{badges and f"<p class={chr(34)}badges{chr(34)}>{badges}</p>" or ""}'
            f'{body}{extras_html}</article>')


def render_research(papers):
    out = []
    for status, heading in STATUS_GROUPS:
        group = [p for p in papers if p["status"] == status and p.get("show_on_site")]
        if group:
            out.append(f"<h3>{esc(heading)}</h3>")
            out.extend(render_paper(p) for p in group)
    unknown = {p["status"] for p in papers} - {s for s, _ in STATUS_GROUPS}
    if unknown:
        sys.exit(f"ERROR: papers.yaml has unknown status values: {unknown}")
    return "\n".join(out)


def render_teaching(t):
    rows = "".join(
        f"<tr><td>{esc(c['name'])} <span class='muted'>({esc(c['code'])})</span></td>"
        f"<td>{esc(c['term'])}</td><td>{c['students']}</td>"
        f"<td>{c['eval_mean']} / {c['eval_median']}</td></tr>"
        for c in t["courses"])
    service = "".join(f"<li>{esc(s)}</li>" for s in t.get("service", []))
    return (f'<p><strong>{esc(t["role"])}</strong>, {esc(t["period"])}. '
            f'{esc(t["eval_note"])}</p>'
            f'<div class="table-wrap"><table><thead><tr><th>Course</th><th>Term</th>'
            f'<th>Students</th><th>Eval mean / median</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            f'{service and f"<ul>{service}</ul>" or ""}')


def render_projects(projects):
    out = []
    for p in projects:
        if not p.get("show_on_site"):
            continue
        name = (f'<a href="{esc(p["url"])}">{esc(p["name"])}</a>'
                if p.get("url") else esc(p["name"]))
        out.append(f'<article class="project"><h4>{name}</h4>'
                   f'<p>{esc(p["description"].strip())}</p></article>')
    return "\n".join(out)


def render_video(profile):
    vid = profile.get("video_youtube_id")
    if not vid:
        return ""
    return (f'<div class="video"><iframe loading="lazy" '
            f'src="https://www.youtube-nocookie.com/embed/{esc(vid)}" '
            f'title="Research overview video" allowfullscreen></iframe>'
            f'<p class="muted">{esc(profile.get("video_caption", ""))}</p></div>')


def main():
    profile = load("profile", ["name", "title", "affiliation", "email", "tagline", "links"])
    papers = load("papers", ["id", "title", "authors", "status", "date", "show_on_site"])
    teaching = load("teaching", ["role", "period", "courses"])
    projects = load("projects", ["id", "name", "show_on_site", "description"])

    advisor = profile.get("advisor") or {}
    subs = {
        "name": esc(profile["name"]),
        "title": esc(profile["title"]),
        "affiliation": esc(profile["affiliation"]),
        "email": esc(profile["email"]),
        "tagline": esc(profile["tagline"].strip()),
        "job_market_line": esc(profile.get("job_market_line", "").strip()),
        "links_html": render_links(profile["links"]),
        "interests": esc(", ".join(profile.get("research_interests", []))),
        "research_html": render_research(papers),
        "teaching_html": render_teaching(teaching),
        "projects_html": render_projects(projects),
        "background": esc(profile.get("background", "").strip()),
        "advisor_html": (f'My advisor is <a href="{esc(advisor["url"])}">{esc(advisor["name"])}</a>.'
                         if advisor.get("name") else ""),
        "video_html": render_video(profile),
        "year": str(date.today().year),
        "build_date": date.today().isoformat(),
    }

    template = (ROOT / "templates" / "index.html").read_text()
    page = template
    for key, value in subs.items():
        page = page.replace("{{" + key + "}}", value)
    leftover = [t for t in page.split("{{")[1:] if "}}" in t]
    if leftover:
        sys.exit(f"ERROR: unreplaced template placeholders: {[t.split('}}')[0] for t in leftover]}")

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / "index.html").write_text(page)
    (SITE / "CNAME").write_text(DOMAIN + "\n")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>https://{DOMAIN}/</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n'
        '</urlset>\n')
    for src in (ROOT / "static").rglob("*"):
        if src.is_file():
            dest = SITE / src.relative_to(ROOT / "static")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

    n_files = sum(1 for _ in SITE.rglob("*") if _.is_file())
    print(f"Built site/ ({n_files} files). Papers shown: "
          f"{sum(1 for p in papers if p.get('show_on_site'))}. "
          f"Preview: python3 -m http.server 8000 -d site")


if __name__ == "__main__":
    main()
