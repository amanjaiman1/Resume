#!/usr/bin/env python3
"""
Renders the classic resume: the layout of Aman's original one-page resume, filled with the content of
the styled template.

Layout, taken from the original: centred small-caps name, an icon contact line, bold section headings
over a full-width rule, bold title rows with the date flush right, italic "organisation | tech" rows,
hanging-indent bullets, and the original's date style (Apr 24 – Apr 25). Every right-aligned item ends
exactly where the section rules end, and spacing is the same between every pair of entries.

Content comes from content.py, the same data the styled template uses: title, contact details,
education, experience, TEMPLATE_PROJECTS and achievements. Technical Skills are the exception: they are
the original resume's own, kept word for word in content.CLASSIC_SKILLS.

Font: Gelasio (SIL Open Font License, see fonts/Gelasio-OFL.txt), a free lookalike of Georgia with the
same old-style figures, embedded so the PDF is self-contained. Run render_classic_pdf.py next.
"""

import base64
import html as _html
import io
import pathlib
import re

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent
from fontTools.varLib.instancer import instantiateVariableFont

import content as C

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "Aman_Jaiman_Resume_Classic.html"

# Icons are ICON px squares. Raising an icon's bottom edge by half Gelasio's cap height (1419/2048 em)
# minus half its own size centres it exactly on the capitals of the text that follows it.
ICON = 11
CAP_HALF_EM = 1419 / 2048 / 2

PATHS = {
    "phone": "M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z",
    "mail": "M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zm8 7L4 6.5V6l8 4.5L20 6v.5L12 11z",
    "github": "M12 2C6.48 2 2 6.48 2 12c0 4.42 2.87 8.17 6.84 9.5.5.09.66-.22.66-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.89 1.53 2.34 1.09 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02.8-.22 1.65-.33 2.5-.33s1.7.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85v2.74c0 .27.16.58.67.48A10 10 0 0 0 22 12c0-5.52-4.48-10-10-10z",
    # LinkedIn's square logo, as in the original resume (Simple Icons, CC0)
    "linkedin": "M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.55V9h3.57v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z",
}


SC_SCALE = 0.7  # a small capital is its capital at 70% size, as browsers draw small caps


def small_caps_font(text):
    """Gelasio Regular with each lowercase letter drawn as a small capital, subset to `text`.

    Gelasio has no small caps of its own. When CSS fakes them, the name is drawn in two font sizes,
    and some PDF parsers read every size change as a word break ("A MAN J AIMAN"). With real small-cap
    glyphs the name is one run at one size, so every parser reads it as written.
    """
    font = instantiateVariableFont(TTFont(HERE / "fonts" / "Gelasio.ttf"), {"wght": 400})
    cmap, glyf, hmtx = font.getBestCmap(), font["glyf"], font["hmtx"]
    for ch in {c for c in text if c.islower()}:
        cap = cmap[ord(ch.upper())]
        part = GlyphComponent()
        part.glyphName, part.x, part.y, part.flags = cap, 0, 0, 0
        part.transform = [[SC_SCALE, 0], [0, SC_SCALE]]
        small = Glyph()
        small.numberOfContours, small.components = -1, [part]
        small.recalcBounds(glyf)
        glyf[cmap[ord(ch)]] = small
        advance, lsb = hmtx[cap]
        hmtx[cmap[ord(ch)]] = (round(advance * SC_SCALE), round(lsb * SC_SCALE))
    options = subset.Options()
    options.layout_features = []  # Gelasio's kerning pairs were written for lowercase shapes
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    out = io.BytesIO()
    font.save(out)
    return out.getvalue()


