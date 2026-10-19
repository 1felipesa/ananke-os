#!/usr/bin/env python3
"""
E-mail HTML Inline Styler & Plaintext Generator - Ananke OS
===========================================================

Converts CSS <style> declarations into inline style="" attributes and generates
a clean plain-text mirror for bulletproof email deliverability across Outlook, Gmail and Apple Mail.

Usage:
    python inline_styler.py input.html [-o output_inlined.html] [-t output_plain.txt]
"""

import sys
import os
import re
import argparse
from pathlib import Path
from html.parser import HTMLParser

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class HTMLToPlainText(HTMLParser):
    """Simple parser to extract structured plain text from HTML email."""

    def __init__(self):
        super().__init__()
        self.pieces = []
        self.ignore = False

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script", "head"):
            self.ignore = True
        elif tag in ("p", "div", "tr", "h1", "h2", "h3", "h4", "h5", "h6"):
            self.pieces.append("\n")
        elif tag == "br":
            self.pieces.append("\n")
        elif tag == "li":
            self.pieces.append("\n• ")
        elif tag == "a":
            for attr, val in attrs:
                if attr == "href" and val.startswith("http"):
                    self.pieces.append(f" ")

    def handle_endtag(self, tag):
        if tag in ("style", "script", "head"):
            self.ignore = False
        elif tag in ("p", "div", "tr", "table", "h1", "h2", "h3", "h4", "h5", "h6"):
            self.pieces.append("\n")

    def handle_data(self, data):
        if not self.ignore:
            text = re.sub(r"\s+", " ", data)
            if text:
                self.pieces.append(text)

    def get_text(self) -> str:
        raw = "".join(self.pieces)
        lines = [line.strip() for line in raw.split("\n")]
        # Deduplicate multiple empty lines
        cleaned = []
        last_empty = False
        for line in lines:
            if not line:
                if not last_empty:
                    cleaned.append("")
                    last_empty = True
            else:
                cleaned.append(line)
                last_empty = False
        return "\n".join(cleaned).strip()


def parse_css_declarations(css_text: str) -> dict:
    """Extracts simple CSS selector -> rules dictionary."""
    css_text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.DOTALL)
    rules = {}
    pattern = re.compile(r"([^{]+)\{([^}]+)\}")
    for match in pattern.finditer(css_text):
        selectors = match.group(1).strip().split(",")
        body = match.group(2).strip().replace("\n", " ")
        cleaned_body = "; ".join([decl.strip() for decl in body.split(";") if decl.strip()])
        if cleaned_body and not cleaned_body.endswith(";"):
            cleaned_body += ";"
        for sel in selectors:
            sel = sel.strip()
            if sel and not sel.startswith("@"):
                rules[sel] = cleaned_body
    return rules


def inline_html_styles(html_content: str) -> str:
    """Inlines styles from <style> blocks directly into HTML tags."""
    # Extract <style> blocks
    style_pattern = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)
    all_css = []
    for match in style_pattern.finditer(html_content):
        all_css.append(match.group(1))

    combined_css = "\n".join(all_css)
    rules = parse_css_declarations(combined_css)

    inlined_html = html_content

    # Apply class-based selectors (.class-name)
    for selector, css_rule in rules.items():
        if selector.startswith("."):
            class_name = selector[1:]
            # Match tag with this class
            class_regex = re.compile(
                rf'(<[a-zA-Z0-9]+[^>]*?\bclass=[\'"][^\'"]*?\b{re.escape(class_name)}\b[^\'"]*?[\'"][^>]*?>)',
                re.IGNORECASE,
            )

            def inject_style(match):
                tag_str = match.group(1)
                if 'style="' in tag_str:
                    return re.sub(
                        r'style="([^"]*)"',
                        lambda m: f'style="{m.group(1).rstrip(";")}; {css_rule}"',
                        tag_str,
                    )
                elif "style='" in tag_str:
                    return re.sub(
                        r"style='([^']*)'",
                        lambda m: f"style='{m.group(1).rstrip(';')}; {css_rule}'",
                        tag_str,
                    )
                else:
                    return tag_str[:-1] + f' style="{css_rule}">'

            inlined_html = class_regex.sub(inject_style, inlined_html)

    return inlined_html


def process_email_template(input_path: str, output_html: str = None, output_txt: str = None) -> dict:
    in_file = Path(input_path)
    if not in_file.exists():
        raise FileNotFoundError(f"Template file not found: {input_path}")

    raw_html = in_file.read_text(encoding="utf-8")

    # 1. Inline CSS
    inlined = inline_html_styles(raw_html)

    # 2. Extract Plain Text
    converter = HTMLToPlainText()
    converter.feed(raw_html)
    plain_text = converter.get_text()

    # Determine default output paths
    if not output_html:
        output_html = str(in_file.parent / f"{in_file.stem}_inlined.html")
    if not output_txt:
        output_txt = str(in_file.parent / f"{in_file.stem}_plain.txt")

    Path(output_html).write_text(inlined, encoding="utf-8")
    Path(output_txt).write_text(plain_text, encoding="utf-8")

    return {
        "status": "success",
        "inlined_html": output_html,
        "plain_text": output_txt,
        "html_size_bytes": len(inlined.encode("utf-8")),
        "plain_size_bytes": len(plain_text.encode("utf-8")),
    }


def main():
    parser = argparse.ArgumentParser(description="Inlines styles and extracts plaintext for e-mail templates.")
    parser.add_argument("input_html", help="Path to input HTML template")
    parser.add_argument("-o", "--output-html", help="Path for inlined HTML output", default=None)
    parser.add_argument("-t", "--output-txt", help="Path for plaintext output", default=None)

    args = parser.parse_args()

    try:
        res = process_email_template(args.input_html, args.output_html, args.output_txt)
        print(f"✅ Inlined HTML created: {res['inlined_html']} ({res['html_size_bytes']} bytes)")
        print(f"✅ Plain Text mirror created: {res['plain_text']} ({res['plain_size_bytes']} bytes)")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
