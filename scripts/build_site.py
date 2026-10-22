"""Build the public academic homepage from content/*.json. Standard library only."""
from datetime import date, datetime
from html import escape
from html.parser import HTMLParser
import json
import re
from pathlib import Path
import shutil
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist"


def text(value):
    return escape(str(value), quote=True)


def read_json(name):
    raw = (ROOT / "content" / f"{name}.json").read_text(encoding="utf-8")
    # Accept editorial comments while preserving URL/string contents verbatim.
    raw = re.sub(r'("(?:\\.|[^"\\])*")|//[^\r\n]*|/\*[\s\S]*?\*/',
                 lambda match: match.group(1) or "", raw)
    return json.loads(raw)


def icon(name, size=17):
    paths = {
        "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
        "github": '<path d="m8 7-5 5 5 5m8-10 5 5-5 5m-3-14-2 18"/>',
        "modelscope": '<path d="m12 3 9 5-9 5-9-5 9-5Zm-9 9 9 5 9-5M3 16l9 5 9-5"/>',
        "external": '<path d="M14 4h6v6m0-6-9 9M10 4H5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-5"/>',
        "zoom": '<path d="M9 3H3v6m12-6h6v6M3 15v6h6m12-6v6h-6"/>',
        "location": '<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2"/>',
        "about": '<circle cx="12" cy="7" r="4"/><path d="M4 21v-2a8 8 0 0 1 16 0v2"/>',
        "publications": '<path d="M4 3h11l5 5v13H4V3Zm11 0v6h5M8 13h8M8 17h6"/>',
        "open-source": '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18"/>',
        "experience": '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12l9 4 9-4m-9 4v3"/>',
        "education": '<path d="m2 9 10-6 10 6-10 6L2 9Zm4 3v6c4 3 8 3 12 0v-6m4-3v9"/>',
        "honors": '<circle cx="12" cy="8" r="5"/><path d="m8 12-2 10 6-3 6 3-2-10"/>',
        "beyond": '<path d="M9 18V5l12-2v13M9 9l12-2"/><ellipse cx="6" cy="18" rx="3" ry="3"/><ellipse cx="18" cy="16" rx="3" ry="3"/>'
    }
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def link(url, label, css="", arrow=False):
    parsed = urlparse(url)
    if parsed.scheme not in {"https", "http", "mailto"}:
        raise ValueError(f"Unsupported link scheme: {url}")
    external = ' target="_blank" rel="noopener noreferrer"' if parsed.scheme != "mailto" else ""
    css_attr = f' class="{css}"' if css else ""
    return f'<a href="{text(url)}"{css_attr}{external}>{label}{icon("external", 13) if arrow else ""}</a>'


def human_date(value):
    if not value:
        return "Present"
    if len(value) == 4:
        return value
    return datetime.strptime(value[:7], "%Y-%m").strftime("%b %Y")


def profile_html(profile):
    contacts = [
        link("mailto:" + profile["email"], icon("email") + "<span>" + text(profile["email"]) + "</span>", "email-link"),
        link(profile["links"]["github"], icon("github") + "<span>GitHub</span>"),
        link(profile["links"]["modelscope"], icon("modelscope") + "<span>ModelScope</span>")
    ]
    for key, label in [("google_scholar", "Google Scholar"), ("orcid", "ORCID"), ("cv", "CV")]:
        if profile["links"].get(key):
            contacts.append(link(profile["links"][key], icon("external") + f"<span>{label}</span>"))
    bio = ''.join('<p>' + text(sentence) + '</p>' for sentence in profile['sidebar_bio'])
    return f'''<aside class="profile" aria-label="Profile and contact details">
      <img class="profile-photo" src="{text(profile['portrait']['path'])}" alt="{text(profile['portrait']['alt'])}" width="216" height="252" fetchpriority="high">
      <h1 class="profile-name">{text(profile['name']['en'])}<span class="profile-name-zh" lang="zh-CN">{text(profile['name']['zh'])}</span></h1>
      <div class="profile-bio">{bio}</div>
      <p class="profile-location">{icon('location', 16)}<span>{text(profile['location'])}</span></p>
      <ul class="profile-links">{''.join('<li>' + c + '</li>' for c in contacts)}</ul>
      <div class="profile-interests"><h2>Research interests</h2><p>{'<br>'.join(text(x) for x in profile['research_interests'])}</p></div>
    </aside>'''


