from __future__ import annotations

import html
import re
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent.parent


PROJECTS = {
    "Program1": {
        "title": "Mechanisms of indoor and outdoor environmental impacts on physical and mental health",
        "cover": "/images/project-covers/population-health.svg",
        "sponsor": "National Key R&D Program of China",
        "period": "Nov 2022 - Nov 2025",
        "status": "In Progress",
        "summary": (
            "Population-scale thermal and environmental health research that connects sensing, "
            "exposure patterns, and decision support for healthier indoor and outdoor living."
        ),
        "lens": "Population health and monitoring",
    },
    "Program2": {
        "title": "Air quality assurance system for cabins of large cruise ships",
        "cover": "/images/project-covers/cruise-cabin.svg",
        "sponsor": "Ministry of Industry of China",
        "period": "Sep 2020 - Oct 2023",
        "status": "Completed",
        "summary": (
            "A cabin-environment project focused on cruise ship air quality assurance, enclosed "
            "space ventilation, and deployable control strategies for constrained interiors."
        ),
        "lens": "Cabin air quality and assurance",
    },
    "Program3": {
        "title": "Thermal environmental control strategies targeting gender differences",
        "cover": "/images/project-covers/gender-thermal.svg",
        "sponsor": "Midea Air-Conditioning Equipment Co., Ltd",
        "period": "Nov 2021 - Aug 2023",
        "status": "Completed",
        "summary": (
            "This project explores differentiated comfort zones, thermal imaging, and adaptive "
            "control strategies that account for sex-based thermal response differences."
        ),
        "lens": "Gender-aware comfort control",
    },
    "Program4": {
        "title": "Vehicle cabin thermal sensation assessment based on thermal imaging",
        "cover": "/images/project-covers/cabin-imaging.svg",
        "sponsor": "NIO Automotive Co., Ltd",
        "period": "Nov 2022 - Dec 2023",
        "status": "Completed",
        "summary": (
            "An occupant-centric vehicle cabin sensing program using infrared thermal imaging "
            "for non-contact comfort assessment and more responsive intelligent climate control."
        ),
        "lens": "Thermal imaging and smart mobility",
    },
}


PAPERS = {
    "Paper1": {
        "year": "2021",
        "kind": "Ventilation analysis",
        "focus": "Stratum ventilation and occupied-zone temperature uniformity",
    },
    "Paper2": {
        "year": "2022",
        "kind": "Thermal physiology",
        "focus": "Gender differences in thermal sensation under local cooling exposure",
    },
    "Paper3": {
        "year": "2022",
        "kind": "Air quality study",
        "focus": "Commercial cooking PM2.5 emissions and associated health effects",
    },
    "Paper4": {
        "year": "2023",
        "kind": "Behavior model",
        "focus": "Household A/C setpoint behavior across three Chinese climate zones",
    },
    "Paper5": {
        "year": "2023",
        "kind": "Sensor strategy",
        "focus": "Thermal imaging sensor placement for smart air-conditioning systems",
    },
    "Paper6": {
        "year": "2023",
        "kind": "Machine learning",
        "focus": "Sleep staging for sleep environment control based on machine learning",
    },
    "Paper7": {
        "year": "2023",
        "kind": "Comfort study",
        "focus": "Gender differences in thermal comfort under coupled environmental factors",
    },
    "Paper8": {
        "year": "2023",
        "kind": "Comfort zones",
        "focus": "Sex-based thermal comfort zones with joint fan and A/C operation",
    },
    "Paper9": {
        "year": "2023",
        "kind": "HVAC innovation",
        "focus": "Differentiated residential comfort through a dual-supply vent air conditioner",
    },
    "Paper10": {
        "year": "2023",
        "kind": "HVAC innovation",
        "focus": "Differentiated residential comfort through a novel dual-supply vent system",
    },
    "Paper11": {
        "year": "2024",
        "kind": "Perception study",
        "focus": "Thermal perception under multiple interacting factors",
    },
    "Paper12": {
        "year": "2024",
        "kind": "System design",
        "focus": "Low-cost thermal imaging system for cabin thermal sensation assessment",
    },
    "Paper13": {
        "year": "2024",
        "kind": "Experimental paper",
        "focus": "Dynamic cabin environments and synchronized occupant thermal response",
    },
    "Paper14": {
        "year": "2024",
        "kind": "Model validation",
        "focus": "Validation of a thermal imaging-based cabin sensation assessment model",
    },
    "Paper15": {
        "year": "2024",
        "kind": "Economic analysis",
        "focus": "Trade-offs between productivity and energy in urban office buildings",
    },
    "Paper16": {
        "year": "2024",
        "kind": "Critical review",
        "focus": "Subjective information in thermal comfort evaluation methods",
    },
    "Paper17": {
        "year": "2024",
        "kind": "Experimental paper",
        "focus": "Odor types, concentrations, and release frequency effects on cognition",
    },
    "Paper18": {
        "year": "2025",
        "kind": "Case study",
        "focus": "Residential cooling behavior, comfort, and energy-saving potential in Shanghai",
    },
}