def font_face():
    def b64(data):
        return base64.b64encode(data).decode()

    def file(name):
        return (HERE / "fonts" / name).read_bytes()
    return f"""
  @font-face {{ font-family:'Gelasio'; font-style:normal; font-weight:400 700;
    src:url(data:font/ttf;base64,{b64(file('Gelasio.ttf'))}) format('truetype'); }}
  @font-face {{ font-family:'Gelasio'; font-style:italic; font-weight:400 700;
    src:url(data:font/ttf;base64,{b64(file('Gelasio-Italic.ttf'))}) format('truetype'); }}
  @font-face {{ font-family:'Gelasio SC'; font-style:normal; font-weight:400;
    src:url(data:font/ttf;base64,{b64(small_caps_font(C.NAME.title()))}) format('truetype'); }}
"""


CSS = f"""
{font_face()}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  @page {{ size:8.5in 11in; margin:0; }}
  html,body {{ font-family:'Gelasio',Georgia,serif; color:#000; }}
  body {{ font-size:9.5pt; line-height:1.17; font-variant-ligatures:no-common-ligatures; }}
  .page {{ padding:0.27in 0.4in; }}
  a {{ color:inherit; text-decoration:none; }}

  header {{ text-align:center; }}
  .name {{ font-family:'Gelasio SC',Georgia,serif; font-size:25pt; line-height:1; }}
  .title {{ font-size:10.5pt; margin-top:2.5pt; }}
  .location {{ font-size:10pt; margin-top:1pt; }}
  .contact {{ display:flex; flex-wrap:wrap; justify-content:center; align-items:baseline; gap:0 13pt;
    margin-top:1pt; }}
  .contact .u {{ text-decoration:underline; text-decoration-thickness:0.5pt; text-underline-offset:1.5pt; }}
  .ic {{ margin-right:3pt; vertical-align:calc({CAP_HALF_EM:.4f}em - {ICON / 2}px); }}

  h2 {{ font-size:11.5pt; font-weight:700; border-bottom:0.75pt solid #000; padding-bottom:1pt;
    margin:7.5pt 0 3pt; }}

  .skills {{ padding-left:0.15in; }}
  .skills p + p {{ margin-top:1pt; }}

  .entry + .entry {{ margin-top:4pt; }}
  .row {{ display:flex; justify-content:space-between; align-items:baseline; gap:12pt; }}
  .row .r {{ white-space:nowrap; }}
  .row b {{ font-size:10pt; }}
  .row.sub {{ font-style:italic; }}

  ul {{ list-style:none; margin-top:1.5pt; }}
  li {{ padding-left:0.3in; }}
  li + li {{ margin-top:0.75pt; }}
  /* The bullet stays in normal flow (no positioning), so the PDF draws each bullet right after
     its job title and parsers read them in order. Wrapped lines start at 0.3in, under the text. */
  li::before {{ content:'•'; display:inline-block; width:0.15in; margin-left:-0.15in; }}
"""


def esc(s):
    return _html.escape(s)


def icon(kind):
    path = f'<path d="{PATHS[kind]}"/>'
    if kind == "linkedin":  # the square logo fills its whole box; shrink it to the other icons' size
        path = f'<g transform="translate(1.8 1.8) scale(0.85)">{path}</g>'
    return (f'<svg class="ic" viewBox="0 0 24 24" width="{ICON}" height="{ICON}" aria-hidden="true">'
            f"{path}</svg>")


def short_date(s):
    """'Apr 2025 - Present' -> 'Apr 25 – Present', the original resume's date style. Bare years stay whole."""
    return re.sub(r"\b([A-Z][a-z]{2}) \d{2}(\d{2})\b", r"\1 \2", s).replace(" - ", " – ")


def url(link):
    """Full URL for a bare link. A bare domain gets a trailing slash: https://sortandvisualize.com/"""
    return "https://" + link + ("" if "/" in link else "/")


def row(left, right="", cls="row"):
    right = f'<span class="r">{right}</span>' if right else ""
    return f'<div class="{cls}"><span class="l">{left}</span>{right}</div>'


def bullets(items):
    return "<ul>" + "".join(f"<li>{b}</li>" for b in items) + "</ul>"


def section(title, body):
    return f"<section><h2>{esc(title)}</h2>{body}</section>"


