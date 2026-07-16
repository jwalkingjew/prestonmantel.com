#!/usr/bin/env python3
"""Build prestonmantel.com from canonical YAML data."""

import html
import json
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DOMAIN = "prestonmantel.com"

PAGES = [
    ("home", "Home", "index.html"),
    ("research", "Research", "research.html"),
    ("teaching", "Teaching", "teaching.html"),
    ("tools", "Tools", "tools.html"),
    ("about", "About", "about.html"),
]

STATUS_GROUPS = [
    ("job_market_paper", "Job Market Paper"),
    ("under_review", "Under Review"),
    ("working", "Working Papers"),
]

STATUS_LABELS = {
    "job_market_paper": "Job Market Paper",
    "under_review": "Under Review",
    "working": "Working Paper",
}


def esc(value):
    return html.escape(str(value), quote=True)


def load(name, required):
    path = ROOT / "data" / f"{name}.yaml"
    data = yaml.safe_load(path.read_text())
    items = data if isinstance(data, list) else [data]
    for item in items:
        for key in required:
            if key not in item:
                sys.exit(f"ERROR: {path.name}: entry missing '{key}': {item}")
    return data


def anchor(url, label, class_name=""):
    attrs = f' class="{esc(class_name)}"' if class_name else ""
    external = str(url).startswith(("http://", "https://"))
    rel = ' rel="noopener"' if external else ""
    return f'<a href="{esc(url)}"{attrs}{rel}>{esc(label)}</a>'


def render_nav(active):
    links = []
    for page_id, label, filename in PAGES:
        current = ' aria-current="page" class="active"' if page_id == active else ""
        links.append(f'<a href="{filename}"{current}>{label}</a>')
    return "".join(links)


def render_profile_links(profile, button=False):
    links = [(item["label"], item.get("url")) for item in profile["links"] if item.get("url")]
    links.insert(0, ("Email", f'mailto:{profile["email"]}'))
    cls = "button button-secondary" if button else ""
    return "".join(anchor(url, label, cls) for label, url in links)


def render_authors(paper):
    others = [author for author in paper["authors"] if author != "Preston Mantel"]
    if not others:
        return '<p class="paper-authors">Preston Mantel</p>'
    affiliations = paper.get("author_affiliations") or {}
    names = [f'{esc(name)} <span>({esc(affiliations[name])})</span>' if name in affiliations else esc(name)
             for name in others]
    joined = " and ".join(names) if len(names) < 3 else ", ".join(names[:-1]) + ", and " + names[-1]
    return f'<p class="paper-authors">Preston Mantel with {joined}</p>'


def render_badges(paper):
    badges = [f'<span class="label">{esc(STATUS_LABELS[paper["status"]])}</span>']
    badges.extend(f'<span class="label label-muted">{esc(award)}</span>' for award in paper.get("awards", []))
    for media in paper.get("media", []):
        text = f'Media: {media["outlet"]}'
        badges.append(anchor(media["url"], text, "label label-muted") if media.get("url")
                      else f'<span class="label label-muted">{esc(text)}</span>')
    return '<div class="paper-labels">' + "".join(badges) + "</div>"


def paper_url(paper):
    if paper.get("ssrn"):
        return f'https://papers.ssrn.com/sol3/papers.cfm?abstract_id={paper["ssrn"]}'
    return ""


def render_abstract(paper):
    if not paper.get("abstract") or not paper.get("abstract_verified"):
        return ""
    source = paper.get("abstract_source")
    source_html = f'<p class="source-note">Source: {esc(source)}. Updated {esc(paper["abstract_verified"])}.</p>' if source else ""
    return (
        '<details class="abstract">'
        '<summary>Read abstract</summary>'
        f'<div class="abstract-copy"><p>{esc(paper["abstract"])}</p>{source_html}</div>'
        '</details>'
    )