FONT_LINK = (
    "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&"
    "family=IBM+Plex+Sans:wght@400;500;600;700&family=Patrick+Hand&display=swap"
)


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).strip()


def extract_title(source: str) -> str:
    marker = re.search(r'data-atelier-title="([^"]+)"', source)
    if marker:
        return html.unescape(marker.group(1))
    match = re.search(r'<h1 class="article-title[^"]*"[^>]*>\s*(.*?)\s*</h1>', source, re.S)
    if not match:
        raise ValueError("Could not extract page title")
    return clean_text(match.group(1))


def extract_body(source: str) -> str:
    preserved = re.search(
        r"<!-- atelier:body:start -->(.*?)<!-- atelier:body:end -->",
        source,
        re.S,
    )
    if preserved:
        return preserved.group(1).strip()
    legacy = re.search(
        r'<div class="article-entry" itemprop="articleBody">\s*(.*?)\s*<!-- reward -->',
        source,
        re.S,
    )
    if not legacy:
        raise ValueError("Could not extract page body")
    return legacy.group(1).strip()


def extract_authors(body: str) -> str | None:
    match = re.search(r'<h2 id="Authors".*?</h2>\s*<p>(.*?)</p>', body, re.S)
    if not match:
        return None
    return clean_text(match.group(1))


def extract_doi(body: str) -> str | None:
    match = re.search(r'href="(https://doi\.org/[^"]+)"', body)
    if match:
        return match.group(1)
    return None


def extract_pdf(body: str) -> str | None:
    match = re.search(r'var url = "([^"]+\.pdf)"', body)
    if match:
        return match.group(1)
    return None


def extract_sections(body: str) -> list[tuple[str, str]]:
    items = re.findall(r'<h2 id="([^"]+)".*?title="([^"]+)".*?</h2>', body, re.S)
    return [(anchor, clean_text(label)) for anchor, label in items]


def extract_section_block(body: str, heading_id: str) -> tuple[str | None, str]:
    pattern = re.compile(
        rf'<h2 id="{re.escape(heading_id)}".*?</h2>\s*(.*?)(?=<h2 id="|\Z)',
        re.S,
    )
    match = pattern.search(body)
    if not match:
        return None, body.strip()

    content = match.group(1).strip()
    remaining = (body[: match.start()] + body[match.end() :]).strip()
    return content, remaining


def strip_doi_paragraphs(fragment: str) -> str:
    return re.sub(
        r'\s*<p><a[^>]+href="https://doi\.org/[^"]+"[^>]*>.*?</a></p>',
        "",
        fragment,
        flags=re.S,
    ).strip()


def strip_generated_pdf_actions(fragment: str) -> str:
    return re.sub(
        r'\s*<div class="paper-pdf-actions">.*?</div>',
        "",
        fragment,
        flags=re.S,
    ).strip()


