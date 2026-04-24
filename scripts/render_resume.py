#!/usr/bin/env python3
"""Render a single-file HTML resume from structured data + optional weekly reports.

Pure template filling — no LLM needed.

Usage:
  python scripts/render_resume.py --resume markdown.md --style apple --output resume.html
  python scripts/render_resume.py --resume markdown.md --style apple --texts extracted_texts.json
  python scripts/render_resume.py --resume markdown.md --style minimal --output-dir ./output
"""

import argparse
import base64
import json
import os
import re
import sys
from datetime import datetime
from html import escape


def _clean_bullet(text):
    """Clean bullet text: remove <br/>, leading markers, trim."""
    text = re.sub(r'<br\s*/?>', '', text)
    text = re.sub(r'^\s*(?:\d+\.\s*|\+\s*|[★●•]\s*)', '', text)
    text = re.sub(r'\s*>\s*', ' ', text)
    text = text.strip()
    # Skip citation/quote lines
    if not text or text.startswith('>') or text.startswith('**'):
        return ''
    return text


SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPTS_DIR, '..', 'assets')

# Keywords to extract from weekly reports
TECH_KEYWORDS = [
    # AI/ML
    'LLM', 'Agent', 'SFT', 'RAG', 'Dify', 'LangChain', 'LLaMA', 'Qwen',
    'ChatGLM', 'DeepSeek', 'Phi3', 'SAM', 'U2Net', 'YOLO', 'PyTorch',
    'TensorFlow', 'Transformers', 'vLLM', 'TGI', 'onnx', 'LoRA',
    # Backend
    'Spring', 'SpringCloud', 'FastAPI', 'Flask', 'Django', 'MyBatis',
    'Redis', 'MySQL', 'MongoDB', 'PostgreSQL', 'Elasticsearch', 'ES',
    # Infra
    'Docker', 'K8s', 'Kubernetes', 'CI/CD', 'Nginx', 'Linux',
    'Git', 'GitHub', 'Jenkins', 'Prometheus', 'Grafana',
    # Frontend
    'React', 'Vue', 'NextJS', 'Next.js', 'TypeScript', 'JavaScript',
    # Cloud
    'AWS', 'GCP', 'Azure', 'Alibaba', 'Tencent',
    # Data
    '爬虫', 'crawling', 'scrapy', 'Playwright', 'Selenium',
]

# Chinese keywords for business impact
BUSINESS_KEYWORDS = [
    '部署', '上线', '优化', '重构', '提升', '降低', '改进', '修复',
    '完成', '实现', '开发', '设计', '管理', '协调', '主导',
]


