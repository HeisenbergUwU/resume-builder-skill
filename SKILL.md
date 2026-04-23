---
name: resume-builder
description: Build a polished single-file HTML resume from scattered historical data. Supports packing up materials from .eml emails, .msg Outlook files, .txt/.html reports, old resumes, and photos into a single resume. Includes resume writing guides for multiple career paths (computer science, human resources, marketing) and swappable CSS style themes (apple, minimal, corporate). Avatar is auto-cropped and Base64-embedded for offline use.
version: 1.0.0
author: community
license: MIT
prerequisites:
  commands: [python3]
  pip_deps: [Pillow]
metadata:
  hermes:
    tags: [resume, HTML, multi-source, data-extraction, writing-guide, swappable-styles, productivity]
    category: productivity
---

# Resume HTML Builder — Multi-source Resume Generator

Build a modern, single-file HTML resume from scattered historical data (.eml reports, old resumes, photos, publications).

## When to Use

- User wants to rebuild a resume from scattered materials (weekly reports, old resumes, etc.)
- User asks to pack up their materials and generate a resume (zip or directory)
- Converting Markdown/PDF resume to a single-file HTML
- Need avatar cropping + Base64 embedding for offline viewing
- Multi-career resume writing guidance (tech, HR, etc.)
- Multi-style design choices (apple, minimal, corporate)
- Multi-source data extraction and merging

## Typical User Prompts

These are the most common ways users trigger this skill:

| Prompt | What happens |
|--------|-------------|
| "把周报打包成一份简历" | Extract .eml/.txt, merge, render HTML |
| "把我的资料整理成简历" | Categorize files, extract text, draft resume |
| "用这些材料帮我生成一份简历" | Full pipeline: extract → draft → style → deliver |
| "把旧简历转成 HTML 格式" | Parse existing resume, apply chosen theme |

## Language Rule (IMPORTANT)

Match the user's input language throughout the entire workflow:

| User speaks | Guide | HTML template | Resume content |
|-------------|-------|---------------|----------------|
| English | `*-guide.md` | `resume-html.html` | English |
| 中文 | `*-guide-cn.md` | `resume-html-cn.html` | 中文 |

If the user doesn't specify, default to English. This applies to every step — guide selection, template selection, and all generated resume content.

## Workflow

```
Collect sources → Extract data → Deduplicate & merge → Draft → Render HTML → Embed avatar → Deliver
```

## Prerequisites

```bash
pip install Pillow
```

## Step 1: Extract and Categorize Source Data

User typically provides a zip archive. Supported file types:

| Extension | Content | How it's read |
|-----------|---------|---------------|
| `.eml` | Standard email (Thunderbird/Mail.app export) | MIME parser |
| `.msg` | Outlook email | `extract-msg` (pip install) |
| `.txt`, `.text` | Plain text reports | Direct read |
| `.html`, `.htm` | HTML emails/reports | Tag stripped |
| `.md`, `.sg`, `.pdf` | Old resume drafts, notes | Text/pdf parser |
| `.jpg`, `.png` | Avatar photos | Image picker |

```bash
# From zip
python scripts/extract_sources.py --zip "resume-sources.zip" --output extracted

# From directory
python scripts/extract_sources.py --dir /path/to/sources
```

Outputs categorized file lists + JSON. Auto-selects best avatar (prefers `avatar`/`photo`/`head` in filename, else largest file).

**Supported email formats:**
- `.eml` — standard MIME (Thunderbird, Mail.app, generic export) — no extra deps
- `.msg` — Outlook format — needs `pip install extract-msg`
- `.txt` / `.html` — plain text or HTML saved from email clients — direct read

## Step 2: Extract Text from Reports

The script converts any file to readable text — it does **not** structure content.

```bash
# Single file
python scripts/extract_text.py report.eml

# Directory of reports
python scripts/extract_text.py reports/ --json

# Recursive
python scripts/extract_text.py reports/ -r --json
```

**Output format (JSON):**
```json
[{"filename": "report.eml", "content": "From: ...\nSubject: ...\n\nBody content..."}]
```

**Agent interprets the text:** Feed the `content` to yourself and use natural language understanding to extract dates, subjects, key achievements, and metrics. The script handles MIME decode, HTML tag stripping, and encoding — you handle meaning.