def publications_html(publications):
    rows = []
    for paper in publications["items"]:
        if not paper.get("visible", True):
            continue
        title = text(paper["title"])
        title_link = link(paper["links"]["paper"], title) if paper["links"].get("paper") else title
        authors = ""
        if paper.get("authors") and paper.get("display_authors", True):
            rendered = []
            for author in paper["authors"]:
                value = text(author)
                if author == publications["author_highlight"]:
                    value = f"<strong>{value}</strong>"
                if author in (paper.get("equal_contribution_authors") or []):
                    value += '<sup title="Equal contribution">*</sup>'
                if author in (paper.get("corresponding_authors") or []):
                    value += '<sup title="Corresponding author">†</sup>'
                rendered.append(value)
            authors = '<p class="publication-authors">' + ", ".join(rendered) + "</p>"
        resources = []
        for key, label in [("paper", "Paper"), ("pdf", "PDF"), ("dataset", "Dataset"), ("code", "Code")]:
            if paper["links"].get(key):
                resources.append(link(paper["links"][key], label, arrow=True))
        links = '<div class="publication-links">' + "".join(resources) + "</div>" if resources else ""
        image = paper.get("image")
        is_review = " is-review" if paper["status"] not in {"published", "accepted"} else ""
        summary = '<p class="publication-summary">' + text(paper['summary']) + '</p>' if paper.get('summary') else ''
        short_title = paper.get("short_title", paper["id"])
        figure = f'''<a class="publication-figure" href="{text(image['path'])}" data-figure-title="{text(short_title)} · Figure {text(image.get('figure', ''))}" aria-label="Enlarge {text(short_title)} framework figure">
            <img src="{text(image['path'])}" alt="{text(image['alt'])}" loading="lazy" width="200" height="140">
            <span class="figure-zoom">{icon('zoom', 14)}</span>
          </a>''' if image else ""
        rows.append(f'''<article class="publication{' publication-text-only' if not image else ''}" id="paper-{text(paper['id'])}">
          {figure}
          <div class="publication-content"><h3>{title_link}</h3>{authors}<p class="publication-venue{is_review}">{text(paper['status_label'])}</p>{summary}{links}</div>
        </article>''')
    return "\n".join(rows)


def open_source_html(profile, metrics):
    return "".join(project_html(project, metrics) for project in profile["projects"] if project.get("visible", True))


def project_html(project, metrics):
    banner = project.get('banner')
    banner_html = f'<img class="project-banner" src="{text(banner["path"])}" alt="{text(banner["alt"])}" width="{banner["width"]}" height="{banner["height"]}" loading="lazy">' if banner else ''
    inventory = project.get("inventory")
    inventory_html = f'<p class="resource-inventory">{inventory["tropical_cyclone_events"]:,} tropical-cyclone events · {inventory["sar_scenes"]:,} SAR scenes · Event-based, traceable records</p>' if inventory else ""
    resources = "".join(link(project["links"][key], label, "resource-link", arrow=True) for key, label in [("dataset", "ModelScope dataset"), ("studio", "Explore the Studio"), ("zenodo", "Zenodo archive"), ("code", "Code"), ("paper", "Paper")] if project["links"].get(key))
    counters = {item["id"]: item for item in metrics["items"]}
    downloads = counters["modelscope-dataset-downloads"]
    visits = counters["modelscope-studio-visits"]
    count_line = link(downloads["url"], f'<strong data-metric-id="modelscope-dataset-downloads">{downloads["value"]:,}</strong> dataset downloads') + " · " + link(visits["url"], f'<strong data-metric-id="modelscope-studio-visits">{visits["value"]:,}</strong> Studio visits') if set(project.get("metric_ids", [])) == {downloads["id"], visits["id"]} else ""
    count_html = '<p class="resource-metrics">' + count_line + '</p>' if count_line else ""
    return f'''<div class="resource">
      <h3>{text(project['subtitle'])}</h3>
      {banner_html}
      <p>{text(project['summary'])}</p>
      {inventory_html}
      <div class="resource-links">{resources}</div>
      {count_html}
    </div>'''


def record_logo(item):
    logo = item.get('logo')
    return f'<img class="record-logo" src="{text(logo["path"])}" alt="{text(logo["alt"])}" width="56" height="56" loading="lazy">' if logo else ''