def extract_generated_card(body: str, class_name: str) -> str | None:
    if class_name == "paper-authors-card":
        pattern = (
            rf'<section class="paper-card {re.escape(class_name)}">\s*'
            r'<h2 class="paper-card-title">.*?</h2>\s*(.*?)\s*</section>\s*'
            r'<section class="paper-card">'
        )
    elif class_name == "paper-pdf-card":
        pattern = (
            rf'<section class="paper-card {re.escape(class_name)}">\s*'
            r'<h2 class="paper-card-title">.*?</h2>\s*(.*?)\s*</section>\s*</div>'
        )
    else:
        pattern = (
            rf'<section class="paper-card {re.escape(class_name)}">\s*'
            r'<h2 class="paper-card-title">.*?</h2>\s*(.*?)\s*</section>'
        )
    match = re.search(pattern, body, re.S)
    if match:
        return match.group(1).strip()
    return None


def extract_generated_notes(body: str) -> str | None:
    match = re.search(
        r'<section class="paper-card">\s*<h2 class="paper-card-title">Research notes</h2>\s*(.*?)\s*</section>\s*<section class="paper-card paper-pdf-card">',
        body,
        re.S,
    )
    if match:
        return match.group(1).strip()
    return None


def normalize_paper_source(body: str) -> tuple[str, str, str, str]:
    if 'class="paper-stack"' not in body:
        author_block, paper_body = extract_section_block(body, "Authors")
        pdf_block, paper_body = extract_section_block(paper_body, "Paper-PDF-Viewer")
        _, paper_body = extract_section_block(paper_body, "Figures")
        author_block = strip_doi_paragraphs(author_block or "")
        paper_body = strip_doi_paragraphs(paper_body)
        return author_block, paper_body, strip_generated_pdf_actions(pdf_block or ""), body

    author_block = extract_generated_card(body, "paper-authors-card") or ""
    pdf_block = strip_generated_pdf_actions(extract_generated_card(body, "paper-pdf-card") or "")
    paper_body = extract_generated_notes(body) or ""
    _, paper_body = extract_section_block(paper_body, "Figures")
    paper_body = strip_doi_paragraphs(paper_body)
    return author_block, paper_body, pdf_block, body


def topbar(active: str) -> str:
    def cls(name: str) -> str:
        return "topbar-link is-active" if active == name else "topbar-link"

    notes = {
        "home": "field notes",
        "about": "profile sketch",
        "projects": "workbench",
        "papers": "paper trail",
        "photos": "photo roll",
    }
    active_note = notes.get(active, "field notes")

    return dedent(
        f"""
        <header class="atelier-topbar" data-topbar>
          <div class="topbar-stack" data-topbar-stack>
            <div class="topbar-doodle" aria-hidden="true">
              <svg viewBox="0 0 88 72" role="presentation">
                <g class="doodle-face">
                  <path d="M24 22c4-8 10-13 20-13 12 0 18 5 20 13" />
                  <path d="M27 20l4-8 5 7 7-8 6 8 7-7 4 8" />
                  <path d="M34 42c4 5 9 7 18 7 8 0 14-2 18-7" />
                  <path d="M31 43c0 11 7 18 22 18s22-7 22-18" />
                  <path d="M25 37c-5-2-9 0-9 5s3 8 8 9" />
                  <path d="M63 51c4-1 8-4 8-9s-4-7-9-5" />
                </g>
                <g class="doodle-eyes">
                  <ellipse cx="36" cy="31" rx="2.6" ry="2.8" />
                  <ellipse cx="52" cy="31" rx="2.6" ry="2.8" />
                </g>
                <path class="doodle-spark-left" d="M14 25l-6 1 4 4-4 4 6 1" />
                <path class="doodle-curl-right" d="M74 26c4 1 6 3 7 7" />
                <path class="doodle-curl-right" d="M78 33l-2 6" />
              </svg>
            </div>
            <nav class="topbar-nav" aria-label="Primary">
              <a class="{cls('home')}" href="/" data-page-link="home" data-nav-note="field notes"><span>home</span></a>
              <a class="{cls('about')}" href="/about" data-page-link="about" data-nav-note="profile sketch"><span>about</span></a>
              <a class="{cls('projects')}" href="/categories" data-page-link="projects" data-nav-note="workbench"><span>projects</span></a>
              <a class="{cls('papers')}" href="/Paper" data-page-link="papers" data-nav-note="paper trail"><span>papers</span></a>
              <a class="{cls('photos')}" href="/photos" data-page-link="photos" data-nav-note="photo roll"><span>photos</span></a>
              <a class="topbar-link" href="https://github.com/Lyu2Patrick" target="_blank" rel="noopener" data-nav-note="say hello"><span>connect</span></a>
            </nav>
            <div class="topbar-caption" data-topbar-caption>{active_note}</div>
          </div>
        </header>
        """
    ).strip()


