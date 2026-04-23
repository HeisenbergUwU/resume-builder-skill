#!/usr/bin/env python3
"""Center-crop and embed an avatar image as Base64 in an HTML resume."""

import argparse
import base64
import io
import os
import re
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: pip install Pillow")


def crop_and_embed(img_path, html_content, size=100):
    """Center-crop to square, resize, and replace Base64 data URI in HTML."""
    img = Image.open(img_path)
    w, h = img.size

    # Center crop to square — keeps the subject centered in the circular frame
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    square = img.crop((left, top, left + side, top + side))

    # Resize
    avatar = square.resize((size, size), Image.LANCZOS)

    # Encode as Base64
    buf = io.BytesIO()
    avatar.save(buf, format='JPEG', quality=90)
    data_uri = f"data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}"

    # Replace existing data URI placeholder in HTML
    old_uris = re.findall(r'src="(data:image/jpeg[^"]+)"', html_content)
    if old_uris:
        html_content = html_content.replace(old_uris[0], data_uri)
    else:
        placeholder = '<img class="avatar" src="data:image/jpeg;base64,..." '
        if placeholder in html_content:
            replacement = f'<img class="avatar" src="{data_uri} '
            html_content = html_content.replace(placeholder, replacement)

    return html_content


def main():
    parser = argparse.ArgumentParser(description='Center-crop avatar and embed in HTML resume')
    parser.add_argument('avatar', help='Path to avatar image')
    parser.add_argument('html', help='Path to HTML resume file')
    parser.add_argument('--output', '-o', help='Output HTML file (default: overwrite input)')
    parser.add_argument('--size', type=int, default=100, help='Avatar output size in px (default: 100)')
    args = parser.parse_args()

    if not os.path.isfile(args.avatar):
        sys.exit(f"Avatar file not found: {args.avatar}")
    if not os.path.isfile(args.html):
        sys.exit(f"HTML file not found: {args.html}")

    with open(args.html, 'r', encoding='utf-8') as f:
        html_content = f.read()

    result = crop_and_embed(args.avatar, html_content, args.size)

    out = args.output or args.html
    with open(out, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Avatar embedded → {out}")


if __name__ == '__main__':
    main()
