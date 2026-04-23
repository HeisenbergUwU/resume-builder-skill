#!/usr/bin/env python3
"""Extract and categorize files from a zip archive or directory."""

import argparse
import os
import zipfile


AVATAR_EXTS = ('.jpg', '.jpeg', '.png')
REPORT_EXTS = ('.eml', '.msg', '.txt', '.html', '.htm', '.text')
DOC_EXTS = ('.md', '.sg', '.pdf')


def extract_zip(zip_path, extract_dir):
    """Unzip and return categorized file lists."""
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_dir)
    return categorize(extract_dir)


def categorize(source_dir):
    """Walk a directory and return files grouped by category."""
    categories = {'avatars': [], 'reports': [], 'docs': []}
    for root, _, files in os.walk(source_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            full = os.path.join(root, f)
            if ext in AVATAR_EXTS:
                categories['avatars'].append(full)
            elif ext in REPORT_EXTS:
                categories['reports'].append(full)
            elif ext in DOC_EXTS:
                categories['docs'].append(full)
    return categories


def pick_best_avatar(avatars):
    """Pick the best avatar: prefer named avatar/photo/head, else largest."""
    if not avatars:
        return None
    named = [a for a in avatars if any(k in os.path.basename(a).lower()
                                        for k in ('avatar', 'photo', 'head'))]
    candidates = named or avatars
    return max(candidates, key=lambda p: os.path.getsize(p))


def main():
    parser = argparse.ArgumentParser(description='Extract and categorize resume source data')
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument('--zip', help='Path to source zip archive')
    src.add_argument('--dir', help='Path to source directory')
    parser.add_argument('--output', default='.', help='Extract directory (for --zip)')
    args = parser.parse_args()

    if args.zip:
        cats = extract_zip(args.zip, args.output)
    else:
        cats = categorize(args.dir)

    best = pick_best_avatar(cats['avatars'])
    print(f"Avatars ({len(cats['avatars'])}): {', '.join(os.path.basename(a) for a in cats['avatars'])}")
    if best:
        print(f"  → Selected: {os.path.basename(best)}")
    print(f"Reports ({len(cats['reports'])}): {', '.join(os.path.basename(r) for r in cats['reports'])}")
    print(f"Docs    ({len(cats['docs'])}): {', '.join(os.path.basename(d) for d in cats['docs'])}")

    # Output JSON for programmatic use
    import json
    result = {
        'avatars': cats['avatars'],
        'reports': cats['reports'],
        'docs': cats['docs'],
        'selected_avatar': best,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