def rails(active: str) -> str:
    home_active = " is-active" if active == "home" else ""
    papers_active = " is-active" if active == "papers" else ""
    projects_active = " is-active" if active == "projects" else ""
    photos_active = " is-active" if active == "photos" else ""
    about_active = " is-active" if active == "about" else ""
    return dedent(
        f"""
        <div class="atelier-rail left" aria-hidden="true">
          <div class="rail-stack">
            <div class="rail-segment">
              <a class="rail-stamp{home_active}" href="/" data-page-link="home">J</a>
              <a class="rail-stamp{papers_active}" href="/Paper" data-page-link="papers"><i class="ri-book-open-line"></i></a>
              <a class="rail-stamp{projects_active}" href="/categories" data-page-link="projects"><i class="ri-flask-line"></i></a>
            </div>
            <div class="rail-segment">
              <a class="rail-stamp{photos_active}" href="/photos" data-page-link="photos"><i class="ri-camera-3-line"></i></a>
              <a class="rail-stamp{about_active}" href="/about" data-page-link="about"><i class="ri-user-smile-line"></i></a>
              <a class="rail-stamp" href="https://github.com/Lyu2Patrick" target="_blank" rel="noopener"><i class="ri-github-line"></i></a>
            </div>
          </div>
        </div>

        <div class="atelier-rail right" aria-hidden="true">
          <div class="rail-stack">
            <div class="rail-segment">
              <a class="rail-stamp" href="/Paper/Paper14/"><i class="ri-thermometer-line"></i></a>
              <a class="rail-stamp" href="/categories/Program3/"><i class="ri-settings-3-line"></i></a>
              <a class="rail-stamp" href="/photos"><i class="ri-image-line"></i></a>
            </div>
            <div class="rail-segment">
              <a class="rail-stamp" href="/Paper/Paper10/"><i class="ri-windy-line"></i></a>
              <a class="rail-stamp" href="/Paper/Paper16/"><i class="ri-file-paper-2-line"></i></a>
              <a class="rail-stamp" href="/about"><i class="ri-map-pin-line"></i></a>
            </div>
          </div>
        </div>
        """
    ).strip()


def footer() -> str:
    return dedent(
        """
        <footer class="atelier-footer">
          <span>Notebook edition inspired by editorial portfolios and hand-drawn field journals.</span>
          <span>
            <a href="/about">About</a> /
            <a href="/Paper">Papers</a> /
            <a href="/categories">Projects</a> /
            <a href="/photos">Photos</a>
          </span>
        </footer>
        """
    ).strip()


