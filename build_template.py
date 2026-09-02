#!/usr/bin/env python3
"""
Renders the styled two-column template resume (matches the requested mockup) to HTML + PDF.

Design: Rubik (Google font, embedded), blue accent, avatar with initials, skill pills grouped
by category, icon contact line, two-column body. Content comes from content.py (single source).

ATS note: the reading order in the generated HTML is header -> full left column -> full right
column, so a parser that extracts in DOM order reads cleanly. render_pdf still governs the plain
single-column .docx/.pdf which remains the safest thing to submit to strict parsers.
"""

import base64
import html as _html
import pathlib
import re

import content as C

OUT = "/projects/sandbox/resume"
BLUE = "#1a73e8"
AVATAR = "#1391f5"
INK = "#202124"
GREY = "#5f6368"


def font_face():
    def b64(name):
        return base64.b64encode(pathlib.Path(f"{OUT}/fonts/{name}").read_bytes()).decode()
    return f"""
  @font-face {{ font-family:'Rubik'; font-style:normal; font-weight:300 900;
    src:url(data:font/ttf;base64,{b64('Rubik.ttf')}) format('truetype'); }}
  @font-face {{ font-family:'Rubik'; font-style:italic; font-weight:300 900;
    src:url(data:font/ttf;base64,{b64('Rubik-Italic.ttf')}) format('truetype'); }}
"""


# --- tiny inline SVG icons (decorative; the text beside them is the real data) ---
def icon(kind, color=BLUE):
    paths = {
        "phone": "M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z",
        "mail": "M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zm8 7L4 6.5V6l8 4.5L20 6v.5L12 11z",
        "linkedin": "M4.98 3.5C4.98 4.9 3.87 6 2.5 6S0 4.9 0 3.5 1.12 1 2.5 1s2.48 1.1 2.48 2.5zM.5 8h4V23h-4V8zm7.5 0h3.8v2.05h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V23h-4v-6.6c0-1.57-.03-3.6-2.2-3.6-2.2 0-2.53 1.72-2.53 3.5V23h-4V8z",
        "github": "M12 2C6.48 2 2 6.48 2 12c0 4.42 2.87 8.17 6.84 9.5.5.09.66-.22.66-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.89 1.53 2.34 1.09 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02.8-.22 1.65-.33 2.5-.33s1.7.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85v2.74c0 .27.16.58.67.48A10 10 0 0 0 22 12c0-5.52-4.48-10-10-10z",
        "pin": "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z",
        "cal": "M7 2v2H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3V2h-2v2H9V2H7zM4 9h16v11H4V9z",
    }
    return (f'<svg viewBox="0 0 24 24" width="11" height="11" fill="{color}" '
            f'style="vertical-align:-1px;margin-right:4px;flex:none">'
            f'<path d="{paths[kind]}"/></svg>')


def initials(name):
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper()


CSS = f"""
{font_face()}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  @page {{ size:A4; margin:0; }}
  html,body {{ font-family:'Rubik',Arial,sans-serif; color:{INK}; }}
  body {{ font-size:8.9pt; line-height:1.21; }}
  .page {{ padding:12px 26px 8px; }}

  header {{ display:flex; justify-content:space-between; align-items:flex-start; gap:16px; }}
  h1 {{ font-size:22pt; font-weight:700; letter-spacing:.5px; line-height:1; }}
  .subtitle {{ color:{BLUE}; font-size:11pt; font-weight:500; margin-top:4px; }}
  .contact {{ margin-top:7px; display:flex; flex-wrap:wrap; gap:3px 16px; max-width:520px; }}
  .contact span {{ display:inline-flex; align-items:center; font-size:9pt; color:{GREY};
    white-space:nowrap; }}
  .contact a.clink {{ text-decoration:none; color:inherit; }}
  .avatar {{ width:88px; height:88px; border-radius:50%; background:{AVATAR}; flex:none;
    display:flex; align-items:center; justify-content:center; color:#0b2a4a;
    font-size:22pt; font-weight:600; letter-spacing:1px; }}

  .grid {{ display:grid; grid-template-columns:1.32fr 1fr; gap:0 28px; margin-top:9px; }}
  section {{ break-inside:avoid; }}
  h2 {{ font-size:11.5pt; font-weight:700; letter-spacing:.6px; text-transform:uppercase;
    border-bottom:1.6px solid {INK}; padding-bottom:2.5px; margin:9px 0 5px; }}
  .grid > div > section:first-child h2 {{ margin-top:0; }}

  .role {{ font-size:10pt; font-weight:600; margin-top:5px; }}
  .org {{ color:{BLUE}; font-size:9.2pt; font-weight:500; margin-top:1px; }}
  .meta {{ display:flex; flex-wrap:wrap; gap:2px 16px; color:{GREY}; font-size:8.6pt;
    margin:2px 0 1px; }}
  .meta span {{ display:inline-flex; align-items:center; }}
  ul {{ list-style:none; margin-top:3px; }}
  li {{ position:relative; padding-left:11px; margin-bottom:1.5px; font-size:8.9pt; color:#3c4043; }}
  li::before {{ content:'•'; position:absolute; left:1px; color:{GREY}; }}

  p.summary {{ font-size:9pt; color:#3c4043; }}

  .skillgroup {{ margin-bottom:6px; }}
  .skilllabel {{ color:{BLUE}; font-weight:600; font-size:9.4pt; margin-bottom:4px; }}
  .pills {{ display:flex; flex-wrap:wrap; gap:5px; }}
  .pill {{ border:1px solid #dadce0; border-radius:5px; padding:3px 7px; font-size:8.4pt;
    color:{INK}; white-space:nowrap; line-height:1.15; }}

  .edu {{ display:flex; justify-content:space-between; align-items:center; gap:14px; }}
  .edu .left {{ flex:1; }}
  .cgpa {{ border-left:1px solid #dadce0; padding-left:14px; text-align:center; flex:none; }}
  .cgpa .lbl {{ font-size:8pt; color:{GREY}; letter-spacing:.5px; }}
  .cgpa .val {{ font-size:12pt; }}
  .cgpa .val b {{ color:{BLUE}; font-weight:700; }}
  .projlink {{ color:{GREY}; font-size:8.6pt; margin:2px 0; display:flex; align-items:center; }}
"""


