# Resume Builder

[中文版](README.md)

**Build a polished resume from your materials (email reports, old resumes, photos etc.), outputting both HTML and Markdown versions.**

HTML version uses inline CSS + Base64 avatar. No dependencies. Opens in browser, email-safe, print-ready.

---

### Install

```bash
git clone https://github.com/HeisenbergUwU/resume-builder-skill.git skills/resume-builder
```

### Prompt Examples

After installing, use in conversation:

**Generate a resume from your materials:**
> Build a resume from my materials, output both HTML and Markdown
> Turn these documents into a resume for me

**Tech roles:**
> Extract my weekly reports into a resume for backend developer, apple style

**HR roles:**
> Build me an HR resume from these materials, highlight recruitment and employee relations, corporate style

**Marketing roles:**
> I have scattered emails and docs, build a growth marketing resume, minimal style

**Multi-language:**
> Translate the resume above into Chinese

### Features

| Feature | Description |
|---------|-------------|
| Multi-source | .eml / .msg / .html / .txt / .md / .jpg / .png |
| Career Guides | Computer Science · Human Resources · Marketing |
| Style Themes | apple · minimal · corporate |
| Avatar | Auto-select + center-crop + Base64 embed |