def wrap_page(
    *,
    title: str,
    description: str,
    active: str,
    hero: str,
    body: str,
    sidebar: str,
    hero_class: str = "detail-hero",
) -> str:
    safe_title = html.escape(title)
    safe_description = html.escape(description)
    return dedent(
        f"""\
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
            <meta name="description" content="{safe_description}" />
            <title>{safe_title} | Junmeng Lyu</title>
            <link rel="shortcut icon" href="/favicon.ico" />
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
            <link href="{FONT_LINK}" rel="stylesheet" />
            <link rel="stylesheet" href="/css/fonts/remixicon.css" />
            <link rel="stylesheet" href="/css/atelier.css" />
          </head>
          <body class="atelier-page detail-page" data-page="{active}">
            {rails(active)}
            {topbar(active)}
            <main class="atelier-shell">
              <section class="notebook notebook-home reveal">
                <div class="page-upper {hero_class}">
                  {hero}
                </div>
              </section>

              <section class="notebook journal-page journal-notebook reveal">
                <div class="journal-copy detail-grid">
                  <aside class="detail-sidebar reveal">
                    {sidebar}
                  </aside>
                  <article class="detail-prose" data-atelier-title="{safe_title}">
                    <!-- atelier:body:start -->
                    {body}
                    <!-- atelier:body:end -->
                  </article>
                </div>
              </section>

              {footer()}
            </main>
            <script src="/js/atelier.js"></script>
          </body>
        </html>
        """
    )


def render_project_page(path: Path) -> str:
    slug = path.parent.name
    meta = PROJECTS[slug]
    source = path.read_text(encoding="utf-8")
    body = extract_body(source)
    title = extract_title(source)
    sections = extract_sections(body)

    index_html = "".join(
        f'<li><a href="#{html.escape(anchor)}">{html.escape(label)}</a></li>'
        for anchor, label in sections
    ) or '<li><a href="#project-brief">Project brief</a></li>'

    hero = dedent(
        f"""
        <div>
          <span class="eyebrow">Project Notebook</span>
          <h1 class="hero-title detail-title">{html.escape(title)}</h1>
          <p class="hero-subtitle">{html.escape(meta['summary'])}</p>
          <div class="hero-actions">
            <a class="sketch-button primary" href="/categories">All projects</a>
            <a class="sketch-button" href="/Paper">Related papers</a>
            <a class="sketch-button" href="/about">About me</a>
          </div>
          <div class="hero-tags">
            <span>{html.escape(meta['status'])}</span>
            <span>{html.escape(meta['period'])}</span>
            <span>{html.escape(meta['lens'])}</span>
          </div>
        </div>
        <aside class="detail-aside interactive-note reveal">
          <div class="detail-cover-frame">
            <img src="{meta['cover']}" alt="{html.escape(title)} cover illustration" />
          </div>
          <div class="detail-note-heading">Project snapshot</div>
          <h2>{html.escape(meta['title'])}</h2>
          <p>{html.escape(meta['summary'])}</p>
          <div class="detail-stat-grid">
            <div><strong>Status</strong><span>{html.escape(meta['status'])}</span></div>
            <div><strong>Period</strong><span>{html.escape(meta['period'])}</span></div>
            <div><strong>Sponsor</strong><span>{html.escape(meta['sponsor'])}</span></div>
            <div><strong>Lens</strong><span>{html.escape(meta['lens'])}</span></div>
          </div>
        </aside>
        """
    ).strip()

    sidebar = dedent(
        f"""
        <section class="detail-card" id="project-brief">
          <div class="detail-card-kicker">Dossier</div>
          <dl class="detail-kv">
            <dt>Sponsor</dt>
            <dd>{html.escape(meta['sponsor'])}</dd>
            <dt>Period</dt>
            <dd>{html.escape(meta['period'])}</dd>
            <dt>Status</dt>
            <dd>{html.escape(meta['status'])}</dd>
          </dl>
        </section>
        <section class="detail-card">
          <div class="detail-card-kicker">Sections</div>
          <ol class="section-index">
            {index_html}
          </ol>
        </section>
        <section class="detail-card">
          <div class="detail-card-kicker">Elsewhere</div>
          <ol class="section-index">
            <li><a href="/categories">Return to project board</a></li>
            <li><a href="/Paper">Browse paper ledger</a></li>
            <li><a href="/photos">See the photo wall</a></li>
          </ol>
        </section>
        """
    ).strip()

    return wrap_page(
        title=title,
        description=meta["summary"],
        active="projects",
        hero=hero,
        body=body,
        sidebar=sidebar,
    )


