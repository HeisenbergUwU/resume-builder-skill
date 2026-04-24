#!/usr/bin/env python3
"""Extract and categorize files from a zip archive or directory."""

import argparse
import json
import os
import sys
import zipfile


AVATAR_EXTS = ('.jpg', '.jpeg', '.png')
REPORT_EXTS = ('.eml', '.msg', '.txt', '.html', '.htm', '.text')
DOC_EXTS = ('.md', '.sg', '.pdf')


def extract_zip(zip_path, extract_dir):
    """Unzip and return categorized file lists."""
    if not os.path.isfile(zip_path):
        print(f"ERROR: Zip file not found: {zip_path}", file=sys.stderr)
        sys.exit(1)
    try:
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(extract_dir)
    except zipfile.BadZipFile:
        print(f"ERROR: Not a valid zip file: {zip_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to extract zip: {e}", file=sys.stderr)
        sys.exit(1)
    return categorize(extract_dir)


def categorize(source_dir):
    """Walk a directory and return files grouped by category."""
    if not os.path.isdir(source_dir):
        print(f"ERROR: Directory not found: {source_dir}", file=sys.stderr)
        sys.exit(1)
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
    try:
        return max(candidates, key=lambda p: os.path.getsize(p))
    except OSError as e:
        print(f"WARNING: Could not get file size for avatar selection: {e}", file=sys.stderr)
        return candidates[0] if candidates else None


def main():
    parser = argparse.ArgumentParser(description='Extract and categorize resume source data')
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument('--zip', help='Path to source zip archive')
    src.add_argument('--dir', help='Path to source directory')
    parser.add_argument('--output', default='.', help='Extract directory (for --zip)')
    parser.add_argument('--json-only', action='store_true', help='Output only JSON (no human-readable summary)')
    parser.add_argument('--manifest', default=None, help='Write manifest JSON to this file (default: ./extracted_manifest.json)')
    args = parser.parse_args()

    if args.zip:
        cats = extract_zip(args.zip, args.output)
    else:
        cats = categorize(args.dir)

    best = pick_best_avatar(cats['avatars'])

    result = {
        'avatars': cats['avatars'],
        'reports': cats['reports'],
        'docs': cats['docs'],
        'selected_avatar': best,
    }

    manifest_path = args.manifest or os.path.join(args.output if args.zip else args.dir, 'extracted_manifest.json')
    try:
        os.makedirs(os.path.dirname(os.path.abspath(manifest_path)), exist_ok=True)
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"WARNING: Could not write manifest: {e}", file=sys.stderr)

    if not args.json_only:
        print(f"Avatars ({len(cats['avatars'])}): {', '.join(os.path.basename(a) for a in cats['avatars'])}")
        if best:
            print(f"  -> Selected: {os.path.basename(best)}")
        print(f"Reports ({len(cats['reports'])}): {', '.join(os.path.basename(r) for r in cats['reports'])}")
        print(f"Docs    ({len(cats['docs'])}): {', '.join(os.path.basename(d) for d in cats['docs'])}")
        print(f"Manifest -> {manifest_path}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
