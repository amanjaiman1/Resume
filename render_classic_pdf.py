#!/usr/bin/env python3
"""Renders the classic resume HTML to a one-page US Letter PDF plus preview PNGs, waits for the embedded
font, and checks the PDF text the way a parser reads it."""
import pathlib
import sys

from playwright.sync_api import sync_playwright
from pypdf import PdfReader
from PIL import Image

import content as C

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "Aman_Jaiman_Resume_Classic.html"
PDF = HERE / "Aman_Jaiman_Resume_Classic.pdf"
PNG = HERE / "classic_full.png"  # ignored by .gitignore; the top and bottom crops are committed

with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page(viewport={"width": 816, "height": 1056}, device_scale_factor=2)
    page.goto(SRC.as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(400)
    h = page.evaluate("document.querySelector('.page').getBoundingClientRect().height")
    page.pdf(path=str(PDF), format="Letter", print_background=True, prefer_css_page_size=True)
    page.screenshot(path=str(PNG), full_page=True)
    b.close()

im = Image.open(PNG)
w, hh = im.size
im.crop((0, 0, w, hh // 2)).resize((w // 2, hh // 4)).save(HERE / "classic_top.png")
im.crop((0, hh // 2, w, hh)).resize((w // 2, hh // 4)).save(HERE / "classic_bottom.png")

reader = PdfReader(PDF)
pages = len(reader.pages)
text = "\n".join(p.extract_text() or "" for p in reader.pages)
flat = " ".join(text.split())
links = {a.get_object()["/A"]["/URI"] for p in reader.pages for a in p.get("/Annots", [])
         if a.get_object().get("/A", {}).get("/URI")}

print(f"content height (px) : {h:.0f}   (one US Letter page = 1056)")
print(f"PDF pages           : {pages}")
print(f"Extractable words   : {len(flat.split())}")
print("\n--- WHAT A PARSER EXTRACTS FROM THE PDF ---")
print(text[:1400])
print("...\n")

expected_links = {"mailto:amanjaiman001@gmail.com", "https://linkedin.com/in/aman-jaiman",
                  "https://github.com/amanjaiman1", "https://sortandvisualize.com/",
                  "https://github.com/amanjaiman1/Product_3D"}
bullets = [b for j in C.CLASSIC_EXPERIENCE for b in j["bullets"]]
bullets += [b for p in C.TEMPLATE_PROJECTS for b in [p["description"], *p.get("classic_points", [])]]
dropped = [b for j in C.EXPERIENCE for b in j["bullets"] if b not in bullets]


def norm(s):
    return " ".join(s.split())
ok = True
for label, cond in [
    ("Single page", pages == 1),
    ("Text-based PDF (not an image)", len(flat.split()) > 400),
    ("Email and phone intact", "amanjaiman001@gmail.com" in flat and "6378722785" in flat),
    ("Current role reads as ongoing", "Present" in flat),
    ("Education parseable", "Lovely Professional University" in flat and "7.4" in flat),
    ("All sections present",
     all(s in flat for s in ["Technical Skills", "Education", "Experience", "Projects", "Achievements"])),
    ("Original Technical Skills kept word for word",
     all(" ".join(f"{label}: {items}".split()) in flat for label, items in C.CLASSIC_SKILLS)),
    ("Sort & Visualize in; DocMate and LeetCode out",
     "Sort & Visualize" in flat and "DocMate" not in flat and "LeetCode" not in flat),
    (f"All {len(bullets)} bullets present", all(norm(b) in flat for b in bullets)),
    (f"{len(dropped)} dropped bullet(s) absent", not any(norm(b) in flat for b in dropped)),
    ("Contact and project links clickable", expected_links <= links),
]:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    ok &= bool(cond)
sys.exit(0 if ok else 1)
