#!/usr/bin/env python3
"""Extract readable text from any file — .eml, .msg, .html, .txt, .md, .pdf."""

import argparse
import email
import json
import os
import re
import sys


def extract_eml(path):
    """Decode .eml (MIME email) to plain text."""
    with open(path, 'rb') as f:
        raw = f.read()
    msg = email.message_from_bytes(raw)

    lines = []

    # Headers — read raw bytes directly to preserve UTF-8
    header_names = ('From', 'To', 'Subject', 'Date', 'Cc', 'Bcc')
    raw_text = raw.decode('utf-8', errors='replace')
    in_headers = True
    for line in raw_text.split('\n'):
        if not in_headers:
            break
        if line.strip() == '':
            in_headers = False
            continue
        colon = line.find(':')
        if colon > 0:
            name = line[:colon].strip()
            value = line[colon+1:].strip()
            if name in header_names:
                lines.append(f'{name}: {value}')
        elif line[0] in (' ', '\t') and lines:
            # Continuation line
            lines[-1] += ' ' + line.strip()

    if lines:
        lines.append('')

    # Body — walk parts and collect text
    body = _extract_body(msg)
    lines.append(body)
    return '\n'.join(lines)


def _extract_body(msg):
    """Walk MIME parts and return combined text body."""
    parts_text = []
    for part in msg.walk():
        ct = part.get_content_type()
        if ct == 'text/plain':
            payload = _decode_payload(part)
            if payload:
                parts_text.append(payload)
        elif ct == 'text/html':
            payload = _decode_payload(part)
            if payload:
                parts_text.append(_html_to_text(payload))
    if parts_text:
        return '\n'.join(parts_text)

    # Fallback: raw payload
    raw = msg.get_payload(decode=True)
    if isinstance(raw, bytes):
        charset = msg.get_content_charset() or 'utf-8'
        return raw.decode(charset, errors='replace')
    return str(raw or '')


def _decode_payload(part):
    """Decode a MIME part's payload to text."""
    payload = part.get_payload(decode=True)
    if isinstance(payload, bytes):
        charset = part.get_content_charset() or 'utf-8'
        return payload.decode(charset, errors='replace')
    return str(payload or '')


def _html_to_text(html):
    """Strip HTML tags to get readable text."""
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S | re.I)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S | re.I)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.I)
    text = re.sub(r'<p[^>]*>', '\n', text, flags=re.I)
    text = re.sub(r'</p>', '\n', text, flags=re.I)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&(amp|lt|gt|quot);', lambda m: {'&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"'}.get(m.group(0), m.group(0)), text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def extract_msg(path):
    """Decode .msg (Outlook) to plain text. Needs extract-msg."""
    try:
        from msgreader import MsgReader  # noqa: F401
    except ImportError:
        return f'[请安装依赖: pip install extract-msg]\n文件: {os.path.basename(path)}'

    import msgreader
    msg = msgreader.MsgReader(path)
    lines = []
    if msg.subject:
        lines.append(f'Subject: {msg.subject}')
    if msg.date:
        lines.append(f'Date: {msg.date}')
    if msg.sender_name:
        lines.append(f'From: {msg.sender_name}')
    if lines:
        lines.append('')
    if msg.body:
        lines.append(msg.body)
    return '\n'.join(lines)


def extract_html(path):
    """Read .html/.htm and strip to plain text."""
    with open(path, 'r', encoding='utf-8-sig', errors='replace') as f:
        html = f.read()
    return _html_to_text(html)


def extract_text(path):
    """Read any text-based file."""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read().strip()


# Dispatch by extension
HANDLERS = {
    '.eml': extract_eml,
    '.msg': extract_msg,
    '.html': extract_html,
    '.htm': extract_html,
}

TEXT_EXTS = {'.txt', '.text', '.md', '.sg', '.log', '.csv', '.json', '.yaml', '.yml'}


def extract_file(path):
    """Auto-detect format, return plain text."""
    ext = os.path.splitext(path)[1].lower()
    handler = HANDLERS.get(ext)
    if handler:
        return handler(path)
    if ext in TEXT_EXTS or not ext:
        return extract_text(path)
    # Fallback: try as UTF-8 text
    return extract_text(path)


def main():
    parser = argparse.ArgumentParser(
        description='Extract plain text from any file (.eml, .msg, .html, .txt, .md, ...)'
    )
    parser.add_argument('source', help='File or directory')
    parser.add_argument('--json', action='store_true', help='Output as JSON array')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recurse into subdirectories')
    args = parser.parse_args()

    if os.path.isfile(args.source):
        content = extract_file(args.source)
        if args.json:
            print(json.dumps({'filename': os.path.basename(args.source), 'content': content}, ensure_ascii=False, indent=2))
        else:
            print(f"--- {os.path.basename(args.source)} ---")
            print(content)
    else:
        entries = []
        paths = []
        if args.recursive:
            for root, _, files in os.walk(args.source):
                for fname in sorted(files):
                    paths.append(os.path.join(root, fname))
        else:
            for fname in sorted(os.listdir(args.source)):
                p = os.path.join(args.source, fname)
                if os.path.isfile(p):
                    paths.append(p)

        for p in paths:
            content = extract_file(p)
            entry = {'filename': os.path.basename(p), 'content': content}
            entries.append(entry)
            if not args.json:
                print(f"--- {entry['filename']} ---")
                print(content)
                print()

        if args.json:
            print(json.dumps(entries, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