**Supported formats:**
- `.eml` — standard MIME email — no extra deps
- `.msg` — Outlook — needs `pip install extract-msg`
- `.html` / `.htm` — auto-stripped to text
- `.txt` / `.md` / `.sg` / anything else — direct read

## Step 3: Extract from Old Resumes

Markdown: parse `#` section headers and group content under each.

PDF: use the `ocr-and-documents` skill (pymupdf or marker-pdf).

## Step 4: Select Career Path and Draft Resume Content

Pick a career path from `references/<career>/resume-guide.md` (EN) or `resume-guide-cn.md` (CN).

| Career Path | Focus | Guide path |
|-------------|-------|-----------|
| **Computer Science** (default) | FAB pattern, per-stack focus (backend/frontend/mobile/C++/Go/architecture), ATS keywords | `references/computer-science/` |
| **Human Resources** | Recruitment metrics, employee relations, HRBP alignment, labor compliance | `references/human-resources/` |
| **Marketing** | Growth metrics (CAC/ROI/LTV), brand campaigns, user ops, content marketing, GTM | `references/marketing/` |

**Language:** Use English guide if user speaks English, Chinese guide (`-cn.md`) if user speaks 中文. Default to `computer-science` if role is unclear.

**Adding a career path:** Create `references/<career>/resume-guide.md` + `resume-guide-cn.md`. Cover: key metrics to emphasize, per-role focus areas, ATS keywords, and concrete before/after writing examples.

**Key merge principles:**
- **Timeline alignment:** Match report dates to employment periods for correct attribution
- **Deduplication:** Merge overlapping weekly report content
- **Role evolution:** Highlight promotions (e.g., "Engineer → Lead")
- **Quantify:** Extract metrics (users, performance gains, data volume)

## Step 5: Choose Style and Render HTML

Styles live under `assets/styles/<name>/` — each has `resume-css.css` + `resume-html.html` (EN) or `resume-html-cn.html` (CN).

| Style | Description |
|-------|-------------|
| **apple** (default) | Clean, white/gray, subtle shadows, rounded cards |
| **minimal** | White background, serif fonts, left-border accents, print-optimized |
| **corporate** | Navy header, sharp edges, structured cards, professional tone |

**Pick a style and render:**

1. Read `assets/styles/<name>/resume-html.html` (EN) or `resume-html-cn.html` (CN) for the HTML skeleton
2. Read `assets/styles/<name>/resume-css.css` and paste into the `<style>` block
3. Replace placeholder content with extracted data

> If user doesn't specify a style, ask. Default to `apple`.

**Adding a new style:** Create `assets/styles/<name>/` with `resume-css.css`, `resume-html.html`, and `resume-html-cn.html`. Use the same HTML class names (`.header`, `.job-card`, `.skills-grid`, `.edu-table`, etc.) so data injection works across all styles.

## Step 6: Crop and Embed Avatar

```bash
# Center-crop + Base64 embed (default 100x100px)
python scripts/embed_avatar.py avatar.jpg resume.html

# Custom size
python scripts/embed_avatar.py avatar.jpg resume.html --size 120 -o final.html
```

The script center-crops to a square and resizes — the avatar stays centered in the circular frame regardless of original aspect ratio.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `h1` invisible — gradient + `transparent` fill | Use `color: var(--text)` directly, no gradient clip |
| Avatar path breaks offline use | Always Base64 data URI, never external reference |
| Avatar/text overlap on mobile | `flex-direction: column` + `align-items: center` below 640px |
| CSS `:root` variables lost during template injection | Ensure `:root` block is at the top of `<style>` |
| Duplicate/conflicting timeline data | Sort by date first, deduplicate, then extract |
| CJK text rendering | Include `'Noto Sans SC'` in `font-family`, ensure `<meta charset="UTF-8">` |
| Email charset detection fails | Try `part.get_content_charset()` first, fallback to `utf-8` |

## Color Reference (Apple Style)

| Use | Value |
|-----|-------|
| Background | `#f5f5f7` (Apple light gray) |
| Card | `#ffffff` |
| Border | `#d5d5da` |
| Primary text | `#1d1d1f` |
| Secondary text | `#86868b` |
| Links/accent | `#0071e3` (Apple Blue) |
| Metrics | `#34a853` (green) |
| Tags/badges | `#ff9500` (orange) |

## Deliverable

`resume-name-final.html` — single file with inline CSS + HTML + Base64 avatar. No external dependencies, opens directly, email-safe, print-ready.