def esc(s):
    return _html.escape(s)


def contact_line():
    email = C.CONTACT_1.split("|")[2].strip()
    phone = C.CONTACT_1.split("|")[1].strip()
    li = C.CONTACT_2.split("|")[0].strip()
    gh = C.CONTACT_2.split("|")[1].strip()
    loc = C.CONTACT_1.split("|")[0].strip()
    items = [
        (icon("phone"), phone, "tel:" + phone.replace(" ", "")),
        (icon("mail"), email, "mailto:" + email),
        (icon("linkedin"), li, "https://" + li),
        (icon("github"), gh, "https://" + gh),
        (icon("pin"), loc, None),
    ]
    out = []
    for ic, t, href in items:
        if href:
            out.append(f'<a class="clink" href="{esc(href)}"><span>{ic}{esc(t)}</span></a>')
        else:
            out.append(f"<span>{ic}{esc(t)}</span>")
    return "".join(out)


def meta(dates, place="Remote"):
    return (f'<div class="meta"><span>{icon("cal", GREY)}{esc(dates)}</span>'
            f'<span>{icon("pin", GREY)}{esc(place)}</span></div>')


def exp_block(j, place="Remote"):
    o = [f'<div class="role">{esc(j["role"])}</div>']
    if j.get("org"):
        o.append(f'<div class="org">{esc(j["org"].split("  |  ")[0])}</div>')
    o.append(meta(j["dates"], place))
    o.append("<ul>" + "".join(f"<li>{esc(b)}</li>" for b in j["bullets"]) + "</ul>")
    return "".join(o)


def proj_block(j):
    text = j["bullets"][0]
    # last "  |  " segment is the repo link if present
    link = ""
    if "  |  " in text:
        body, link = text.rsplit("  |  ", 1)
    else:
        body = text
    o = [f'<div class="role">{esc(j["role"])}</div>',
         f'<div class="meta"><span>{icon("cal", GREY)}{esc(j["dates"])}</span></div>']
    if link:
        o.append(f'<div class="projlink">{icon("github", GREY)}{esc(link)}</div>')
    o.append(f'<ul><li>{esc(body)}</li></ul>')
    return "".join(o)


def build():
    left = ['<section><h2>Experience</h2>']
    for j in C.EXPERIENCE:
        left.append(exp_block(j))
    left.append("</section>")

    ed = C.EDUCATION
    left.append('<section><h2>Education</h2><div class="edu"><div class="left">')
    left.append(f'<div class="role">{esc(ed["degree"])}</div>')
    left.append(f'<div class="org">{esc(ed["institution"].split(",")[0])}</div>')
    left.append(meta(ed["dates"], ", ".join(ed["institution"].split(",")[1:]).strip()))
    left.append("</div>")
    score = ed["score"].replace("CGPA:", "").strip()  # "7.4 / 10"
    num, _, denom = score.partition("/")
    left.append(f'<div class="cgpa"><div class="lbl">CGPA</div>'
                f'<div class="val"><b>{esc(num.strip())}</b> / {esc(denom.strip())}</div></div>')
    left.append("</div></section>")

    left.append('<section><h2>Projects</h2>')
    for j in C.PROJECTS:
        left.append(proj_block(j))
    left.append("</section>")

    right = [f'<section><h2>Summary</h2><p class="summary">{esc(C.SUMMARY)}</p></section>',
             '<section><h2>Skills</h2>']
    for label, items in C.SKILLS:
        # split on commas that are NOT inside parentheses, so "Next.js (App Router, SSR/SSG/ISR)"
        # stays a single pill
        parts = re.split(r",(?![^(]*\))", items)
        pills = "".join(f'<span class="pill">{esc(x.strip())}</span>' for x in parts if x.strip())
        right.append(f'<div class="skillgroup"><div class="skilllabel">{esc(label)}</div>'
                     f'<div class="pills">{pills}</div></div>')
    right.append("</section>")

    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>{esc(C.NAME.title())} - Resume</title><style>{CSS}</style></head><body>
<div class="page">
  <header>
    <div>
      <h1>{esc(C.NAME)}</h1>
      <div class="subtitle">{esc(C.TITLE.replace('  |  ', ' | '))}</div>
      <div class="contact">{contact_line()}</div>
    </div>
    <div class="avatar">{esc(initials(C.NAME))}</div>
  </header>
  <div class="grid">
    <div>{''.join(left)}</div>
    <div>{''.join(right)}</div>
  </div>
</div>
</body></html>"""

    path = f"{OUT}/Aman_Jaiman_Resume_Template.html"
    pathlib.Path(path).write_text(doc, encoding="utf-8")
    return path


if __name__ == "__main__":
    print("wrote", build())
