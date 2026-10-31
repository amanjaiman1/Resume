#!/usr/bin/env python3
"""Renders the styled template HTML to PDF + preview PNG, waits for the embedded font, and
reports how a parser extracts the two-column layout."""
import re
import sys
from playwright.sync_api import sync_playwright
from pypdf import PdfReader
from PIL import Image

SRC = "/projects/sandbox/resume/Aman_Jaiman_Resume_Template.html"
PDF = "/projects/sandbox/resume/Aman_Jaiman_Resume_Template.pdf"
PNG = "/projects/sandbox/resume/template_full.png"

with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2)
    page.goto("file://" + SRC)
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(400)
    h = page.evaluate("document.body.getBoundingClientRect().height")
    page.pdf(path=PDF, format="A4", print_background=True)
    page.screenshot(path=PNG, full_page=True)
    b.close()

im = Image.open(PNG)
w, hh = im.size
im.crop((0, 0, w, hh // 2)).resize((w // 2, hh // 4)).save(PNG.replace("full", "top"))
im.crop((0, hh // 2, w, hh)).resize((w // 2, hh // 4)).save(PNG.replace("full", "bottom"))

r = PdfReader(PDF)
pages = len(r.pages)
text = "\n".join(p.extract_text() or "" for p in r.pages)
words = len(text.split())

print(f"content height (px) : {h:.0f}   (single A4 ~ 1123)")
print(f"PDF pages           : {pages}")
print(f"Extractable words   : {words}")
print("\n--- WHAT AN ATS EXTRACTS FROM THE PDF (order matters) ---")
print(text[:1400])
print("...\n")

ok = True
for label, cond in [
    ("Text-based PDF (not an image)", words > 400),
    ("Single page", pages == 1),
    ("Email intact", "amanjaiman001@gmail.com" in text),
    ("Phone intact", "6378722785" in text),
    ("Current role reads as ongoing", "Present" in text),
    ("Education parseable", "Lovely Professional University" in text and "7.4" in text),
    ("Skills + Experience + Education + Projects present",
     all(s.lower() in text.lower() for s in ["Skills", "Experience", "Education", "Projects"])),
]:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    ok &= bool(cond)
sys.exit(0 if ok else 1)
