#!/usr/bin/env python3
"""Renders the HTML resume to a text-based (ATS-readable) PDF and a PNG preview, then verifies it."""
import re
import sys
from playwright.sync_api import sync_playwright

SRC = "/projects/sandbox/resume/Aman_Jaiman_Resume.html"
PDF = "/projects/sandbox/resume/Aman_Jaiman_Resume.pdf"
PNG = "/projects/sandbox/resume/preview_full.png"

with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2)
    page.goto("file://" + SRC)
    page.emulate_media(media="print")
    page.pdf(path=PDF, format="A4", print_background=True,
             margin={"top": "11mm", "bottom": "11mm", "left": "11mm", "right": "11mm"})
    page.screenshot(path=PNG, full_page=True)
    b.close()

# split the preview into two readable halves
from PIL import Image  # noqa: E402

im = Image.open(PNG)
w, h = im.size
im.crop((0, 0, w, h // 2)).resize((w // 2, h // 4)).save(PNG.replace("full", "top"))
im.crop((0, h // 2, w, h)).resize((w // 2, h // 4)).save(PNG.replace("full", "bottom"))

from pypdf import PdfReader  # noqa: E402

r = PdfReader(PDF)
pages = len(r.pages)
text = "\n".join(p.extract_text() or "" for p in r.pages)
words = len(text.split())

print(f"PDF pages          : {pages}")
print(f"Extractable words  : {words}  (0 would mean an image-only, ATS-unreadable PDF)")

ok = True
for label, cond in [
    ("PDF is text-based, not scanned/image", words > 500),
    ("Fits on exactly ONE page", pages == 1),
    ("Email survives PDF extraction", bool(re.search(r"amanjaiman001@gmail\.com", text))),
    ("Phone survives PDF extraction", bool(re.search(r"6378722785", text))),
    ("Current role reads as ongoing", "Present" in text),
    ("Education block intact", "Lovely Professional University" in text and "7.4" in text),
    ("All 6 sections present in PDF text",
     all(h.lower() in text.lower() for h in ["Professional Summary", "Technical Skills",
                                             "Professional Experience", "Projects",
                                             "Education", "Achievements"])),
]:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    ok &= bool(cond)

print(f"\nPage 1 fill check: {'SINGLE PAGE' if pages == 1 else f'{pages} pages'}")
sys.exit(0 if ok else 1)
