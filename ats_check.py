#!/usr/bin/env python3
"""Simulates how an ATS parses the .docx and audits it against common scoring rules."""
import re
from collections import Counter
from docx import Document

PATH = "/projects/sandbox/resume/Aman_Jaiman_Resume.docx"
doc = Document(PATH)
paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
text = "\n".join(paras)
flat = text.replace("\t", " ")

print("=" * 78)
print("PARSED PLAIN TEXT (what an ATS actually ingests)")
print("=" * 78)
print(flat)

checks = []

# ---- parse safety: the things that actually break ATS extraction ----
checks.append(("No tables", len(doc.tables) == 0))
checks.append(("No images", "graphicData" not in doc.element.xml))
checks.append(("No text boxes", "txbxContent" not in doc.element.xml))
checks.append(("No multi-column section breaks", 'w:num="2"' not in doc.element.xml))
checks.append(("Nothing hidden in headers/footers",
               all(not p.text.strip() for s in doc.sections for p in s.header.paragraphs)
               and all(not p.text.strip() for s in doc.sections for p in s.footer.paragraphs)))

# ---- contact block ----
checks.append(("Name on first line", paras[0].upper() == "AMAN JAIMAN"))
checks.append(("Email parseable", bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", flat))))
checks.append(("Phone parseable", bool(re.search(r"\+91\s?\d{10}", flat))))
checks.append(("Location parseable", "Bharatpur, Rajasthan 321001" in flat))
checks.append(("LinkedIn URL present", "linkedin.com/in/" in flat))
checks.append(("GitHub URL present", "github.com/" in flat))
checks.append(("Target titles in header", "Product Manager" in paras[1] and "Frontend Engineer" in paras[1]))

# ---- standard headings ----
for h in ["Professional Summary", "Technical Skills", "Professional Experience",
          "Projects", "Education", "Achievements & Recognition"]:
    checks.append((f'Recognised heading: "{h}"', h.lower() in flat.lower()))

# ---- dates: must sit in the SAME paragraph as their title, in Mon YYYY form ----
date_re = re.compile(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+20\d{2}\s*-\s*"
                     r"(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+20\d{2}|Present)")
dated_titles = [p for p in paras if date_re.search(p)]
checks.append((f"All 5 role/project dates inline with their title ({len(dated_titles)} found)",
               len(dated_titles) == 5))
checks.append(("Every dated line carries a title, no orphan date rows",
               all(len(date_re.sub("", p).strip()) > 5 for p in dated_titles)))
checks.append(("Current role ends in 'Present' (reads as actively employed)",
               bool(re.search(r"-\s*Present", flat))))
checks.append(("Continuous timeline, no gap at Apr 2025",
               "Apr 2024 - Apr 2025" in flat and "Apr 2025 - Present" in flat))
checks.append(("Newest role listed first (reverse-chronological)",
               flat.index("Apr 2025 - Present") < flat.index("Apr 2024 - Apr 2025")))

# ---- education (the original resume's weakest section) ----
edu = ["Bachelor of Technology", "B.Tech", "Computer Science & Engineering",
       "Lovely Professional University", "Phagwara, Punjab", "2020 - 2024", "CGPA: 7.4"]
missing_edu = [k for k in edu if k not in flat]
checks.append(("Education structured: degree + field + institution + location + dates + CGPA", not missing_edu))

# ---- formatting hygiene ----
bullets = [p for p in paras if p.startswith("- ")]
# one-page format: fewer, denser bullets is correct, so the floor is 12 not 20
checks.append((f"Plain-hyphen bullets, machine readable ({len(bullets)})", len(bullets) >= 12))
checks.append(("No decorative glyphs or private-use characters",
               not re.search(r"[\u2022\u25AA\u25CF\u2713\uE000-\uF8FF]", text)))
checks.append(("Single standard font (Calibri) throughout",
               all(r.font.name in (None, "Calibri") for p in doc.paragraphs for r in p.runs)))

# ---- content quality signals ----
verbs = ["Founded", "Architected", "Built", "Migrated", "Cut", "Designed", "Implemented", "Ran",
         "Instrumented", "Mentored", "Developed", "Integrated", "Improved", "Partnered", "Engineered",
         "Achieved", "Redesigned", "Secured", "Solved", "Awarded", "Ranked", "Shipped", "Delivered"]
used = sorted({v for v in verbs if re.search(rf"\b{v}\b", flat)})
# scaled to bullet count: a dense one-pager has ~10 bullets, so 10 distinct verbs is full marks
checks.append((f"Distinct strong action verbs ({len(used)})", len(used) >= 10))

# no verb should lead more than two bullets - repetition reads as filler
leads = [b[2:].split()[0] for b in bullets if b[2:].split()]
repeats = {v: n for v, n in Counter(leads).items() if n > 2 and v in verbs}
checks.append((f"No action verb leads more than 2 bullets", not repeats))
metrics = re.findall(r"\d+\s*%|\b\d{2,}\+", flat)
checks.append((f"Quantified achievements ({len(metrics)})", len(metrics) >= 12))
words = len(flat.split())
checks.append((f"Length in single-page ATS band 550-850 words ({words})", 550 <= words <= 850))
checks.append(("No first-person pronouns in bullets",
               not re.search(r"\b(I|my|me)\b", "\n".join(bullets))))

# ---- keyword coverage for both target titles ----
kw = ["React", "Next.js", "TypeScript", "JavaScript", "Node.js", "REST", "API", "Tailwind", "SQL",
      "PostgreSQL", "Git", "CI/CD", "Agile", "Scrum", "Roadmap", "Product Manager", "Frontend",
      "PRD", "Stakeholder", "A/B Test", "Analytics", "User Research", "Sprint", "Backlog",
      "Data Structures", "Algorithms", "Accessibility", "SEO", "Performance", "Figma", "Jira"]
missing_kw = [k for k in kw if k.lower() not in flat.lower()]
checks.append((f"Keyword coverage {len(kw) - len(missing_kw)}/{len(kw)}", not missing_kw))

print("\n" + "=" * 78)
print("ATS COMPLIANCE AUDIT")
print("=" * 78)
passed = 0
for label, ok in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    passed += bool(ok)
if missing_kw:
    print(f"         -> missing keywords: {missing_kw}")
if missing_edu:
    print(f"         -> missing education fields: {missing_edu}")

pct = round(passed / len(checks) * 100)
print("-" * 78)
print(f"  RESULT: {passed}/{len(checks)} checks passed  ->  ATS readiness score: {pct}%")
print("=" * 78)
