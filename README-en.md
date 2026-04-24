# Resume Builder

[中文版](README.md)

Turn weekly reports, emails, class notes, old resumes, and photos into a polished resume in minutes.

Auto-extract, auto-layout, swap themes, translate, and export to PDF — all with a single message.

---

### Preview

<table>
<tr>
<td align="center">
  <img src="previews/apple.png" width="280"><br><br><b>Apple</b> — Dark hero header, large typography, card grid
</td>
<td align="center">
  <img src="previews/minimal.png" width="280"><br><br><b>Minimal</b> — Centered layout, left-border accents
</td>
</tr>
<tr>
<td align="center">
  <img src="previews/corporate.png" width="280"><br><br><b>Corporate</b> — Orange accent, arrow bullets
</td>
<td align="center">
  <img src="previews/heisenberg.png" width="280"><br><br><b>Heisenberg</b> — Side-by-side avatar, soft blue, rounded cards
</td>
</tr>
</table>

---

### Install

Pick your tool:

**🚀 Hermes:**
```bash
git clone https://github.com/HeisenbergUwU/resume-builder-skill.git ~/.hermes/skills/resume-builder
```

**🦞 OpenClaw:**
```bash
git clone https://github.com/HeisenbergUwU/resume-builder-skill.git ~/.openclaw/skills/resume-builder
```

**💻 Cursor / Claude Code / Generic:**
```bash
git clone https://github.com/HeisenbergUwU/resume-builder-skill.git skills/resume-builder
```

---

### How to Use

Once installed, just send your materials to the agent:

> Turn these weekly reports and emails into a resume
>
> Extract skills and build a student resume from my class notes and lab reports

Then iterate with follow-ups:

> Switch to corporate style, make it more professional
>
> Translate to Chinese
>
> Export as PDF

---

### Features

| Feature | Description |
|---------|-------------|
| Multi-source | .eml / .msg / .html / .txt / .md / .jpg / .png — all supported |
| Auto-render | Markdown resumes compiled to HTML via script, no LLM needed |
| Student-friendly | Class notes and lab reports auto-extracted into skills and projects |
| Career Guides | Computer Science · Human Resources · Marketing |
| Style Themes | apple · minimal · corporate · heisenberg · pulse |
| Avatar | Auto-discover, center-crop, Base64 embed |
| Multi-format | HTML + Markdown + PDF |

---

### Custom Styles

Built-in themes not enough? Drop your CSS + templates under `assets/styles/<name>/` and PR it back.