def parse_resume_md(md_path):
    """Parse the Markdown resume into structured data.

    Resume format: table with 4 columns per row.
    Row 0: name/info (merged cells)
    Row 1: separator (---)
    Row 2: contact info (phone | email | target position)
    Row 3: **教育经历** (section header)
    Row 4: time | school | dept | degree
    Row 5: courses/details (merged)
    ...alternating data/detail rows...
    Row N: **工作经历** (section header)
    Row N+1: time | company | dept | role
    Row N+2: bullet content (merged, + and <br/> separated)
    ...alternating...
    Row M: **核心项目、作品** (section header)
    Row M+N: **Name  time**<br/>description<br/>1. bullet<br/>2. bullet...
    Row K: **个人兴趣项目** (section header)
    Row K+1: + item1<br/>+ item2<br/>...
    """
    if not os.path.isfile(md_path):
        print(f"ERROR: Resume file not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    with open(md_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        raw = f.read()

    # Strip image markdown
    raw = re.sub(r'<!--.*?-->', '', raw)
    raw = re.sub(r'!\[.*?\]\(.*?\)', '', raw)

    # Parse table rows
    rows = []
    for line in raw.split('\n'):
        line = line.strip()
        if not line.startswith('|') or re.match(r'^\s*\|\s*---\s*\|', line):
            continue
        # Remove leading/trailing |
        inner = line.strip('|').strip()
        if not inner:
            continue
        cells = [c.strip() for c in inner.split('|')]
        # Normalize: ensure 4 cells
        while len(cells) < 4:
            cells.append('')
        rows.append(cells)

    data = {
        'name': '',
        'phone': '',
        'email': '',
        'github': '',
        'summary': '',
        'tags': [],
        'skills': [],
        'education': [],
        'work': [],
        'projects': [],
        'interests': [],
    }

    # Row 0: name row (may be merged cell with name + summary)
    # Find the first row with actual content
    first_row_idx = 0
    for ri, row in enumerate(rows):
        full = ' '.join(row)
        if full.strip() and not re.match(r'^[\s*\-|]*$', full):
            first_row_idx = ri
            break

    full = ' '.join(rows[first_row_idx]) if rows else ''

    # Name from bold markers (with possible spaces between Chinese chars)
    name_match = re.search(r'\*\*\s*([\u4e00-\u9fff][ \u4e00-\u9fff]{0,3})\s*\*\*', full)
    if name_match:
        data['name'] = name_match.group(1).replace(' ', '')
    else:
        # Fallback: find first 2+ Chinese chars
        name_match = re.search(r'([\u4e00-\u9fff][ \u4e00-\u9fff]{0,3})', full)
        if name_match:
            data['name'] = name_match.group(1).replace(' ', '')

    # GitHub from name row
    gh_match = re.search(r'github\.com/([\w-]+)', full)
    if gh_match:
        data['github'] = gh_match.group(1)

    # Row 1 (or first_row_idx+1): contact info
    contact_row_idx = first_row_idx + 1
    if len(rows) > contact_row_idx:
        contact_full = ' | '.join(rows[contact_row_idx])
        phone_match = re.search(r'手机[:：]?\s*(\d{11})', contact_full)
        if phone_match:
            data['phone'] = phone_match.group(1)
        email_match = re.search(r'邮箱[:：]?\s*([\w.+-]+@[\w-]+\.[\w.]+)', contact_full)
        if email_match:
            data['email'] = email_match.group(1)
        tag_match = re.search(r'期望岗位[:：]?\s*([^|]+)', contact_full)
        if tag_match:
            data['tags'].append(tag_match.group(1).strip())

    # Summary from name row (age, years of experience, etc.)
    summary_match = re.search(r'(\d+年工作经验[^|]*)', full)
    if summary_match:
        summary = summary_match.group(1).strip()
        summary = re.sub(r'\[.*?\]\(.*?\)', '', summary)
        summary = re.sub(r'<br\s*/?>', '', summary).strip()
        data['summary'] = summary

    # Walk through rows, tracking section
    # Start after name row + contact row
    i = contact_row_idx + 1
    current_section = None
    pending_work_header = None

    while i < len(rows):
        cell0 = rows[i][0]
        full = ' '.join(rows[i])

        # Detect section headers (bold text in first cell)
        if '**教育经历**' in cell0 or '**教育背景**' in cell0:
            current_section = 'education'
            pending_work_header = None
            i += 1
            continue
        elif '**工作经历**' in cell0:
            current_section = 'work'
            pending_work_header = None
            i += 1
            continue
        elif '**专业技能**' in cell0:
            current_section = 'skills'
            pending_work_header = None
            i += 1
            continue
        elif '**业务能力**' in cell0:
            current_section = 'abilities'
            pending_work_header = None
            i += 1
            continue
        elif '**核心项目' in cell0 or '**项目' in cell0:
            current_section = 'projects'
            pending_work_header = None
            i += 1
            continue
        elif '个人兴趣项目' in cell0 or '**个人兴趣' in cell0:
            current_section = 'interests'
            pending_work_header = None
            i += 1
            continue

        # Process data rows
        if current_section == 'education':
            _parse_edu_row(data, rows[i])
        elif current_section == 'work':
            _parse_work(data, rows[i], pending_work_header)
            if pending_work_header and not pending_work_header.get('time_set'):
                pending_work_header['time_set'] = True
        elif current_section == 'skills':
            _parse_skills(data, rows[i])
        elif current_section == 'abilities':
            _parse_abilities(data, rows[i])
        elif current_section == 'projects':
            _parse_project(data, rows[i])
        elif current_section == 'interests':
            _parse_interests(data, rows[i])

        i += 1

    return data


def _parse_edu_row(data, row):
    """Parse education data or detail row."""
    full = ' '.join(row)
    cells = row

    # Check if this is a detail row (courses)
    if '主修课程' in full or '**主修' in full:
        if data['education']:
            detail = full
            detail = re.sub(r'\*\*主修课程\*\*[：:]\s*', '', detail)
            detail = re.sub(r'主修课程[：:]\s*', '', detail)
            detail = re.sub(r'<br\s*/?>', ' ', detail)
            detail = re.sub(r'\s*>\s*', ' ', detail)
            detail = detail.strip()
            if detail:
                data['education'][-1].setdefault('details', '')
                if data['education'][-1]['details']:
                    data['education'][-1]['details'] += '; '
                data['education'][-1]['details'] += detail
        return

    # Data row: time | school | dept | degree
    time_match = re.search(r'(\d{4}\.\d{1,2}\s*~\s*\d{4}\.\d{1,2})', full)
    school = cells[1].strip() if len(cells) > 1 else ''
    dept = cells[2].strip() if len(cells) > 2 else ''
    degree_raw = cells[3].strip() if len(cells) > 3 else ''

    edu = {
        'time': time_match.group(1).replace('.', '-').replace(' ', '') if time_match else '',
        'school': school,
        'dept': dept,
        'degree': '',
    }

    if '硕士' in degree_raw:
        edu['degree'] = '硕士'
    elif '博士' in degree_raw:
        edu['degree'] = '博士'
    elif '学士' in degree_raw:
        edu['degree'] = '学士'

    if edu['school']:
        data['education'].append(edu)


def _parse_work(data, row, pending):
    """Parse work entry: header row (time|company|dept|role) or bullet row."""
    full = ' '.join(row)
    cells = row

    # Is this a bullet row?
    if full.startswith('+') or full.startswith(' +'):
        # Append bullets to last work entry
        if data['work']:
            # Split by <br/>
            parts = re.split(r'<br\s*/?>', full)
            for part in parts:
                bullet = _clean_bullet(part)
                if bullet:
                    data['work'][-1]['bullets'].append(bullet)
        return

    # Is this a header row? (has time pattern in first cell)
    time_match = re.search(r'(\d{4}[\.\-]\d{1,2}\s*(?:~|至|-)\s*(?:\d{4}[\.\-]\d{1,2}|\d{4}[\.\-]\s*今|今|至今))', cells[0])

    if time_match:
        time_str = time_match.group(1).replace('.', '-').replace(' ', '')
        time_str = re.sub(r'(今|至今)', 'Present', time_str)
        time_str = re.sub(r'至', '-', time_str)

        company = cells[1].strip() if len(cells) > 1 else ''
        dept = cells[2].strip() if len(cells) > 2 else ''
        role_raw = cells[3].strip() if len(cells) > 3 else ''

        # Clean company name
        company = re.sub(r'【[^】]*】', '', company).strip()

        work = {
            'time': time_str,
            'company': company,
            'dept': dept,
            'role': role_raw,
            'bullets': [],
        }
        data['work'].append(work)
    else:
        # Could be bullet content in merged cell
        if data['work']:
            parts = re.split(r'<br\s*/?>', full)
            for part in parts:
                bullet = _clean_bullet(part)
                if bullet:
                    data['work'][-1]['bullets'].append(bullet)


def _parse_skills(data, row):
    """Parse skill row: **Label：**value**Label2：**value2..."""
    full = ' '.join(row)

    # Find all bold labels with content
    skills = re.findall(r'\*\*([^*]+)\*\*[：:]\s*([^*<]+(?:<br\s*/?>\s*\*\*[^*]+\*\*[：:]\s*[^*<]+)*)', full)
    if not skills:
        # Simpler pattern
        skills = re.findall(r'\*\*([^*]+)\*\*[：:]\s*(.+?)(?=\*\*|$)', full)

    for label, value in skills:
        value = re.sub(r'<br\s*/?>', ' ', value).strip()
        data['skills'].append({
            'label': label.strip(),
            'value': value,
        })


def _parse_abilities(data, row):
    """Parse ability row (merged into skills as tags)."""
    full = ' '.join(row)

    # Extract ability items
    abilities = re.findall(r'\*\*([^*]+)\*\*[：:]\s*(.+?)(?=\*\*|$)', full)
    for label, value in abilities:
        value = re.sub(r'<br\s*/?>', ' ', value).strip()
        if label and value:
            data['skills'].append({
                'label': label.strip(),
                'value': value,
            })


def _parse_project(data, row):
    """Parse project row: **Name  time**<br/>description<br/>1. bullet<br/>2. ..."""
    full = ' '.join(row)

    # Project name + time (bold at start)
    name_match = re.search(r'\*\*([^*]{3,40})\*\*', full)
    if not name_match:
        return

    name_and_time = name_match.group(1).strip()

    # Separate name from time
    time_match = re.search(r'(\d{4}[\.\-]\d{1,2}\s*(?:~|-)?\s*(?:\d{4}[\.\-]\d{1,2}|\d{4}[\.\-]\s*今|今|至今|Now|now))', name_and_time)
    if time_match:
        time_str = time_match.group(1).replace('.', '-').replace(' ', '')
        project_time = re.sub(r'(今|至今)', 'Present', time_str, flags=re.I)
        project_name = name_and_time[:time_match.start()].strip()
    else:
        project_time = ''
        project_name = name_and_time

    # Description (text after bold, before numbered bullets)
    after_name = full[name_match.end():]
    after_name = re.sub(r'^<br\s*/?>', '', after_name)

    # Numbered bullets
    bullets = re.findall(r'\d+\.\s*(.+?)(?:\s*\d+\.\s*|$)', after_name)

    # Links
    links = re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', full)

    if not bullets:
        # + bullets
        bullets = re.findall(r'\+\s*(.+?)(?:\+\s*|$)', after_name)

    if not bullets:
        # Try <br/> separated items
        parts = re.split(r'<br\s*/?>', after_name)
        for part in parts:
            part = part.strip()
            if part and len(part) > 10:
                bullets.append(part)

    # Clean up bullet text
    bullets = [_clean_bullet(b) for b in bullets]
    bullets = [b for b in bullets if b]

    # Citation line
    cite_match = re.search(r'>(\s*(?:He|Lei|作者)[^<]+)', full)
    citation = cite_match.group(1).strip() if cite_match else ''

    project = {
        'name': project_name,
        'time': project_time,
        'bullets': [b.strip() for b in bullets if b.strip()],
        'link': links[0][1] if links else '',
    }
    if citation:
        project['citation'] = citation

    data['projects'].append(project)


def _parse_interests(data, row):
    """Parse interest row: + name：link<br/>+ name：link"""
    full = ' '.join(row)

    parts = re.split(r'<br\s*/?>', full)
    for part in parts:
        part = re.sub(r'^\s*\+\s*', '', part).strip()
        if not part:
            continue

        # Extract name and link
        name_link = re.match(r'([^：:\s]+)[:：]\s*(.*)', part)
        if name_link:
            interest = {'name': name_link.group(1).strip()}
            link_text = name_link.group(2).strip()
            link_match = re.search(r'(https?://[\w\.\-_/]+)', link_text)
            if link_match:
                interest['link'] = link_match.group(1)
            data['interests'].append(interest)
        elif part:
            data['interests'].append({'name': part})


def extract_keywords_from_texts(texts_path):
    """Extract keywords and metrics from weekly reports, grouped by employer.

    Auto-detects employers from the resume data by parsing work entry dates.
    """
    if not texts_path or not os.path.isfile(texts_path):
        return {}

    with open(texts_path, 'r', encoding='utf-8') as f:
        texts = json.load(f)

    # Parse dates from work entries to build employer ranges
    # Work entries come from parsed resume_data.json or manifest
    employer_ranges = {}
    for entry in texts:
        content = entry.get('content', '') or ''
        if '工作经历' in content or '**工作经历**' in content:
            # Extract employer + time info from content
            pass

    # Fallback: group all keywords globally (no employer grouping)
    # This is simpler and works for any resume
    all_keywords = set()
    for entry in texts:
        content = entry.get('content', '') or ''
        for kw in TECH_KEYWORDS:
            if kw in content:
                all_keywords.add(kw)

    return {'all': sorted(list(all_keywords))}


def extract_business_highlights(texts_path):
    """Extract notable business actions from weekly reports."""
    if not texts_path or not os.path.isfile(texts_path):
        return []

    with open(texts_path, 'r', encoding='utf-8') as f:
        texts = json.load(f)

    highlights = []
    for entry in texts:
        content = entry.get('content', '') or ''
        fname = entry.get('filename', '')

        # Look for impactful lines
        for line in content.split('\n'):
            line = line.strip()
            if not line or len(line) < 10:
                continue
            # Skip email headers
            if line.startswith(('From:', 'To:', 'Subject:', 'Date:', 'boundary')):
                continue
            # Skip empty bullet markers
            if line in ['*', '+', '-', '进度', '进度：主要跟进 HyperAI 相关工作']:
                continue

            # Lines with metrics are valuable
            has_metric = bool(re.search(r'\d+%', line) or re.search(r'\d+万', line) or
                            re.search(r'\d+人', line) or re.search(r'提升|降低|优化', line))
            if has_metric:
                highlights.append({
                    'text': line,
                    'date': fname,
                })

    return highlights[:20]  # Limit to 20 most impactful


def render_html(data, style, keywords=None):
    """Render HTML from structured data using the chosen style template."""
    style_dir = os.path.join(ASSETS_DIR, 'styles', style)

    # Read CSS
    css_path = os.path.join(style_dir, 'resume-css.css')
    if not os.path.isfile(css_path):
        print(f"ERROR: CSS not found: {css_path}", file=sys.stderr)
        sys.exit(1)
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()

    # Read template
    tmpl_path = os.path.join(style_dir, 'resume-html-cn.html')
    if not os.path.isfile(tmpl_path):
        tmpl_path = os.path.join(style_dir, 'resume-html.html')
    if not os.path.isfile(tmpl_path):
        print(f"ERROR: Template not found in {style_dir}", file=sys.stderr)
        sys.exit(1)

    # Build HTML sections
    html = build_html(data, css, keywords)
    return html


def build_html(data, css, keywords=None):
    """Build the full HTML string."""
    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="zh-CN">')
    parts.append('<head>')
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    parts.append(f'<title>{escape(data["name"])} - 简历</title>')
    parts.append('<style>')
    parts.append(css)
    parts.append('</style>')
    parts.append('</head>')
    parts.append('<body>')
    parts.append('<div class="container">')

    # Header
    parts.append(build_header(data))

    # Skills
    if data['skills']:
        parts.append(build_skills(data['skills']))

    # Work experience
    if data['work']:
        parts.append(build_work(data['work'], keywords))

    # Projects (if any, separate from work)
    if data['projects']:
        parts.append(build_projects(data['projects']))

    # Education
    if data['education']:
        parts.append(build_education(data['education']))

    # Interests
    if data['interests']:
        parts.append(build_interests(data['interests']))

    parts.append('</div>')
    parts.append('</body>')
    parts.append('</html>')

    return '\n'.join(parts)


def build_header(data):
    """Build the header section."""
    h = []
    h.append('  <div class="header">')
    h.append('    <div class="header-top">')
    h.append(f'      <img class="avatar" src="data:image/jpeg;base64,..." alt="{escape(data["name"])}">')
    h.append('      <div class="header-info">')
    h.append(f'        <h1>{escape(data["name"])}</h1>')

    if data.get('summary'):
        h.append(f'        <div class="subtitle">{escape(data["summary"])}</div>')

    # Contacts
    contacts = []
    if data.get('phone'):
        contacts.append(f'<a href="tel:{data["phone"]}">📱 {data["phone"]}</a>')
    if data.get('email'):
        contacts.append(f'<a href="mailto:{data["email"]}">✉️ {data["email"]}</a>')
    if data.get('github'):
        contacts.append(f'<a href="https://github.com/{data["github"]}">🔗 github.com/{data["github"]}</a>')

    if contacts:
        h.append('        <div class="contacts">')
        h.append('          ' + ' '.join(contacts))
        h.append('        </div>')

    h.append('      </div>')
    h.append('    </div>')

    # Tags
    tags = data.get('tags', [])
    if tags:
        h.append('    <div class="tag-row">')
        for tag in tags:
            h.append(f'      <span class="tag">{escape(tag)}</span>')
        h.append('    </div>')

    h.append('  </div>')
    return '\n'.join(h)


def build_skills(skills):
    """Build the skills section."""
    s = []
    s.append('  <div class="section">')
    s.append('    <div class="section-title">专业技能</div>')
    s.append('    <div class="skills-grid">')
    for skill in skills:
        s.append('      <div class="skill-card">')
        s.append(f'        <div class="label">{escape(skill["label"])}</div>')
        s.append(f'        <div class="value">{escape(skill["value"])}</div>')
        s.append('      </div>')
    s.append('    </div>')
    s.append('  </div>')
    return '\n'.join(s)


def build_work(work_entries, keywords=None):
    """Build the work experience section."""
    w = []
    w.append('  <div class="section">')
    w.append('    <div class="section-title">工作经历</div>')

    # Determine featured (most recent) entries
    for idx, entry in enumerate(work_entries):
        is_featured = (idx < 2)
        w.append(f'    <div class="job-card{" featured" if is_featured else ""}">')
        w.append('      <div class="job-header">')
        w.append('        <div>')

        company_line = escape(entry.get('company', ''))
        if entry.get('dept'):
            company_line += f' <span class="job-company-separator">—</span> <span class="job-institution">{escape(entry["dept"])}</span>'
        w.append(f'          <div class="job-company">{company_line}</div>')
        w.append(f'          <div class="job-role">{escape(entry.get("role", ""))}</div>')

        w.append('        </div>')
        w.append(f'        <div class="job-period">{escape(entry.get("time", ""))}</div>')
        w.append('      </div>')

        # HR element for corporate style
        w.append('      <hr class="section-rule">')

        # Description
        w.append('      <div class="job-group">')

        # Add keywords from weekly reports as extra context
        if keywords:
            all_kws = keywords.get('all', [])
            if all_kws:
                kw_text = ', '.join(all_kws[:15])
                w.append(f'      <div class="job-desc">技术栈关键词：<span class="highlight">{escape(kw_text)}</span></div>')

        # Bullets
        bullets = entry.get('bullets', [])
        if bullets:
            w.append('        <ul>')
            for bullet in bullets:
                cleaned = re.sub(r'^[\+\*\-]\s*', '', bullet).strip()
                if cleaned:
                    w.append(f'          <li>{escape(cleaned)}</li>')
            w.append('        </ul>')

        w.append('      </div>')
        w.append('    </div>')

    w.append('  </div>')
    return '\n'.join(w)


def build_projects(projects):
    """Build the projects section."""
    p = []
    p.append('  <div class="section">')
    p.append('    <div class="section-title">核心项目</div>')

    for proj in projects:
        p.append('    <div class="job-card">')
        p.append('      <div class="job-header">')
        p.append('        <div>')
        name = escape(proj.get('name', ''))
        if proj.get('link'):
            name += f' <a href="{escape(proj["link"])}" class="link" target="_blank">[链接]</a>'
        p.append(f'          <div class="job-company">{name}</div>')
        p.append(f'          <div class="job-role">{escape(proj.get("time", ""))}</div>')
        p.append('        </div>')
        p.append('      </div>')
        p.append('      <hr class="section-rule">')

        bullets = proj.get('bullets', [])
        if bullets:
            p.append('      <div class="job-group">')
            p.append('        <ul>')
            for bullet in bullets:
                cleaned = re.sub(r'^\d+\.\s*', '', bullet).strip()
                if cleaned:
                    p.append(f'          <li>{escape(cleaned)}</li>')
            p.append('        </ul>')
            p.append('      </div>')

        p.append('    </div>')

    p.append('  </div>')
    return '\n'.join(p)


def build_education(edu_entries):
    """Build the education section."""
    e = []
    e.append('  <div class="section">')
    e.append('    <div class="section-title">教育背景</div>')
    e.append('    <table class="edu-table">')
    e.append('      <thead><tr><th>时间</th><th>学校</th><th>学院</th><th>学位</th></tr></thead>')
    e.append('      <tbody>')
    for edu in edu_entries:
        e.append(f'      <tr>')
        e.append(f'        <td>{escape(edu.get("time", ""))}</td>')
        e.append(f'        <td>{escape(edu.get("school", ""))}</td>')
        e.append(f'        <td>{escape(edu.get("dept", ""))}</td>')
        e.append(f'        <td>{escape(edu.get("degree", ""))}</td>')
        e.append('      </tr>')
    e.append('      </tbody>')
    e.append('    </table>')
    e.append('  </div>')
    return '\n'.join(e)


def build_interests(interests):
    """Build the interests section."""
    i = []
    i.append('  <div class="section">')
    i.append('    <div class="section-title">个人项目</div>')
    i.append('    <div class="skills-grid">')
    for interest in interests:
        i.append('      <div class="skill-card">')
        name = escape(interest.get('name', ''))
        if interest.get('link'):
            name += f' <a href="{escape(interest["link"])}" class="link" target="_blank">[GitHub]</a>'
        i.append(f'        <div class="value">{name}</div>')
        i.append('      </div>')
    i.append('    </div>')
    i.append('  </div>')
    return '\n'.join(i)


def generate_markdown(data, output_path):
    """Generate a clean Markdown version of the resume."""
    lines = []
    lines.append(f'# {data["name"]}')
    lines.append('')

    # Contact info
    contact_parts = []
    if data.get('phone'):
        contact_parts.append(f'📱 {data["phone"]}')
    if data.get('email'):
        contact_parts.append(f'✉️ {data["email"]}')
    if data.get('github'):
        contact_parts.append(f'🔗 github.com/{data["github"]}')
    if contact_parts:
        lines.append(' | '.join(contact_parts))
        lines.append('')

    if data.get('tags'):
        lines.append(' | '.join(data['tags']))
        lines.append('')

    # Skills
    if data['skills']:
        lines.append('## 专业技能')
        lines.append('')
        for skill in data['skills']:
            lines.append(f'- **{skill["label"]}**: {skill["value"]}')
        lines.append('')

    # Work
    if data['work']:
        lines.append('## 工作经历')
        lines.append('')
        for entry in data['work']:
            header = f'### {entry.get("company", "")} | {entry.get("role", "")}'
            if entry.get('time'):
                header += f'  ({entry["time"]})'
            lines.append(header)
            lines.append('')
            for bullet in entry.get('bullets', []):
                cleaned = re.sub(r'^[\+\*\-]\s*', '', bullet).strip()
                if cleaned:
                    lines.append(f'- {cleaned}')
            lines.append('')

    # Projects
    if data['projects']:
        lines.append('## 核心项目')
        lines.append('')
        for proj in data['projects']:
            lines.append(f'### {proj.get("name", "")} ({proj.get("time", "")})')
            if proj.get('link'):
                lines.append(f'- 链接: {proj["link"]}')
            lines.append('')
            for bullet in proj.get('bullets', []):
                cleaned = re.sub(r'^\d+\.\s*', '', bullet).strip()
                if cleaned:
                    lines.append(f'- {cleaned}')
            lines.append('')

    # Education
    if data['education']:
        lines.append('## 教育背景')
        lines.append('')
        lines.append('| 时间 | 学校 | 学院 | 学位 |')
        lines.append('|------|------|------|------|')
        for edu in data['education']:
            lines.append(f'| {edu.get("time", "")} | {edu.get("school", "")} | {edu.get("dept", "")} | {edu.get("degree", "")} |')
        lines.append('')

    # Interests
    if data['interests']:
        lines.append('## 个人项目')
        lines.append('')
        for interest in data['interests']:
            name = interest.get('name', '')
            if interest.get('link'):
                name += f' ({interest["link"]})'
            lines.append(f'- {name}')
        lines.append('')

    content = '\n'.join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Render HTML resume from Markdown source + weekly reports')
    parser.add_argument('--resume', '-r', required=True, help='Path to resume Markdown file')
    parser.add_argument('--style', '-s', default='apple', help='Style theme (apple, minimal, corporate, heisenberg, pulse)')
    parser.add_argument('--output', '-o', default=None, help='Output HTML file path')
    parser.add_argument('--output-dir', '-d', default=None, help='Output directory (generates HTML + Markdown)')
    parser.add_argument('--texts', '-t', default=None, help='Path to extracted_texts.json (weekly reports)')
    parser.add_argument('--json', action='store_true', help='Output parsed JSON instead of HTML')
    args = parser.parse_args()

    # Step 1: Parse resume
    print("Parsing resume...")
    data = parse_resume_md(args.resume)
    print(f"  Name: {data['name']}")
    print(f"  Skills: {len(data['skills'])}")
    print(f"  Work: {len(data['work'])}")
    print(f"  Education: {len(data['education'])}")
    print(f"  Projects: {len(data['projects'])}")

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    # Step 2: Extract keywords from weekly reports
    keywords = None
    if args.texts:
        print("Extracting keywords from weekly reports...")
        keywords = extract_keywords_from_texts(args.texts)
        all_kws = keywords.get('all', [])
        if all_kws:
            print(f"  Keywords: {', '.join(all_kws[:10])}{'...' if len(all_kws) > 10 else ''}")

    # Step 3: Render HTML
    print("Rendering HTML...")
    html = render_html(data, args.style, keywords)

    # Determine output path
    if args.output:
        html_path = args.output
    elif args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        name = data['name'].replace(' ', '-')
        html_path = os.path.join(args.output_dir, f'resume-{name}-final.html')
    else:
        name = data['name'].replace(' ', '-')
        html_path = f'resume-{name}-final.html'

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  HTML -> {html_path}")

    # Step 4: Generate Markdown
    if args.output_dir:
        md_path = os.path.splitext(html_path)[0] + '.md'
        generate_markdown(data, md_path)
        print(f"  Markdown -> {md_path}")

    # Write parsed data for debugging
    if args.output_dir:
        json_path = os.path.join(args.output_dir, 'resume_data.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON   -> {json_path}")


if __name__ == '__main__':
    main()