def render_paper(paper, number):
    url = paper_url(paper)
    title = anchor(url, paper["title"]) if url else esc(paper["title"])
    points = "".join(f'<li>{esc(point)}</li>' for point in paper.get("bullets", []))
    actions = []
    if url:
        actions.append(anchor(url, "View paper", "text-link"))
    else:
        actions.append('<span class="availability">Draft available upon request</span>')
    presentations = ""
    if paper.get("presentations"):
        items = "".join(f'<li>{esc(item)}</li>' for item in paper["presentations"])
        presentations = f'<details class="presentations"><summary>Presentations</summary><ul>{items}</ul></details>'
    return (
        f'<article class="paper-card" id="{esc(paper["id"])}">'
        f'<div class="paper-number">{number:02d}</div>'
        '<div class="paper-content">'
        f'{render_badges(paper)}<h2>{title}</h2>{render_authors(paper)}'
        f'<ul class="paper-points">{points}</ul>'
        f'<div class="paper-actions">{"".join(actions)}</div>'
        f'{render_abstract(paper)}{presentations}'
        '</div></article>'
    )


def render_featured_paper(paper):
    url = paper_url(paper)
    points = "".join(f'<li>{esc(point)}</li>' for point in paper.get("bullets", [])[:2])
    primary = anchor(url, "Read on SSRN", "button button-light") if url else ""
    return (
        '<section class="featured-paper" aria-labelledby="featured-title">'
        '<div class="featured-index"><span>01</span><span>Featured Research</span></div>'
        '<div class="featured-main">'
        '<p class="eyebrow eyebrow-light">Job Market Paper</p>'
        f'<h2 id="featured-title">{esc(paper.get("short_title", paper["title"]))}</h2>'
        f'<p class="featured-full-title">{esc(paper["title"])}</p>'
        f'<ul>{points}</ul>'
        f'<div class="featured-actions">{primary}{anchor("research.html#" + paper["id"], "Research details", "button button-outline-light")}</div>'
        '</div></section>'
    )


def render_home(profile, papers):
    featured = next(paper for paper in papers if paper["status"] == "job_market_paper" and paper.get("show_on_site"))
    return (
        '<section class="home-hero">'
        '<div class="hero-copy">'
        f'<p class="eyebrow">{esc(profile["hero_eyebrow"])}</p>'
        f'<h1>{esc(profile["hero_headline"])}</h1>'
        f'<p class="hero-intro">{esc(profile["hero_intro"])}</p>'
        f'<p class="job-market-line">{esc(profile["job_market_line"])}</p>'
        '<div class="hero-actions">'
        f'{anchor("research.html", "Explore my research", "button button-primary")}'
        f'{anchor("files/Mantel_CV.pdf", "Download CV", "button button-secondary")}'
        '</div></div>'
        '<aside class="hero-profile">'
        f'<div class="portrait-frame"><img src="img/headshot.jpg" alt="Portrait of {esc(profile["name"])}" width="640" height="800"></div>'
        '<div class="profile-caption">'
        f'<strong>{esc(profile["name"])}</strong>'
        f'<span>{esc(profile["title"])}</span>'
        '<span>University of Cincinnati</span>'
        '</div></aside></section>'
        '<section class="engineering-bridge" aria-label="Research perspective">'
        '<p>Engineering asks how systems behave under constraints.</p>'
        '<span aria-hidden="true">+</span>'
        '<p>Finance asks how people and capital respond to incentives.</p>'
        '<span aria-hidden="true">=</span>'
        '<p>Market microstructure studies both.</p>'
        '</section>'
        f'{render_featured_paper(featured)}'
        '<section class="research-lenses">'
        '<div class="section-heading"><p class="eyebrow">Research Lens</p><h2>How I approach markets</h2></div>'
        '<div class="lens-grid">'
        '<article><span>01</span><h3>System design</h3><p>Rules, order types, and trading mechanisms determine what a market makes possible.</p></article>'
        '<article><span>02</span><h3>Measured outcomes</h3><p>Market data reveals whether a design works as intended and who ultimately benefits.</p></article>'
        '<article><span>03</span><h3>Investor impact</h3><p>The practical test is how market structure changes execution, liquidity, and trading costs.</p></article>'
        '</div></section>'
    )


def render_research(profile, papers):
    visible = [paper for paper in papers if paper.get("show_on_site")]
    groups = []
    number = 1
    for status, heading in STATUS_GROUPS:
        group = [paper for paper in visible if paper["status"] == status]
        if not group:
            continue
        cards = []
        for paper in group:
            cards.append(render_paper(paper, number))
            number += 1
        groups.append(f'<section class="paper-group"><h2 class="group-title">{heading}</h2>{"".join(cards)}</section>')
    interests = "".join(f'<li>{esc(item)}</li>' for item in profile.get("research_interests", []))
    return (
        '<header class="page-hero"><p class="eyebrow">Research</p><h1>Markets as designed systems</h1>'
        '<p>I study how trading rules and market mechanisms shape liquidity, price discovery, and investor outcomes.</p></header>'
        f'<ul class="interest-list" aria-label="Research interests">{interests}</ul>'
        f'{"".join(groups)}'
    )


