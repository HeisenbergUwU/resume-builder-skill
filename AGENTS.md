# AGENTS.md — Resume Builder Skill

## What This Is

A Hermes/OpenClaw agent skill, not a conventional software project. No build system, no tests, no CI. Everything is pure Python scripts + HTML/CSS templates.

## Where Everything Lives

| Path | Purpose |
|------|---------|
| `SKILL.md` | **The single source of truth.** Complete workflow, rules, and conventions. Read it first. |
| `scripts/` | 6 scripts (4 standalone + 1 renderer + 1 orchestrator) |
| `assets/styles/<name>/` | Per-style CSS + EN/CN HTML templates |
| `references/<career>/` | Per-career resume writing guides (EN + CN) |

## Scripts

| Script | What it does | Key deps |
|--------|-------------|----------|
| `scripts/pipeline.py` | **Orchestrator.** Runs all scripts in sequence. All paths configurable via CLI args (`--dir`, `--output-dir`, `--resume`, `--style`). | none |
| `scripts/extract_sources.py` | Categorizes files from zip/dir into avatars, reports, docs. Auto-picks best avatar. Writes `extracted_manifest.json`. | none (stdlib) |
| `scripts/extract_text.py` | Extracts plain text from .eml/.msg/.html/.txt/.md. JSON output with `--json`. Skips binary files (zip, images, etc). | `msgreader` (optional, for .msg) |
| `scripts/render_resume.py` | **Auto-render.** Parses `个人简历.md` → structured JSON, fills HTML template, extracts keywords from weekly reports. No LLM needed. | none (stdlib) |
| `scripts/embed_avatar.py` | Center-crops avatar, Base64-embeds into HTML. | `Pillow` (optional; falls back to raw embed) |
| `scripts/html_to_pdf.py` | HTML → PDF via weasyprint > wkhtmltopdf > chromium. | `weasyprint` (recommended) |

## Critical Rules from SKILL.md (Easy to Miss)

- **Language matching:** User's language dictates guide file (`*-guide.md` vs `*-guide-cn.md`), HTML template (`resume-html.html` vs `resume-html-cn.html`), and all generated content. Default to English.
- **Footer:** Must be empty or removed. Never write "Generated from..." or any attribution.
- **No fabrication:** Never invent metrics, companies, or leadership roles. Use "约" / "approximately" for estimates.
- **Deep-dive:** Always expand the most recent 2 entries (employers for pros, projects for students) using the elevate framework. Other entries stay concise.
- **Deliverables:** Always produce 3 files: `.html` (single-file, inline CSS, Base64 avatar), `.md`, and `.pdf`.

## Adding a New Style

Create `assets/styles/<name>/` with 3 files:
- `resume-css.css` — the styles
- `resume-html.html` — English HTML skeleton
- `resume-html-cn.html` — Chinese HTML skeleton

Use the same CSS class names as existing styles (`.header`, `.job-card`, `.skills-grid`, `.edu-table`, etc.) so avatar embedding and data injection work.

## Prerequisites

```bash
pip install Pillow          # avatar cropping (optional but recommended)
pip install weasyprint      # PDF generation (recommended)
pip install msgreader       # .msg support (optional)
```