def experience_html(profile):
    rows = []
    for experience in profile["research_experience"]:
        if not experience.get("visible", True):
            continue
        period = human_date(experience["start"]) + " – " + human_date(experience["end"])
        group = link(experience["group_url"], text(experience["group"])) if experience.get("group_url") else text(experience["group"])
        rows.append(f'''<article class="record"><div class="record-heading">{record_logo(experience)}<div><h3>{text(experience['institution'])}</h3><p class="record-subtitle">{text(experience['role'])} · {group}</p></div></div><time datetime="{text(experience['start'])}">{period}</time><p class="record-detail">{text(experience['supervision'])} · Prof. {text(experience['lab_lead'])}'s lab<br>{text(experience['summary'])}</p></article>''')
    return "\n".join(rows)


def education_html(profile):
    rows = []
    for education in profile["education"]:
        if not education.get("visible", True):
            continue
        incoming = education["status"] == "incoming"
        period = "From " + human_date(education["start"]) if incoming else human_date(education["start"]) + " – Present"
        subtitle = education["degree_en"] + " · " + education["program_en"] if incoming else education["program"] + " · Undergraduate"
        tag = ' <span class="record-tag">Incoming</span>' if incoming else ""
        notes = [] if incoming else [education["class"], *education["highlights"]]
        details = '<ul class="record-highlights">' + "".join("<li>" + text(n) + "</li>" for n in notes) + "</ul>"
        rows.append(f'''<article class="record education-record"><div class="record-heading">{record_logo(education)}<div><h3>{text(education['institution'])}{tag}</h3><p class="education-school">{text(education['school'])}</p><p class="record-subtitle education-degree">{text(subtitle)}</p></div></div><time datetime="{text(education['start'])}">{period}</time>{'<div class="record-detail">' + details + '</div>' if notes else ''}</article>''')
    return "\n".join(rows)


def honors_html(profile):
    rows = []
    for award in profile["awards"]:
        if not award.get("visible", True):
            continue
        year = award["date"][:4] if award.get("date") else ""
        detail = " · ".join(text(award[k]) for k in ["event", "role"] if award.get(k))
        detail_html = '<span class="honor-detail"> · ' + detail + '</span>' if detail else ""
        date_html = f'<time>{year}</time>' if year else '<span aria-hidden="true"></span>'
        rows.append(f'<li>{date_html}<div>{text(award["title"])}{detail_html}</div></li>')
    return "\n".join(rows)


def rich_text(value, links=(), emphasis=()):
    """Escape prose and add only explicitly configured links/emphasis."""
    urls = {item["text"]: item["url"] for item in links}
    keys = sorted(set(urls) | set(emphasis), key=len, reverse=True)
    if not keys:
        return text(value)
    parts = re.split("(" + "|".join(re.escape(key) for key in keys) + ")", value)
    return "".join(link(urls[part], text(part)) if part in urls else
                   "<strong>" + text(part) + "</strong>" if part in emphasis else text(part)
                   for part in parts)


def news_html(profile):
    rows = []
    for item in profile.get("news", []):
        if not item.get("visible", True):
            continue
        prose = rich_text(item["text"], item.get("links", []), item.get("emphasis", []))
        rows.append(f'<div class="recent-news"><p><time datetime="{text(item["date"])}">{human_date(item["date"])}</time> {prose}</p></div>')
    return "".join(rows)


def section_images_html(profile, section):
    return "".join('<figure class="section-media"><img src="' + text(item["path"]) + '" alt="' + text(item["alt"]) + '" loading="lazy">' + ('<figcaption>' + text(item["caption"]) + '</figcaption>' if item.get("caption") else '') + '</figure>' for item in profile.get("section_images", {}).get(section, []) if item.get("visible", True))


def service_html(profile):
    rows = []
    for item in profile["service_and_interests"]:
        if not item.get("visible", True):
            continue
        details = item.get("details", []) or ([item["summary"]] if item.get("summary") else [])
        rows.append('<li><strong>' + text(item["title"]) + '</strong><br><span>' + text(item["organization"]) + '</span>' + ''.join('<p class="service-detail">' + text(detail) + '</p>' for detail in details) + '</li>')
    return ''.join(rows)


def public_metrics(metrics):
    return {"observed_at": metrics["observed_at"], "items": [{"id": item["id"], "value": item["value"]} for item in metrics["items"]]}


class PageAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.paths = []
        self.fragments = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                raise ValueError(f'Duplicate HTML id: {attrs["id"]}')
            self.ids.add(attrs["id"])
        for attr in ["href", "src"]:
            value = attrs.get(attr, "")
            if value.startswith("#"):
                self.fragments.append(value[1:])
            elif value and not urlparse(value).scheme:
                self.paths.append(value)