def render_teaching(teaching):
    rows = "".join(
        '<tr>'
        f'<th scope="row"><strong>{esc(course["name"])}</strong><span>{esc(course["code"])}</span></th>'
        f'<td>{esc(course["term"])}</td><td>{esc(course["students"])}</td>'
        f'<td>{esc(course["eval_mean"])}</td><td>{esc(course["eval_median"])}</td>'
        '</tr>' for course in teaching["courses"]
    )
    service = "".join(f'<li>{esc(item)}</li>' for item in teaching.get("service", []))
    return (
        '<header class="page-hero"><p class="eyebrow">Teaching</p><h1>Clear models, practical decisions</h1>'
        '<p>I teach finance by connecting analytical tools to the choices people make in real markets.</p></header>'
        '<section class="teaching-overview">'
        '<div><p class="eyebrow">Role</p>'
        f'<h2>{esc(teaching["role"])}</h2><p>{esc(teaching["period"])}</p></div>'
        '<div class="evaluation-note"><strong>8-point scale</strong>'
        f'<p>{esc(teaching["eval_note"])}</p></div></section>'
        '<section class="table-section"><div class="section-heading"><p class="eyebrow">Course Record</p><h2>Instructor evaluations</h2></div>'
        '<div class="table-wrap"><table><thead><tr><th scope="col">Course</th><th scope="col">Term</th>'
        '<th scope="col">Students</th><th scope="col">Mean</th><th scope="col">Median</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div></section>'
        f'<section class="service"><p class="eyebrow">Service &amp; Mentorship</p><ul>{service}</ul></section>'
    )


def render_tools(projects):
    cards = []
    for project in projects:
        if not project.get("show_on_site"):
            continue
        action = anchor(project["url"], f'Visit {project["name"]}', "button button-primary") if project.get("url") else ""
        cards.append(
            '<article class="tool-card">'
            '<div class="tool-mark" aria-hidden="true">PT</div>'
            '<div><p class="eyebrow">Built for educators</p>'
            f'<h2>{esc(project["name"])}</h2><p>{esc(project["description"].strip())}</p>{action}</div>'
            '</article>'
        )
    return (
        '<header class="page-hero"><p class="eyebrow">Tools</p><h1>Useful systems, built from experience</h1>'
        '<p>I build tools when a recurring problem in teaching or research calls for a better workflow.</p></header>'
        f'<section class="tools-list">{"".join(cards)}</section>'
    )


def render_video(profile):
    video_id = profile.get("video_youtube_id")
    if not video_id:
        return ""
    return (
        '<section class="video-section"><div class="section-heading"><p class="eyebrow">Research Overview</p>'
        '<h2>Why market design matters</h2></div>'
        '<div class="video-frame"><iframe loading="lazy" '
        f'src="https://www.youtube-nocookie.com/embed/{esc(video_id)}" '
        'title="Preston Mantel research overview" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
        'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
        f'<p class="caption">{esc(profile.get("video_caption", ""))}</p></section>'
    )


def render_about(profile):
    advisor = profile.get("advisor") or {}
    advisor_html = anchor(advisor["url"], advisor["name"]) if advisor.get("url") else esc(advisor.get("name", ""))
    interests = "".join(f'<li>{esc(item)}</li>' for item in profile.get("research_interests", []))
    return (
        '<header class="page-hero about-hero"><p class="eyebrow">About</p><h1>From mechanical systems to financial markets</h1>'
        '<p>Engineering gave me a way to think about constraints, feedback, and system performance. Finance gave me a new class of systems to study.</p></header>'
        '<section class="about-grid"><div class="about-copy"><h2>Background</h2>'
        f'<p>{esc(profile["background"])}</p><p>My advisor is {advisor_html}.</p></div>'
        '<aside><img src="img/headshot.jpg" alt="Preston Mantel" width="640" height="800"></aside></section>'
        '<section class="path-grid">'
        '<article><p class="eyebrow">Engineering</p><h2>Purdue University</h2><p>B.S. in Mechanical Engineering with minors in Computer Science and Global Engineering Studies.</p></article>'
        '<article><p class="eyebrow">Finance</p><h2>University of Cincinnati</h2><p>Ph.D. Candidate studying market microstructure, retail investor protection, and market regulation.</p></article>'
        '</section>'
        f'<section class="interest-section"><p class="eyebrow">Research Interests</p><ul class="interest-list">{interests}</ul></section>'
        f'{render_video(profile)}'
    )


