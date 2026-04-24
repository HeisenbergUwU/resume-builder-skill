#!/usr/bin/env python3
"""Center-crop and embed an avatar image as Base64 in an HTML resume.

Auto-discovers avatar from local files first, downloads a placeholder as fallback.
"""

import argparse
import base64
import io
import os
import re
import sys

AVATAR_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
AVATAR_NAMES = ('avatar', 'photo', 'head', 'profile', 'portrait', 'face')


def find_local_avatar(search_dirs):
    """Search for avatar files in given directories."""
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            ext = os.path.splitext(f)[1].lower()
            if ext in AVATAR_EXTS:
                base = os.path.splitext(f)[0].lower()
                if any(k in base for k in AVATAR_NAMES):
                    return os.path.join(d, f)
        for f in os.listdir(d):
            ext = os.path.splitext(f)[1].lower()
            if ext in AVATAR_EXTS:
                return os.path.join(d, f)
    return None


def download_placeholder_avatar(dest):
    """Generate a simple SVG placeholder avatar (no network needed)."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <rect width="200" height="200" fill="#e5e7eb"/>
  <circle cx="100" cy="75" r="35" fill="#9ca3af"/>
  <ellipse cx="100" cy="170" rx="55" ry="45" fill="#9ca3af"/>
</svg>'''
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(svg)
    return dest


def crop_and_embed(img_path, html_content, size=100):
    """Center-crop to square, resize, and replace avatar in HTML."""
    is_svg = os.path.splitext(img_path)[1].lower() == '.svg'

    has_pillow = False
    try:
        from PIL import Image
        has_pillow = True
    except ImportError:
        pass

    try:
        if has_pillow and not is_svg:
            img = Image.open(img_path)
            img.load()  # Force load to detect corrupted images
            w, h = img.size
            side = min(w, h)
            left = (w - side) // 2
            top = (h - side) // 2
            square = img.crop((left, top, left + side, top + side))
            avatar = square.resize((size, size), Image.LANCZOS)
            buf = io.BytesIO()
            avatar.save(buf, format='JPEG', quality=90)
            data_uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        else:
            with open(img_path, 'rb') as f:
                raw = f.read()
            ext = os.path.splitext(img_path)[1].lower()
            mime = 'image/jpeg' if ext in ('.jpg', '.jpeg') else ('image/png' if ext == '.png' else 'image/svg+xml')
            data_uri = f"data:{mime};base64," + base64.b64encode(raw).decode()
    except Exception as e:
        print(f"ERROR: Failed to process avatar image: {e}", file=sys.stderr)
        sys.exit(1)

    img_tag = '<img class="avatar" src="' + data_uri + '" alt="avatar">'

    # Strategy 1: Replace existing data URI in <img src="data:image/...">
    old_uris = re.findall(r'src="data:image/[^"]+"', html_content)
    if old_uris:
        old = old_uris[0]
        new = 'src="' + data_uri + '"'
        html_content = html_content.replace(old, new)
        return html_content

    # Strategy 2: Replace <div class="avatar">...</div> with <img class="avatar" ...>
    div_match = re.search(r'<div\s+class="avatar"[^>]*>.*?</div>', html_content, re.S)
    if div_match:
        html_content = html_content.replace(div_match.group(0), img_tag)
        return html_content

    # Strategy 3: Replace explicit placeholder
    placeholder = 'src="data:image/jpeg;base64,..."'
    if placeholder in html_content:
        replacement = 'src="' + data_uri + '"'
        html_content = html_content.replace(placeholder, replacement)
        return html_content

    # Fallback: prepend img before first .container or <body>
    if '<div class="container">' in html_content:
        html_content = html_content.replace('<div class="container">', f'<div class="container">\n  {img_tag}')
    elif '<body>' in html_content:
        html_content = html_content.replace('<body>', f'<body>\n  {img_tag}')
    else:
        print("WARNING: Could not find a good insertion point for avatar", file=sys.stderr)

    return html_content


def main():
    parser = argparse.ArgumentParser(description='Center-crop avatar and embed in HTML resume')
    parser.add_argument('avatar', nargs='?', default=None, help='Path to avatar image (auto-discover if omitted)')
    parser.add_argument('html', help='Path to HTML resume file')
    parser.add_argument('--output', '-o', help='Output HTML file (default: overwrite input)')
    parser.add_argument('--size', type=int, default=100, help='Avatar output size in px (default: 100)')
    parser.add_argument('--search-dirs', nargs='*', default=[], help='Directories to search for avatar')
    args = parser.parse_args()

    if not os.path.isfile(args.html):
        print(f"ERROR: HTML file not found: {args.html}", file=sys.stderr)
        sys.exit(1)

    # Determine avatar path
    avatar_path = args.avatar
    if not avatar_path:
        html_dir = os.path.dirname(os.path.abspath(args.html))
        search_dirs = args.search_dirs + [html_dir, '.']
        avatar_path = find_local_avatar(search_dirs)

    if not avatar_path or not os.path.isfile(avatar_path):
        tmp = os.path.join(os.path.dirname(os.path.abspath(args.html)), '_placeholder_avatar.svg')
        avatar_path = download_placeholder_avatar(tmp)
        print(f"NOTE: No avatar found, using placeholder ({avatar_path})")
    else:
        print(f"Using avatar: {avatar_path}")

    try:
        with open(args.html, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except UnicodeDecodeError:
        with open(args.html, 'r', encoding='utf-8', errors='replace') as f:
            html_content = f.read()
        print("WARNING: HTML file had encoding issues, using error replacement", file=sys.stderr)

    result = crop_and_embed(avatar_path, html_content, args.size)

    out = args.output or args.html
    with open(out, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Avatar embedded -> {out}")


if __name__ == '__main__':
    main()
