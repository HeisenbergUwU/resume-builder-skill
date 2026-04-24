#!/usr/bin/env python3
"""Resume Builder Pipeline — orchestrates all scripts in sequence.

Automatic steps:
  1. extract_sources  ->  manifest.json
  2. extract_text     ->  extracted_texts.json
  [MODEL: draft resume content, choose style, render HTML]
  6. embed_avatar     ->  final HTML with avatar
  [MODEL: generate Markdown version]
  8. html_to_pdf      ->  final PDF

Usage:
  python scripts/pipeline.py --zip sources.zip --output-dir ./output
  python scripts/pipeline.py --dir /path/to/sources --output-dir ./output
  python scripts/pipeline.py --zip sources.zip --output-dir ./output --skip embed-avatar,html-to-pdf
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time


SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    {'id': 'extract-sources', 'label': 'Extract & categorize sources', 'auto': True},
    {'id': 'extract-text', 'label': 'Extract text from files', 'auto': True},
    {'id': 'draft-resume', 'label': 'Render HTML from resume markdown', 'auto': True},
    {'id': 'embed-avatar', 'label': 'Crop & embed avatar', 'auto': True},
    {'id': 'generate-markdown', 'label': 'Generate Markdown version', 'auto': True},
    {'id': 'html-to-pdf', 'label': 'Convert HTML to PDF', 'auto': True},
]


def run(script, args, cwd=None, check=True):
    """Run a sibling script and return (success, stdout, stderr)."""
    script_path = os.path.join(SCRIPTS_DIR, script)
    cmd = [sys.executable, script_path] + args
    cwd = cwd or SCRIPTS_DIR
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=120)
        success = result.returncode == 0
        if success or not check:
            return success, result.stdout, result.stderr
        else:
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            return False, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print(f"ERROR: {script} timed out", file=sys.stderr)
        return False, "", "Timeout"
    except Exception as e:
        print(f"ERROR: Failed to run {script}: {e}", file=sys.stderr)
        return False, "", str(e)


def step_extract_sources(output_dir, source_zip=None, source_dir=None):
    """Step 1: Extract and categorize sources."""
    args = ['--output', output_dir, '--manifest', os.path.join(output_dir, 'extracted_manifest.json')]
    if source_zip:
        args = ['--zip', source_zip] + args
    elif source_dir:
        args = ['--dir', source_dir] + args

    success, stdout, stderr = run('extract_sources.py', args)
    if stdout:
        print(stdout)
    if success:
        manifest_path = os.path.join(output_dir, 'extracted_manifest.json')
        if os.path.isfile(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    return None


def step_extract_text(output_dir, source_dir):
    """Step 2: Extract text from all reports and docs."""
    if not os.path.isdir(source_dir):
        print(f"ERROR: Source directory not found: {source_dir}", file=sys.stderr)
        return []

    output_file = os.path.join(output_dir, 'extracted_texts.json')
    args = [source_dir, '-r', '--json', '--output', output_file]

    success, stdout, stderr = run('extract_text.py', args)
    if success and os.path.isfile(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def step_embed_avatar(output_dir, html_path, avatar_path=None):
    """Step 4: Embed avatar into HTML."""
    if not os.path.isfile(html_path):
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        return False

    args = [html_path]
    if avatar_path and os.path.isfile(avatar_path):
        args = [avatar_path, html_path]
    else:
        args = [None, html_path]
        # Clean up None from args
        args = [a for a in args if a is not None]
        args = [html_path]

    out_path = html_path  # overwrite in place
    args.extend(['--output', out_path])

    # Add search dirs for auto-discovery
    args.extend(['--search-dirs', output_dir])

    success, stdout, stderr = run('embed_avatar.py', args)
    if stdout:
        print(stdout)
    return success


def step_html_to_pdf(output_dir, html_path):
    """Step 6: Convert HTML to PDF."""
    if not os.path.isfile(html_path):
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        return False

    pdf_path = os.path.splitext(html_path)[0] + '.pdf'
    args = [html_path, '--output', pdf_path]

    success, stdout, stderr = run('html_to_pdf.py', args)
    if stdout:
        print(stdout)
    return success


def find_html_in_dir(directory):
    """Find the final HTML file in output directory."""
    for f in os.listdir(directory):
        if f.endswith('.html') and not f.startswith('_'):
            return os.path.join(directory, f)
    return None


def print_todo(step_id, context=None):
    """Print a TODO block for manual steps."""
    todos = {
        'draft-resume': [
            "Read extracted_texts.json for source content",
            "Select career guide from references/<career>/",
            "Choose a style from assets/styles/<name>/",
            "Draft resume content following the guide",
            "Render HTML using the chosen style template",
            "Save as <output-dir>/resume-<name>-final.html",
        ],
        'generate-markdown': [
            "Read the finalized HTML file",
            "Convert HTML sections to Markdown",
            "Save as <output-dir>/resume-<name>-final.md",
        ],
    }
    items = todos.get(step_id, [])
    print(f"\n{'='*60}")
    print(f"  TODO: Manual step needed")
    print(f"{'='*60}")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    if context:
        for k, v in context.items():
            print(f"\n  {k}: {v}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Resume Builder Pipeline — orchestrates all scripts in sequence',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument('--zip', help='Path to source zip archive')
    src.add_argument('--dir', help='Path to source directory')
    parser.add_argument('--output-dir', '-o', default='./resume-output', help='Output directory (default: ./resume-output)')
    parser.add_argument('--skip', default='', help='Comma-separated step IDs to skip')
    parser.add_argument('--resume', default=None, help='Path to resume Markdown file (default: auto-search in source dir)')
    parser.add_argument('--style', default='apple', help='Style theme: apple, minimal, corporate, heisenberg, pulse (default: apple)')
    parser.add_argument('--html', default=None, help='Path to pre-built HTML (skips draft step)')
    args = parser.parse_args()

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    skip_steps = set(s.strip() for s in args.skip.split(',') if s.strip())
    if skip_steps:
        print(f"Skipping steps: {', '.join(skip_steps)}")

    print(f"\nResume Builder Pipeline")
    print(f"{'='*60}")
    print(f"  Source: {args.zip or args.dir}")
    print(f"  Output: {output_dir}")
    print(f"{'='*60}\n")

    t0 = time.time()

    # --- Step 1: Extract sources ---
    if 'extract-sources' not in skip_steps:
        print("[1/6] Extract & categorize sources...")
        manifest = step_extract_sources(output_dir, source_zip=args.zip, source_dir=args.dir)
        if manifest is None:
            print("ERROR: Source extraction failed", file=sys.stderr)
            sys.exit(1)
        avatar_path = manifest.get('selected_avatar')
        print(f"  Files: {len(manifest.get('reports', []))} reports, {len(manifest.get('docs', []))} docs, {len(manifest.get('avatars', []))} avatars\n")
    else:
        manifest_path = os.path.join(output_dir, 'extracted_manifest.json')
        if os.path.isfile(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        else:
            manifest = {'avatars': [], 'reports': [], 'docs': [], 'selected_avatar': None}
        avatar_path = manifest.get('selected_avatar')
        print("[1/6] Skipped (extract-sources)\n")

    # --- Step 2: Extract text ---
    if 'extract-text' not in skip_steps:
        print("[2/6] Extract text from files...")
        texts = step_extract_text(output_dir, args.dir or os.path.join(output_dir, '.'))
        print(f"  Extracted {len(texts)} files\n")
    else:
        texts_path = os.path.join(output_dir, 'extracted_texts.json')
        texts = json.load(open(texts_path, 'r', encoding='utf-8')) if os.path.isfile(texts_path) else []
        print("[2/6] Skipped (extract-text)\n")

    # --- Step 3: Render HTML from resume markdown ---
    if 'draft-resume' not in skip_steps:
        print("[3/6] Render HTML from resume markdown...")
        html_file = args.html
        if html_file and os.path.isfile(html_file):
            dest = os.path.join(output_dir, os.path.basename(html_file))
            shutil.copy2(html_file, dest)
            print(f"  Using provided HTML: {dest}\n")
        else:
            resume_md = args.resume
            if not resume_md:
                source_dir = args.dir or (os.path.dirname(args.zip) if args.zip else '.')
                for candidate in ['个人简历.md', 'resume.md', 'Resume.md', 'README.md']:
                    candidate_path = os.path.join(source_dir, candidate)
                    if os.path.isfile(candidate_path):
                        resume_md = candidate_path
                        break

            texts_json = os.path.join(output_dir, 'extracted_texts.json')
            if resume_md:
                args_render = ['--resume', resume_md, '--style', args.style, '--output-dir', output_dir]
                if os.path.isfile(texts_json):
                    args_render.extend(['--texts', texts_json])
                success, stdout, stderr = run('render_resume.py', args_render)
                if stdout:
                    print(stdout)
                if success:
                    html_file = find_html_in_dir(output_dir)
                    if html_file:
                        print(f"  Auto-rendered: {os.path.basename(html_file)}\n")
            if not html_file:
                print_todo('draft-resume', {
                    'Manifest': os.path.join(output_dir, 'extracted_manifest.json'),
                    'Extracted text': os.path.join(output_dir, 'extracted_texts.json'),
                    'Output dir': output_dir,
                })
    else:
        print("[3/6] Skipped (draft-resume)\n")

    # Find HTML for subsequent steps
    if html_file:
        final_html = html_file
    else:
        final_html = find_html_in_dir(output_dir)

    # --- Step 4: Embed avatar ---
    if 'embed-avatar' not in skip_steps:
        print("[4/6] Crop & embed avatar...")
        if final_html:
            step_embed_avatar(output_dir, final_html, avatar_path)
            print()
        else:
            print("  SKIPPED: No HTML file found. Complete step 3 first.\n")
    else:
        print("[4/6] Skipped (embed-avatar)\n")

    # --- Step 5: Generate Markdown (auto if render_resume.py created it) ---
    if 'generate-markdown' not in skip_steps:
        print("[5/6] Generate Markdown version")
        if final_html:
            md_path = os.path.splitext(final_html)[0] + '.md'
            if os.path.isfile(md_path):
                print(f"  Auto-generated: {os.path.basename(md_path)}\n")
            else:
                print_todo('generate-markdown', {
                    'HTML file': final_html,
                    'Output dir': output_dir,
                })
        else:
            print("  SKIPPED: No HTML file found.\n")
    else:
        print("[5/6] Skipped (generate-markdown)\n")

    # --- Step 6: HTML to PDF ---
    if 'html-to-pdf' not in skip_steps:
        print("[6/6] Convert HTML to PDF...")
        if final_html:
            step_html_to_pdf(output_dir, final_html)
            print()
        else:
            print("  SKIPPED: No HTML file found. Complete step 3 first.\n")
    else:
        print("[6/6] Skipped (html-to-pdf)\n")

    # --- Summary ---
    elapsed = time.time() - t0
    print(f"{'='*60}")
    print(f"  Pipeline complete ({elapsed:.1f}s)")
    print(f"{'='*60}")

    # List output files
    if os.path.isdir(output_dir):
        files = sorted(os.listdir(output_dir))
        output_files = [f for f in files if not f.startswith('_')]
        if output_files:
            print(f"  Output files:")
            for f in output_files:
                fpath = os.path.join(output_dir, f)
                size = os.path.getsize(fpath)
                size_str = f"{size/1024:.1f}KB" if size > 1024 else f"{size}B"
                print(f"    {f} ({size_str})")
        print()


if __name__ == '__main__':
    main()