def structured_data(profile):
    same_as = [item["url"] for item in profile["links"] if item.get("url") and item["url"].startswith("http")]
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Person",
        "name": profile["name"],
        "url": f"https://{DOMAIN}/",
        "image": f"https://{DOMAIN}/img/headshot.jpg",
        "jobTitle": profile["title"],
        "affiliation": {"@type": "CollegeOrUniversity", "name": "University of Cincinnati"},
        "sameAs": same_as,
    }, ensure_ascii=False)


def render_page(template, profile, page_id, title, description, content):
    filename = next(filename for candidate, _, filename in PAGES if candidate == page_id)
    canonical = f'https://{DOMAIN}/' if filename == "index.html" else f'https://{DOMAIN}/{filename}'
    replacements = {
        "page_title": esc(title),
        "description": esc(description),
        "canonical": esc(canonical),
        "name": esc(profile["name"]),
        "nav_html": render_nav(page_id),
        "profile_links_html": render_profile_links(profile),
        "content_html": content,
        "page_id": esc(page_id),
        "year": str(date.today().year),
        "structured_data": structured_data(profile),
    }
    page = template
    for key, value in replacements.items():
        page = page.replace("{{" + key + "}}", value)
    leftover = [part.split("}}")[0] for part in page.split("{{")[1:] if "}}" in part]
    if leftover:
        sys.exit(f"ERROR: unreplaced template placeholders: {leftover}")
    return page


def ensure_no_em_dashes():
    failures = []
    for path in SITE.rglob("*"):
        if path.suffix.lower() not in {".html", ".css", ".js", ".xml", ".txt"}:
            continue
        if "\u2014" in path.read_text():
            failures.append(str(path.relative_to(SITE)))
    if failures:
        sys.exit(f"ERROR: em dash found in generated site files: {failures}")


def main():
    profile = load("profile", ["name", "title", "affiliation", "email", "hero_headline", "links"])
    papers = load("papers", ["id", "title", "authors", "status", "date", "show_on_site"])
    teaching = load("teaching", ["role", "period", "courses"])
    projects = load("projects", ["id", "name", "show_on_site", "description"])

    unknown = {paper["status"] for paper in papers} - set(STATUS_LABELS)
    if unknown:
        sys.exit(f"ERROR: unknown paper status values: {unknown}")

    page_content = {
        "home": (f'{profile["name"]} | Finance Researcher', profile["tagline"], render_home(profile, papers)),
        "research": (f'Research | {profile["name"]}', 'Research on market microstructure, market design, retail trading, and liquidity.', render_research(profile, papers)),
        "teaching": (f'Teaching | {profile["name"]}', 'Teaching experience and instructor evaluations at the University of Cincinnati.', render_teaching(teaching)),
        "tools": (f'Tools | {profile["name"]}', 'Research and teaching tools built by Preston Mantel.', render_tools(projects)),
        "about": (f'About | {profile["name"]}', 'Background, education, and research perspective of Preston Mantel.', render_about(profile)),
    }

    template = (ROOT / "templates" / "index.html").read_text()
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()

    for page_id, _, filename in PAGES:
        title, description, content = page_content[page_id]
        (SITE / filename).write_text(render_page(template, profile, page_id, title, description, content))

    (SITE / "CNAME").write_text(DOMAIN + "\n")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    urls = "\n".join(
        f'  <url><loc>https://{DOMAIN}/{"" if filename == "index.html" else filename}</loc><lastmod>{date.today().isoformat()}</lastmod></url>'
        for _, _, filename in PAGES
    )
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{urls}\n</urlset>\n'
    )
    for source in (ROOT / "static").rglob("*"):
        if source.is_file():
            destination = SITE / source.relative_to(ROOT / "static")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    ensure_no_em_dashes()
    print(f"Built {len(PAGES)} pages in site/. Papers shown: {sum(1 for paper in papers if paper.get('show_on_site'))}.")


if __name__ == "__main__":
    main()