def header():
    location, phone, email = (s.strip() for s in C.CONTACT_1.split("|"))
    linkedin, github = (s.strip() for s in C.CONTACT_2.split("|")[:2])
    items = [
        ("phone", phone, "tel:" + phone.replace(" ", ""), False),
        ("mail", email, "mailto:" + email, True),
        ("linkedin", linkedin, "https://" + linkedin, True),
        ("github", github, "https://" + github, True),
    ]
    contact = ""
    for kind, text, href, underline in items:
        label = f'<span class="u">{esc(text)}</span>' if underline else f"<span>{esc(text)}</span>"
        contact += f'<a href="{esc(href)}">{icon(kind)}{label}</a>'
    title = C.TITLE.replace("  |  ", " | ")
    return (f'<header><div class="name">{esc(C.NAME.title())}</div>'
            f'<div class="title">{esc(title)}</div>'
            f'<div class="location">{esc(location)}</div>'
            f'<div class="contact">{contact}</div></header>')


def skills():
    lines = "".join(f"<p><b>{esc(label)}</b>: {esc(items)}</p>" for label, items in C.CLASSIC_SKILLS)
    return f'<div class="skills">{lines}</div>'


def education():
    ed = C.EDUCATION
    school, _, place = ed["institution"].partition(", ")
    return ('<div class="entry">'
            + row(f'<b>{esc(ed["degree"])}</b>', f'<b>{esc(short_date(ed["dates"]))}</b>')
            + row(f'{esc(school)} | {esc(ed["score"])}', esc(place), "row sub")
            + "</div>")


def experience():
    out = []
    for j in C.EXPERIENCE:
        org, _, place = j["org"].partition("  |  ")
        out.append('<div class="entry">'
                   + row(f'<b>{esc(j["role"])}</b>', f'<b>{esc(short_date(j["dates"]))}</b>')
                   + row(f'{esc(org)} | {esc(j["stack"])}.', esc(j.get("location", place)), "row sub")
                   + bullets(esc(b) for b in j["bullets"])
                   + "</div>")
    return "".join(out)


def projects():
    out = []
    for p in C.TEMPLATE_PROJECTS:
        name = p["role"].split(" - ")[0]  # the short name, as the original resume titles projects
        label = "Repository Link" if p["link"].startswith("github.com") else "Live Link"
        href = url(p["link"])
        out.append('<div class="entry">'
                   + row(f'<b>{esc(name)}</b> | <i>{esc(p["tech"])}.</i>',
                         f'<b>{esc(short_date(p["dates"]))}</b>')
                   + bullets([esc(p["description"]), f'{label}: <a href="{esc(href)}">{esc(href)}</a>'])
                   + "</div>")
    return "".join(out)


# "... 100+ day streak (leetcode.com/u/amanjaiman890)." -> detail text, plus the link in the brackets
LINK_AT_END = re.compile(r"(.*?)\s*\(([\w.-]+\.[a-z]{2,}/\S+)\)\.?")


def achievements():
    out = []
    for a in C.ACHIEVEMENTS:
        detail, right = a["detail"], ""
        m = LINK_AT_END.fullmatch(detail)
        if m:  # the link moves to the right edge of the detail row, as in the original resume
            detail, href = m.group(1) + ".", url(m.group(2))
            right = f'<a href="{esc(href)}">{esc(href)}</a>'
        date = f'<b>{esc(short_date(a["date"]))}</b>' if a.get("date") else ""
        out.append('<div class="entry">' + row(f'<b>{esc(a["title"])}</b>', date)
                   + row(esc(detail), right, "row sub") + "</div>")
    return "".join(out)


def build():
    body = (header()
            + section("Technical Skills", skills())
            + section("Education", education())
            + section("Experience", experience())
            + section("Projects", projects())
            + section("Achievements", achievements()))
    doc = (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
           f"<title>{esc(C.NAME.title())} - Resume</title><style>{CSS}</style></head>"
           f'<body><div class="page">{body}</div></body></html>')
    OUT.write_text(doc, encoding="utf-8")
    return OUT


if __name__ == "__main__":
    print("wrote", build())
