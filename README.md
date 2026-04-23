# Resume Builder

[English](README-en.md)

攒了一堆周报、邮件、课程笔记、旧简历、头像照片，却懒得整理？

把这个 Skill 装好，把资料丢给 Agent，剩下的交给它。在校生的课程笔记、实验报告、项目文档也能自动提取技能和项目经历。

---

### 效果预览

<table>
<tr>
<td align="center">
  <img src="previews/apple.png" width="280"><br><br><b>Apple</b> — 暗色 Hero 头部，大字体，卡片网格，蓝色链接
</td>
<td align="center">
  <img src="previews/minimal.png" width="280"><br><br><b>Minimal</b> — 居中排版，底部分割线，左侧边框强调
</td>
</tr>
<tr>
<td align="center">
  <img src="previews/corporate.png" width="280"><br><br><b>Corporate</b> — 橙色强调，彩色区块标题栏，箭头项目符号
</td>
<td align="center">
  <img src="previews/pulse.png" width="280"><br><br><b>Pulse</b> — 暗亮交替区块，技能进度条，动态光晕
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

装完就开始聊：

> 帮我把这些周报和邮件整理成一份简历
>
> 用我的课程笔记和实验报告提取一份在校生简历

生成好了还能接着调：

> 换成 corporate 风格，看着正式一点
>
> 色调再活泼一些
>
> 翻译成英文版
>
> 导出成 PDF

就这么简单。

---

### 它能做什么

| 能力 | 说明 |
|------|------|
| 多源提取 | .eml / .msg / .html / .txt / .md / .jpg / .png 通吃 |
| 在校生友好 | 课程笔记、实验报告、项目文档自动提取技能和项目经历 |
| 职业指南 | 计算机科学 · 人力资源 · 市场运营 |
| 样式主题 | apple · minimal · corporate · pulse |
| 头像处理 | 自动找头像，居中裁剪，Base64 嵌入 |
| 多格式输出 | HTML + Markdown + PDF |

---

### 自定义样式

内置四个风格不够用？自己加一个新主题到 `assets/styles/` 就行，欢迎 PR。
