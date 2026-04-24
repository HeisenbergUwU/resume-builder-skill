#!/usr/bin/env python3
"""Convert an HTML resume to PDF.

Supports weasyprint (recommended) or system tools (wkhtmltopdf, chromium) as fallback.
"""

import argparse
import os
import shutil
import subprocess
import sys


def try_weasyprint(html_path, pdf_path):
    """Convert using weasyprint (best quality, pure Python)."""
    try:
        from weasyprint import HTML
        HTML(filename=html_path).write_pdf(pdf_path)
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"ERROR: weasyprint failed: {e}", file=sys.stderr)
        return False


def try_wkhtmltopdf(html_path, pdf_path):
    """Convert using wkhtmltopdf system tool."""
    if not shutil.which('wkhtmltopdf'):
        return False
    cmd = ['wkhtmltopdf', '--no-outline', '--margin-top', '0',
           '--margin-bottom', '0', '--margin-left', '0', '--margin-right', '0',
           html_path, pdf_path]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, timeout=60)
        if result.returncode == 0:
            return True
    except subprocess.TimeoutExpired:
        print("ERROR: wkhtmltopdf timed out", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: wkhtmltopdf failed: {e.stderr.decode('utf-8', errors='replace')}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: wkhtmltopdf failed: {e}", file=sys.stderr)
    return False


def try_chromium(html_path, pdf_path):
    """Convert using headless Chromium."""
    chrome = shutil.which('chromium') or shutil.which('google-chrome')
    if not chrome:
        return False
    cmd = [chrome, '--headless', '--disable-gpu',
           '--print-to-pdf=' + pdf_path,
           '--no-margins', 'file://' + os.path.abspath(html_path)]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, timeout=60)
        if result.returncode == 0:
            return True
    except subprocess.TimeoutExpired:
        print("ERROR: Chromium timed out", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Chromium failed: {e.stderr.decode('utf-8', errors='replace')}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: Chromium failed: {e}", file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(description='Convert HTML resume to PDF')
    parser.add_argument('html', help='Path to HTML resume file')
    parser.add_argument('--output', '-o', help='Output PDF path (default: same name as HTML)')
    args = parser.parse_args()

    if not os.path.isfile(args.html):
        print(f"ERROR: HTML file not found: {args.html}", file=sys.stderr)
        sys.exit(1)

    pdf_path = args.output or os.path.splitext(args.html)[0] + '.pdf'
    abs_html = os.path.abspath(args.html)

    methods = [
        ('weasyprint', lambda: try_weasyprint(abs_html, pdf_path)),
        ('wkhtmltopdf', lambda: try_wkhtmltopdf(abs_html, pdf_path)),
        ('chromium', lambda: try_chromium(abs_html, pdf_path)),
    ]

    for name, fn in methods:
        if fn():
            print(f"PDF generated ({name}) -> {pdf_path}")
            return

    print(f"No PDF converter found. Install one of:", file=sys.stderr)
    print(f"  pip install weasyprint     (recommended, pure Python)", file=sys.stderr)
    print(f"  brew install wkhtmltopdf   (system tool)", file=sys.stderr)
    print(f"  brew install chromium       (headless browser)", file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
