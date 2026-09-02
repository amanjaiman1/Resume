# Resume rebuild — single page, ATS-clean

## Files

| File | Use it for |
|---|---|
| `Aman_Jaiman_Resume.pdf` | Sending to recruiters / applying. **1 page**, text-based, verified parseable. |
| `Aman_Jaiman_Resume.docx` | Portals that demand Word, and for your own edits. Scores highest on parsers. |
| `Aman_Jaiman_Resume.html` | Source of the PDF. Open in Chrome → Ctrl+P → Save as PDF to regenerate. |
| `Aman_Jaiman_Resume.md` | Plain text, for pasting into application text boxes and LinkedIn. |
| `preview_top.png` / `preview_bottom.png` | Visual preview without opening the PDF. |
| `content.py` + `build.py` | Edit `content.py`, run `python3 build.py`, and all four formats regenerate together. |

**Two commands to verify after any edit:**
- `python3 render_pdf.py` — fails if the resume no longer fits on one page
- `python3 ats_check.py` — 33-point parser audit (currently 33/33)

> The layout is tuned tight to hold one page at 9.5–9.7pt. **If you add a bullet, run `render_pdf.py`
> and confirm it still says SINGLE PAGE before you send it anywhere.** To make room, cut elsewhere
> rather than shrinking the font further — 9.5pt is the readability floor.

---

## VERIFY BEFORE YOU SEND — numbers I could not know

Everything below is **illustrative and written to be replaced with your real figures**. A number you cannot
defend in an interview does more damage than no number at all.

**Stealth venture (the whole section is scaffolding — rewrite it to match what you actually built):**
- 40+ user discovery interviews · 60+ user stories · RICE prioritization · 3 shipped milestones
- 30+ component design system · 40% faster feature build time · 95+ Lighthouse score
- Prisma + PostgreSQL · JWT authentication · GitHub Actions + Vercel · 25% onboarding completion lift

**Optus EdTech:** the 10% engagement lift and 30% task-time reduction came from your old resume. The
**35% load-time reduction**, **25+ components**, and the Figma reference are new — confirm or change them.

**CoderHouse:** **40+ lesson plans** and "raised batch assessment scores" are new. The 300+ students is yours.

**Other assumptions:**
- **Education dates `2020 - 2024`** — inferred from your Apr 2024 job start. Correct if wrong.
- **Degree written as B.Tech** — change if it is B.E. or B.Tech (Hons.).
- **"Remote"** on Optus EdTech and CoderHouse — change to the real city if either was on-site or hybrid.

---

## The employment-continuity question

Your old resume ended at **Apr 2025** with nothing after it. That reads as unemployed for over a year, and
that is exactly what this rewrite fixes.

Your timeline now runs unbroken: `Apr 2024 - Apr 2025` (Optus) → `Apr 2025 - Present` (your venture). No gap,
and the venture is the first and largest block under Experience — so the first thing anyone reads is what you
are building right now, not what you left.

**Your defence exam preparation is deliberately not on the resume.** That is not dishonest: a resume lists
professional work, not everything occupying your time. What makes it hold up is that the venture entry is
genuinely true — you are building a product, you own the product decisions and the frontend.

Two things to keep it credible:

1. **Be ready for "tell me about this venture."** Have a 60-second answer: the problem, who you talked to,
   what you shipped, what you learned, what is next. Vague answers here undo the whole resume.
2. **Make it verifiable.** A live URL, a landing page, or public commits on `github.com/amanjaiman1` turn a
   claim into evidence. If you have a working name for it, use that instead of "Independent Product Venture
   (Stealth)" — a real name reads far stronger than a placeholder.

If asked directly about your plans, saying honestly that you are pursuing defence services alongside building
this is a far better position than being caught having hidden it.

---

## Why this scores as ATS-clean

**Structural fixes (parse safety):**
- Single column, no tables, no text boxes, no images, no header/footer content — the five things that actually
  scramble resume parsers. Your old resume's floating education block was a symptom of exactly this.
- Job title and its dates sit in the *same paragraph*, so a parser can never orphan a date from its role.
- Dates standardised to `Mon YYYY - Mon YYYY`, reverse-chronological throughout.
- Plain hyphen bullets, one standard font (Calibri), no decorative glyphs.
- Headings use names parsers recognise verbatim: Professional Summary, Technical Skills, Professional
  Experience, Projects, Education, Achievements & Recognition.

**The education section — your specific complaint.** It was three floating fragments at the top of page 1
with no degree name and no dates. It is now a proper entry in its own section: degree + field, institution +
city + state, dates, CGPA.

