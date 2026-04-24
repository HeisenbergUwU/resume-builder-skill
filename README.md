# Resume Builder

[English](README-en.md)

把周报、邮件、课程笔记、旧简历和照片交给 AI，几分钟生成一份精美简历。

支持一键提取、自动排版，换风格、翻译、导出 PDF 都能一句话完成。

---

### 效果预览

<table>
<tr>
<td align="center">
  <img src="previews/apple.png" width="280"><br><br><b>Apple</b> — 暗色头部，大字体，卡片网格
</td>
<td align="center">
  <img src="previews/minimal.png" width="280"><br><br><b>Minimal</b> — 居中排版，左侧边框强调
</td>
</tr>
<tr>
<td align="center">
  <img src="previews/corporate.png" width="280"><br><br><b>Corporate</b> — 橙色强调，箭头项目符号
</td>
<td align="center">
  <img src="previews/heisenberg.png" width="280"><br><br><b>Heisenberg</b> — 头像并排，柔和蓝色，圆润卡片
</td>
</tr>
</table>

---

### 安装

选一个你用的工具：

**🚀 Hermes:**
```bash
git clone https://github.com/HeisenbergUwU/resume-builder-skill.git ~/.hermes/skills/resume-builder
```

**🦞 OpenClaw:**
```bash
git clone https://github.com/HeisenbergUwU/resume-builder-skill.git ~/.openclaw/skills/resume-builder
```

**💻 Cursor / Claude Code / 通用:**
```bash
git clone https://github.com/HeisenbergUwU/resume-builder-skill.git skills/resume-builder
```

---

### 怎么用

装好之后，把资料发给 Agent 就行了：

> 帮我把这些周报和邮件整理成一份简历
>
> 用我的课程笔记和实验报告提取一份在校生简历

生成后一句话就能调整：

> 换成 corporate 风格，看着正式一点
>
> 翻译成英文版
>
> 导出成 PDF

---

### 能力一览

| 能力 | 说明 |
|------|------|
| 多源提取 | .eml / .msg / .html / .txt / .md / .jpg / .png 全部支持 |
| 自动渲染 | 旧简历 Markdown 纯脚本拼接 HTML，无需大模型 |
| 在校生友好 | 课程笔记、实验报告自动提取技能和项目经历 |
| 职业指南 | 计算机科学 · 人力资源 · 市场运营 |
| 样式主题 | apple · minimal · corporate · heisenberg · pulse |
| 头像处理 | 自动发现、居中裁剪、Base64 内嵌 |
| 多格式输出 | HTML + Markdown + PDF |

---

### 自定义样式

内置主题不够？把 CSS + 模板放到 `assets/styles/<name>/` 下即可生效，欢迎 PR。