def main():
    profile = read_json("profile")
    publications = read_json("publications")
    metrics = read_json("metrics")
    replacements = {
        "PROFILE": profile_html(profile),
        "ABOUT": "".join("<p>" + rich_text(paragraph, profile.get("about_links", [])) + "</p>" for paragraph in profile["about"]),
        "NEWS": news_html(profile),
        "PUBLICATIONS": publications_html(publications),
        "OPEN_SOURCE": open_source_html(profile, metrics),
        "EXPERIENCE": experience_html(profile),
        "EDUCATION": education_html(profile),
        "HONORS": honors_html(profile),
        "SERVICE": service_html(profile),
        "SERVICE_INTRO": text(profile.get("service_intro", "Outside research, music is an important part of my life. I play the violin and sing tenor.")),
        "YEAR": profile["updated_on"][:4],
        "UPDATED": date.fromisoformat(profile["updated_on"]).strftime("%B %d, %Y"),
        "EMAIL": text(profile["email"])
    }
    for section in ["about", "publications", "open-source", "experience", "education", "honors", "beyond"]:
        replacements["ICON_" + section.upper().replace("-", "_")] = icon(section, 21)
        replacements["IMAGES_" + section.upper().replace("-", "_")] = section_images_html(profile, section)
    html = (ROOT / "site" / "index.template.html").read_text(encoding="utf-8")
    for key, value in replacements.items():
        html = html.replace("{{" + key + "}}", value)
    if "{{" in html:
        raise ValueError("Unresolved template marker")
    # dist is generated output only. Refuse links or any target outside this workspace.
    if OUTPUT.is_symlink() or OUTPUT.resolve() != ROOT.resolve() / "dist":
        raise ValueError("Refusing to rebuild a redirected dist directory")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    (OUTPUT / "assets").mkdir(parents=True)
    for name in ["styles.css", "main.js", "favicon.svg"]:
        shutil.copy2(ROOT / "site" / name, OUTPUT / "assets" / name)
    font_source = ROOT / "assets" / "fonts"
    if not (font_source / "fonts.css").is_file():
        raise FileNotFoundError("Self-hosted fonts are missing")
    shutil.copytree(font_source, OUTPUT / "assets" / "fonts")
    visible_papers = [paper for paper in publications["items"] if paper.get("visible", True)]
    selected_images = [profile["portrait"]["path"], *(paper["image"]["path"] for paper in visible_papers if paper.get("image")), *(item["path"] for images in profile.get("section_images", {}).values() for item in images if item.get("visible", True))]
    selected_images += [item['logo']['path'] for section in ['education', 'research_experience'] for item in profile[section] if item.get('visible', True) and item.get('logo')]
    selected_images += [item['banner']['path'] for item in profile['projects'] if item.get('visible', True) and item.get('banner')]
    selected_images = list(dict.fromkeys(selected_images))
    for relative in selected_images:
        source = (ROOT / relative).resolve()
        source.relative_to((ROOT / "assets" / "images").resolve())
        target = OUTPUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")
    (OUTPUT / "assets" / "metrics.json").write_text(json.dumps(public_metrics(metrics)) + "\n", encoding="utf-8")
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUTPUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://wys-whu.github.io/sitemap.xml\n", encoding="utf-8")
    (OUTPUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://wys-whu.github.io/</loc><lastmod>' + profile["updated_on"] + '</lastmod></url></urlset>\n', encoding="utf-8")
    audit = PageAudit()
    audit.feed(html)
    for path in audit.paths:
        if not (OUTPUT / path).is_file():
            raise FileNotFoundError(f"Missing public resource: {path}")
    for fragment in audit.fragments:
        if fragment not in audit.ids:
            raise ValueError(f"Missing anchor: {fragment}")
    manifest = {"output": str(OUTPUT), "papers": len(visible_papers), "images": selected_images, "files": sorted(p.relative_to(OUTPUT).as_posix() for p in OUTPUT.rglob("*") if p.is_file()), "local_resource_references_checked": len(audit.paths), "section_links_checked": len(audit.fragments)}
    (ROOT / "work").mkdir(exist_ok=True)
    (ROOT / "work" / "build-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {OUTPUT / 'index.html'}")
    print(f"Verified {len(audit.paths)} local resource references and {len(audit.fragments)} section links.")


if __name__ == "__main__":
    main()
