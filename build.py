#!/usr/bin/env python3
"""Renders Aman Jaiman's resume to ATS-safe .docx, print-ready .html, and plain .md from content.py."""

import html as _html
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import content as C

OUT = "/projects/sandbox/resume"
FONT = "Calibri"
DARK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x44, 0x44, 0x44)
RIGHT_TAB = Inches(7.0)
BODY = 9.5


# ============================================================ DOCX
def build_docx():
    doc = Document()
    s = doc.styles["Normal"]
    s.font.name = FONT
    s.font.size = Pt(BODY)
    s.font.color.rgb = DARK
    s._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    s.paragraph_format.space_before = Pt(0)
    s.paragraph_format.space_after = Pt(0)
    s.paragraph_format.line_spacing = 1.0
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Inches(0.35)
        sec.left_margin = sec.right_margin = Inches(0.5)

    def para(sb=0, sa=0, align=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(sb)
        p.paragraph_format.space_after = Pt(sa)
        if align is not None:
            p.alignment = align
        return p

    def run(p, text, size=BODY, bold=False, italic=False, color=DARK, caps=False):
        r = p.add_run(text)
        r.font.name = FONT
        r.font.size = Pt(size)
        r.bold, r.italic = bold, italic
        r.font.color.rgb = color
        r.font.all_caps = caps
        return r

    def heading(text):
        p = para(sb=5, sa=2)
        run(p, text, size=10.5, bold=True, caps=True)
        pPr = p._p.get_or_add_pPr()
        bdr = OxmlElement("w:pBdr")
        b = OxmlElement("w:bottom")
        b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "8")
        b.set(qn("w:space"), "1"); b.set(qn("w:color"), "555555")
        bdr.append(b); pPr.append(bdr)
        p.paragraph_format.keep_with_next = True

    def entry(title, dates, org, stack):
        # Title + dates live in ONE paragraph -> a parser never orphans the date.
        p = para(sb=3.5)
        p.paragraph_format.tab_stops.add_tab_stop(RIGHT_TAB, WD_TAB_ALIGNMENT.RIGHT)
        p.paragraph_format.keep_with_next = True  # never orphan a title at a page break
        run(p, title, size=10, bold=True)
        run(p, "\t" + dates, bold=True)
        if not (org or stack):
            return
        p = para(sb=0.5, sa=1.5)
        p.paragraph_format.keep_with_next = True
        if stack:
            p.paragraph_format.tab_stops.add_tab_stop(RIGHT_TAB, WD_TAB_ALIGNMENT.RIGHT)
        run(p, org or "", italic=True, color=GREY)
        if stack:
            run(p, "\t" + stack, italic=True, color=GREY)

    def bullet(text, label=None):
        p = para(sa=0.8)
        p.paragraph_format.left_indent = Inches(0.22)
        p.paragraph_format.first_line_indent = Inches(-0.14)
        run(p, "- ")
        if label:
            run(p, label + " ", bold=True)
        run(p, text)

    p = para(align=WD_ALIGN_PARAGRAPH.CENTER)
    run(p, C.NAME, size=20, bold=True)
    p = para(sb=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    run(p, C.TITLE, size=10.5, bold=True, color=GREY)
    for line in (C.CONTACT_1, C.CONTACT_2):
        p = para(sb=2, align=WD_ALIGN_PARAGRAPH.CENTER)
        run(p, line, size=9.5)

    heading("Professional Summary")
    run(para(), C.SUMMARY)

    heading("Technical Skills")
    for label, items in C.SKILLS:
        p = para(sa=1.6)
        run(p, label + ": ", bold=True)
        run(p, items)

    heading("Professional Experience")
    for j in C.EXPERIENCE:
        entry(j["role"], j["dates"], j["org"], j["stack"])
        for b in j["bullets"]:
            bullet(b)

    heading("Projects")
    for j in C.PROJECTS:
        entry(j["role"], j["dates"], j["org"], j["stack"])
        for b in j["bullets"]:
            bullet(b)

    heading("Education")
    entry(C.EDUCATION["degree"], C.EDUCATION["dates"], C.EDUCATION["institution"], C.EDUCATION["score"])
    if C.EDUCATION.get("coursework"):
        bullet(C.EDUCATION["coursework"])

    heading("Achievements & Recognition")
    for a in C.ACHIEVEMENTS:
        label = a["title"] + (f" ({a['date']})" if a.get("date") else "") + ":"
        bullet(a["detail"], label=label)

    path = f"{OUT}/Aman_Jaiman_Resume.docx"
    doc.save(path)
    return path


# ============================================================ HTML
CSS = """
  @page { size: A4; margin: 9mm; }
  * { box-sizing: border-box; }
  body { font-family: Calibri, Carlito, Arial, sans-serif; font-size: 9.7pt; line-height: 1.2;
         color: #1a1a1a; max-width: 192mm; margin: 0 auto; padding: 0; }
  h1 { font-size: 20pt; letter-spacing: 1px; text-align: center; margin: 0; }
  .title { text-align: center; font-size: 10.5pt; font-weight: 700; color: #444; margin: 2px 0 3px; }
  .contact { text-align: center; font-size: 9.5pt; margin: 0.5px 0; }
  h2 { font-size: 10.5pt; text-transform: uppercase; letter-spacing: .6px; border-bottom: 1px solid #555;
       margin: 3.5px 0 2px; padding-bottom: 1.5px; }
  .row { display: flex; justify-content: space-between; align-items: baseline; gap: 14px; margin-top: 3.5px; }
  .row.sub { margin-top: 1px; }
  .role { font-weight: 700; font-size: 10pt; }
  .dates { font-weight: 700; white-space: nowrap; }
  .org, .stack { font-style: italic; color: #444; }
  .stack { white-space: nowrap; }
  ul { margin: 1px 0 0; padding-left: 15px; }
  li { margin-bottom: 0.5px; }
  p { margin: 0; }
  .skills p { margin-bottom: 2px; }
  .entry { break-inside: avoid; page-break-inside: avoid; }
  @media print { body { padding: 0; } h2 { page-break-after: avoid; } li { page-break-inside: avoid; } }
"""


def build_html():
    e = _html.escape
    o = ["<!DOCTYPE html>", '<html lang="en"><head><meta charset="UTF-8">',
         f"<title>{e(C.NAME.title())} - Product Manager & Frontend Engineer</title>",
         f"<style>{CSS}</style></head><body>",
         f"<h1>{e(C.NAME)}</h1>",
         f'<p class="title">{e(C.TITLE)}</p>',
         f'<p class="contact">{e(C.CONTACT_1)}</p>',
         f'<p class="contact">{e(C.CONTACT_2)}</p>',
         "<h2>Professional Summary</h2>", f"<p>{e(C.SUMMARY)}</p>",
         '<h2>Technical Skills</h2><div class="skills">']
    for label, items in C.SKILLS:
        o.append(f"<p><b>{e(label)}:</b> {e(items)}</p>")
    o.append("</div>")

    def entry(j):
        o.append('<div class="entry">')
        o.append(f'<div class="row"><span class="role">{e(j["role"])}</span>'
                 f'<span class="dates">{e(j["dates"])}</span></div>')
        if j.get("org") or j.get("stack"):
            sub = f'<div class="row sub"><span class="org">{e(j.get("org") or "")}</span>'
            if j.get("stack"):
                sub += f'<span class="stack">{e(j["stack"])}</span>'
            o.append(sub + "</div>")
        o.append("<ul>" + "".join(f"<li>{e(b)}</li>" for b in j["bullets"]) + "</ul>")
        o.append("</div>")

    o.append("<h2>Professional Experience</h2>")
    for j in C.EXPERIENCE:
        entry(j)
    o.append("<h2>Projects</h2>")
    for j in C.PROJECTS:
        entry(j)

    ed = C.EDUCATION
    o.append("<h2>Education</h2>")
    o.append('<div class="entry">')
    o.append(f'<div class="row"><span class="role">{e(ed["degree"])}</span>'
             f'<span class="dates">{e(ed["dates"])}</span></div>')
    o.append(f'<div class="row sub"><span class="org">{e(ed["institution"])}</span>'
             f'<span class="stack">{e(ed["score"])}</span></div>')
    if ed.get("coursework"):
        o.append(f'<ul><li>{e(ed["coursework"])}</li></ul>')
    o.append("</div>")

    o.append("<h2>Achievements &amp; Recognition</h2><ul>")
    for a in C.ACHIEVEMENTS:
        label = a["title"] + (f" ({a['date']})" if a.get("date") else "") + ":"
        o.append(f"<li><b>{e(label)}</b> {e(a['detail'])}</li>")
    o.append("</ul></body></html>")

    path = f"{OUT}/Aman_Jaiman_Resume.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return path


# ============================================================ MARKDOWN
def build_md():
    o = [f"# {C.NAME}", f"## {C.TITLE.replace('  |  ', ' | ')}", "",
         C.CONTACT_1.replace("  |  ", " | "), "", C.CONTACT_2.replace("  |  ", " | "), "",
         "---", "", "## PROFESSIONAL SUMMARY", "", C.SUMMARY, "", "---", "", "## TECHNICAL SKILLS", ""]
    for label, items in C.SKILLS:
        o += [f"**{label}:** {items}", ""]

    def entry(j):
        o.append(f'### {j["role"]}')
        if j.get("org"):
            o.append(f'**{j["org"].replace("  |  ", " | ")}** | {j["dates"]}')
        else:
            o.append(f'**{j["dates"]}**')
        if j.get("stack"):
            o.append(f'*{j["stack"]}*')
        o.append("")
        o.extend(f"- {b}" for b in j["bullets"])
        o.append("")

    o += ["---", "", "## PROFESSIONAL EXPERIENCE", ""]
    for j in C.EXPERIENCE:
        entry(j)
    o += ["---", "", "## PROJECTS", ""]
    for j in C.PROJECTS:
        entry(j)

    ed = C.EDUCATION
    o += ["---", "", "## EDUCATION", "", f'### {ed["degree"]}',
          f'**{ed["institution"]}** | {ed["dates"]} | {ed["score"]}', ""]
    if ed.get("coursework"):
        o += [f'- {ed["coursework"]}', ""]
    o += ["---", "", "## ACHIEVEMENTS & RECOGNITION", ""]
    for a in C.ACHIEVEMENTS:
        label = a["title"] + (f" ({a['date']})" if a.get("date") else "") + ":"
        o.append(f"- **{label}** {a['detail']}")
    o.append("")

    path = f"{OUT}/Aman_Jaiman_Resume.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    return path


if __name__ == "__main__":
    for p in (build_docx(), build_html(), build_md()):
        print("wrote", p)