def render_paper_page(path: Path) -> str:
    slug = path.parent.name
    meta = PAPERS[slug]
    source = path.read_text(encoding="utf-8")
    body = extract_body(source)
    title = extract_title(source)
    author_block, paper_body, pdf_block, _ = normalize_paper_source(body)
    authors = extract_authors(body)
    doi = extract_doi(body)
    pdf = extract_pdf(body)
    sections = extract_sections(paper_body)

    action_links = ['<a class="sketch-button primary" href="/Paper">All papers</a>']
    if pdf:
      action_links.append(
          f'<a class="sketch-button" href="{html.escape(pdf)}" download>Download PDF</a>'
      )

    index_html = "".join(
        f'<li><a href="#{html.escape(anchor)}">{html.escape(label)}</a></li>'
        for anchor, label in sections
    ) or '<li><a href="/Paper">Return to paper ledger</a></li>'

    doi_line = ""
    if doi:
        doi_line = (
            f'<p class="paper-doi-line"><span>DOI page</span>'
            f'<a href="{html.escape(doi)}" target="_blank" rel="noopener">{html.escape(doi)}</a></p>'
        )

    hero = dedent(
        f"""
        <div>
          <span class="eyebrow">Paper Note • {html.escape(meta['year'])}</span>
          <h1 class="hero-title detail-title">{html.escape(title)}</h1>
          {doi_line}
          <p class="hero-subtitle">{html.escape(meta['focus'])}</p>
          <div class="hero-actions">
            {' '.join(action_links)}
          </div>
          <div class="hero-tags">
            <span>{html.escape(meta['kind'])}</span>
            <span>Thermal comfort research</span>
            <span>Notebook entry {html.escape(slug.replace('Paper', '#'))}</span>
          </div>
        </div>
        """
    ).strip()

    pdf_section = ""
    if pdf:
        pdf_section = f"""
        <dt>PDF</dt>
        <dd><a class="inline-link" href="{html.escape(pdf)}" download>Download manuscript</a></dd>
        """

    sidebar = dedent(
        f"""
        <section class="detail-card">
          <div class="detail-card-kicker">Index Card</div>
          <dl class="detail-kv">
            <dt>Year</dt>
            <dd>{html.escape(meta['year'])}</dd>
            <dt>Lens</dt>
            <dd>{html.escape(meta['kind'])}</dd>
            <dt>Focus</dt>
            <dd>{html.escape(meta['focus'])}</dd>
            {pdf_section}
        </dl>
        </section>
        <section class="detail-card">
          <div class="detail-card-kicker">Sections</div>
          <ol class="section-index">
            {index_html}
          </ol>
        </section>
        <section class="detail-card">
          <div class="detail-card-kicker">Browse</div>
          <ol class="section-index">
            <li><a href="/Paper">Return to paper ledger</a></li>
            <li><a href="/categories">Open project board</a></li>
            <li><a href="/about">Research profile</a></li>
          </ol>
        </section>
        """
    ).strip()

    authors_panel = ""
    if author_block:
        authors_panel = dedent(
            f"""
            <section class="paper-card paper-authors-card">
              <h2 class="paper-card-title">Authors &amp; affiliations</h2>
              {author_block}
            </section>
            """
        ).strip()

    notes_panel = dedent(
        f"""
        <section class="paper-card">
          <h2 class="paper-card-title">Research notes</h2>
          {paper_body}
        </section>
        """
    ).strip()

    pdf_panel = ""
    if pdf_block:
        download_button = ""
        if pdf:
            download_button = (
                f'<div class="paper-pdf-actions"><a class="sketch-button primary" '
                f'href="{html.escape(pdf)}" download>Download PDF</a></div>'
            )
        pdf_panel = dedent(
            f"""
            <section class="paper-card paper-pdf-card">
              <h2 class="paper-card-title">PDF reader</h2>
              {download_button}
              {pdf_block}
            </section>
            """
        ).strip()

    body = dedent(
        f"""
        <div class="paper-stack">
          {authors_panel}
          {notes_panel}
          {pdf_panel}
        </div>
        """
    ).strip()

    return wrap_page(
        title=title,
        description=meta["focus"],
        active="papers",
        hero=hero,
        body=body,
        sidebar=sidebar,
        hero_class="detail-hero detail-hero-single",
    )