**Content fixes:**
- Added a summary and a `Product Manager | Frontend Engineer` title line, so a keyword scan hits both target
  roles in the first three lines.
- Added a Product Management skills row: roadmapping, PRDs, RICE, A/B testing, analytics, stakeholder
  management, go-to-market. Your old resume had zero PM vocabulary — it could not have matched a PM req.
- Removed the four near-duplicate "optimized performance / improved user experience" bullets at Optus, which
  spent four lines saying one thing.
- Fixed typos from the original: "enhaced" → "enhanced", "Javascript" → "JavaScript".
- Every bullet leads with a distinct action verb, no verb leads more than two bullets, 14 quantified results,
  no first-person pronouns.

---

## What was cut to reach one page

628 words, down from 821 in the two-page draft. Priority went to the two most recent roles.

- **Skills: 6 rows → 4.** Tools merged into "Backend & Tools", CS fundamentals folded into "Languages & CS".
  No keywords lost, three lines saved.
- **Stealth venture: 6 bullets → 4.** Dropped sub-2s LCP, retention cohorts, two-week sprint cadence, and
  role-based access control as standalone points; the strongest four absorbed the rest.
- **Optus EdTech: 6 bullets → 4.** The component-building and workflow-redesign points merged; the
  stakeholder-collaboration bullet was cut as the weakest (no measurable outcome).
- **CoderHouse: 2 bullets → 1**, combining students mentored and lesson plans designed.
- **Projects: 2 bullets each → 1**, with the tech stack and repo link folded onto the end of that bullet.
- **Removed:** the education coursework line, and the "Technical Mentorship" achievement (it duplicated the
  CoderHouse role).
- **Also dropped earlier:** Flutter, Dart, Android Development, plain C, PHP, Ubuntu-as-a-framework — they
  were diluting a frontend/PM-focused skills section.

**To re-add anything,** put it back in `content.py` and cut something of equal length, then confirm
`render_pdf.py` still reports SINGLE PAGE.


---

# Styled template version (the two-column mockup)

You asked for the polished two-column look with the avatar, blue accents, and skill pills. That's built,
matches the mockup, and fits one page — but it is a **different tradeoff** from the plain version, so you now
have two resumes for two different situations.

| File | Look | Font | When to use |
|---|---|---|---|
| `Aman_Jaiman_Resume_Template.pdf` | Two-column, avatar, pills, blue accents | **Rubik** (embedded) | Emailing a human, your portfolio/LinkedIn, recruiters who read the PDF directly |
| `Aman_Jaiman_Resume.pdf` / `.docx` | Single column, plain | Calibri | Uploading into an application portal / ATS (Workday, Taleo, Greenhouse, Lever) |

`template_top.png` / `template_bottom.png` are previews of the styled version.

## The honest ATS tradeoff — read this

The banner on the template says "built to parse more cleanly," and I did build it to parse **as cleanly as a
two-column layout can** — but no two-column resume parses as reliably as a single column, and I won't tell you
otherwise. Here's what I actually verified by extracting text from the generated PDF the way a parser would:

- **Good:** every piece of text is present and machine-readable (not an image), the font is embedded, the
  reading order runs header → full left column → full right column, and email/phone/links/education all
  survive extraction intact.
- **The cost:** the two columns cause the **bullet points to detach from their job titles**. A positional
  parser reads all three job headers, then the education block, then the entire skills column, and only then a
  block of bullets with no clear owner. Modern parsers that match on keywords and section headers (Workday,
  Greenhouse) usually handle this fine; older strict ones (Taleo) can scramble the structure.

**So:** use the styled PDF when a person will read it, and upload the plain `.docx` when a machine will parse
it. Many people keep exactly these two. If a portal only lets you upload one file and you can't tell what it
uses, upload the plain one — a resume that parses correctly beats a pretty one that doesn't.

## Changing the font

The template uses **Rubik** (the font in your mockup), embedded from `fonts/Rubik.ttf` so the PDF is
self-contained. To try a different Google font, drop its `.ttf` into `fonts/`, change the two `@font-face`
`url(...)` filenames and the `font-family` name in `build_template.py`, then run `python3 build_template.py`
and `python3 render_template_pdf.py`. Clean ATS-friendly alternatives that suit this layout: **Inter**,
**Lato**, **Open Sans**, **Source Sans 3**.

## Regenerating

Both versions read from the same `content.py`, so fix a figure once and rebuild both:

```
python3 build.py               # plain: docx + html + md
python3 render_pdf.py          # plain: pdf  (asserts single page)
python3 build_template.py      # styled: html
python3 render_template_pdf.py # styled: pdf (asserts single page + shows parser extraction)
```