def render_about_page() -> str:
    about_title = "About Me"
    about_description = (
        "Notebook-style profile page for Junmeng Lyu covering research, education, awards, "
        "projects, publications, and life outside the lab."
    )
    hero = dedent(
        """
        <div>
          <span class="eyebrow">About • Research Profile</span>
          <h1 class="hero-title detail-title">Research, systems, and field notes from real environments.</h1>
          <p class="hero-subtitle">
            I am Junmeng Lyu, a PhD researcher working on thermal comfort, thermal imaging,
            occupant-centered sensing, and intelligent HVAC control. My work sits between
            controlled experiments, machine learning, and the everyday environments people
            actually live in.
          </p>
          <div class="hero-actions">
            <a class="sketch-button primary" href="/Paper">Read papers</a>
            <a class="sketch-button" href="/categories">Open projects</a>
            <a class="sketch-button" href="/photos">Photo wall</a>
          </div>
          <div class="hero-tags">
            <span>Shanghai Jiao Tong University</span>
            <span>Thermal comfort</span>
            <span>Smart HVAC</span>
            <span>Photography</span>
          </div>
        </div>
        <aside class="detail-aside interactive-note reveal">
          <div class="portrait-frame">
            <img src="/pic.png" alt="Portrait of Junmeng Lyu" />
            <div>
              <div class="detail-note-heading">Current notebook</div>
              <h2>Occupant-centered environmental intelligence</h2>
              <p>
                I like translating sensed human response into models and control logic that
                stay useful outside the lab, especially in cabins, homes, and shared indoor environments.
              </p>
            </div>
          </div>
          <div class="inline-stat-strip">
            <span>18 paper pages</span>
            <span>4 funded projects</span>
            <span>Best Paper Award 2023</span>
          </div>
        </aside>
        """
    ).strip()

    body = dedent(
        """
        <div class="about-columns">
          <section class="about-card">
            <div class="about-card-kicker">Education</div>
            <h2>Training across building environment and architecture</h2>
            <ol class="about-list">
              <li>Shanghai Jiao Tong University, PhD student in Architecture, September 2021 - present.</li>
              <li>Chongqing University, BEng in Building Environment and Energy Application Engineering, June 2021.</li>
            </ol>
          </section>

          <section class="about-card">
            <div class="about-card-kicker">Research Lens</div>
            <h2>What I keep returning to</h2>
            <ol class="about-list">
              <li>Occupant-centered thermal comfort assessment in dynamic indoor and cabin environments.</li>
              <li>Thermal imaging and low-cost sensing for non-contact comfort evaluation.</li>
              <li>Machine learning models that can support intelligent HVAC control decisions.</li>
              <li>Environmental health links between exposure, behavior, and physical or mental outcomes.</li>
            </ol>
          </section>

          <section class="about-card">
            <div class="about-card-kicker">Selected Honors</div>
            <h2>Awards and recognition</h2>
            <ol class="award-list">
              <li>Outstanding Graduate Student Scholarship, Shanghai Jiao Tong University, 2023.</li>
              <li>Best Paper Award, Healthy Buildings Asia Conference, 2023.</li>
              <li>First-class academic scholarship, Shanghai Jiao Tong University, 2022 and 2021.</li>
              <li>Outstanding graduation design, Chongqing University, 2021.</li>
              <li>Province-level science and technology innovation prize, Chongqing, 2021.</li>
              <li>National silver medal, 3rd National college students' advanced technology and product information modeling innovation competition, 2018.</li>
            </ol>
          </section>

          <section class="about-card">
            <div class="about-card-kicker">Leadership</div>
            <h2>Work beyond the lab</h2>
            <ol class="about-list">
              <li>Chairman of the Graduate Student Association, School of Design, Shanghai Jiao Tong University, since May 2022.</li>
              <li>Long-term interest in photography, running, and documenting atmosphere through field images.</li>
              <li>Comfortable working with Python, Origin, Photoshop, AutoCAD, Revit, Zotero, and Office workflows.</li>
            </ol>
            <div class="interest-tags">
              <span>Python</span>
              <span>Origin</span>
              <span>AutoCAD</span>
              <span>Revit</span>
              <span>Zotero</span>
              <span>Photography</span>
              <span>Running</span>
            </div>
          </section>
        </div>

        <section class="about-card" style="margin-top:1.35rem;">
          <div class="about-card-kicker">Research Programs</div>
          <h2>Funded threads and applied collaborations</h2>
          <ol class="about-list">
            <li>National Key R&D Program of China: mechanisms of indoor and outdoor environmental impacts on physical and mental health, 2022-2025.</li>
            <li>Ministry of Industry of China: air quality assurance system for large cruise ship cabins, 2020-2023.</li>
            <li>Midea collaboration: thermal imaging models, differentiated comfort zones, and data-driven comfort control, 2021-2023.</li>
            <li>NIO collaboration: vehicle cabin thermal sensation assessment based on thermal imaging, 2022-2023.</li>
          </ol>
        </section>

        <section class="journal-panels" style="margin-top:1.35rem;">
          <article class="journal-panel">
            <div class="panel-kicker">Projects</div>
            <h2 class="panel-title">Current research threads</h2>
            <div class="compact-projects" data-render="projects-compact"></div>
          </article>
          <article class="journal-panel">
            <div class="panel-kicker">Papers</div>
            <h2 class="panel-title">Recent paper notes</h2>
            <div class="compact-papers" data-render="papers-compact"></div>
          </article>
          <article class="journal-panel">
            <div class="panel-kicker">Photos</div>
            <h2 class="panel-title">Notebook beyond research</h2>
            <div class="compact-photos" data-render="photos-compact"></div>
          </article>
        </section>
        """
    ).strip()

    sidebar = dedent(
        """
        <section class="detail-card">
          <div class="detail-card-kicker">Profile</div>
          <dl class="detail-kv">
            <dt>Role</dt>
            <dd>PhD researcher in architecture and thermal environment studies</dd>
            <dt>Base</dt>
            <dd>Shanghai Jiao Tong University, Shanghai, China</dd>
            <dt>Focus</dt>
            <dd>Thermal comfort, smart control, sensing, and environmental health</dd>
          </dl>
        </section>
        <section class="detail-card">
          <div class="detail-card-kicker">Jump To</div>
          <ol class="section-index">
            <li><a href="/Paper">Paper ledger</a></li>
            <li><a href="/categories">Project board</a></li>
            <li><a href="/photos">Photo wall</a></li>
            <li><a href="https://github.com/Lyu2Patrick" target="_blank" rel="noopener">GitHub</a></li>
          </ol>
        </section>
        <section class="detail-card">
          <div class="detail-card-kicker">In Short</div>
          <p>
            This page keeps the long CV energy but turns it into a cleaner notebook profile:
            clearer research themes, selected honors, and the links that matter most for browsing.
          </p>
        </section>
        """
    ).strip()

    return wrap_page(
        title=about_title,
        description=about_description,
        active="about",
        hero=hero,
        body=body,
        sidebar=sidebar,
    )


def main() -> None:
    for page in sorted((ROOT / "categories").glob("Program*/index.html")):
        page.write_text(render_project_page(page), encoding="utf-8")

    for page in sorted((ROOT / "Paper").glob("Paper*/index.html")):
        page.write_text(render_paper_page(page), encoding="utf-8")

    (ROOT / "about" / "index.html").write_text(render_about_page(), encoding="utf-8")


if __name__ == "__main__":
    main()
