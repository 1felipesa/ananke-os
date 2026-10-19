#!/usr/bin/env python3
"""
Ethical Lead Scraper & Contact Extractor - Ananke OS
===================================================

Extracts corporate email addresses from public web pages, filters out false
positives (media files, placeholder domains), and exports clean leads to CSV.

Usage:
    python lead_scraper.py <URL> [-o leads.csv]
    python lead_scraper.py --file urls.txt [-o leads.csv]
"""

import sys
import os
import re
import csv
import time
import argparse
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse, urljoin

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Strict email regex preventing images or asset strings
EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    re.IGNORECASE,
)

# Invalid file extensions or false positive patterns
INVALID_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".css", ".js",
    ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".mp3", ".pdf", ".zip"
)

# Placeholder or generic domains to ignore
IGNORE_DOMAINS = {
    "example.com", "domain.com", "email.com", "yourdomain.com",
    "test.com", "sample.com", "sentry.io", "wixpress.com"
}


def clean_email(candidate: str) -> str:
    """Sanitizes extracted email string and validates against false positives."""
    candidate = candidate.strip().lower()
    candidate = candidate.rstrip(".,;:'\")>]}?")
    candidate = candidate.lstrip("mailto:")

    # Check extension
    for ext in INVALID_EXTENSIONS:
        if candidate.endswith(ext):
            return None

    # Check domain
    if "@" not in candidate:
        return None

    user, domain = candidate.split("@", 1)
    if not user or not domain or "." not in domain:
        return None

    if domain in IGNORE_DOMAINS:
        return None

    return candidate


def fetch_page_content(url: str, timeout: int = 10) -> str:
    """Fetches HTML content with friendly User-Agent."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type and "text/plain" not in content_type:
                return ""
            html = response.read().decode("utf-8", errors="ignore")
            return html
    except (HTTPError, URLError, Exception) as e:
        print(f"⚠️ Warning: Could not fetch {url}: {e}", file=sys.stderr)
        return ""


def extract_leads_from_url(url: str) -> list:
    """Extracts valid leads from single URL."""
    html = fetch_page_content(url)
    if not html:
        return []

    domain = urlparse(url).netloc
    matches = EMAIL_REGEX.findall(html)
    found_emails = set()

    for match in matches:
        cleaned = clean_email(match)
        if cleaned:
            found_emails.add(cleaned)

    results = []
    capture_date = time.strftime("%Y-%m-%d %H:%M:%S")
    for email in sorted(found_emails):
        results.append({
            "email": email,
            "domain": domain,
            "source_url": url,
            "captured_at": capture_date,
        })
    return results


def export_leads_to_csv(leads: list, output_csv: str):
    """Saves leads list to CSV."""
    fieldnames = ["email", "domain", "source_url", "captured_at"]
    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            writer.writerow(lead)


def main():
    parser = argparse.ArgumentParser(description="Ethical Lead Scraper for B2B Contact Discovery.")
    parser.add_argument("url", nargs="?", help="Target website URL")
    parser.add_argument("--file", "-f", help="Text file containing list of URLs (one per line)")
    parser.add_argument("-o", "--output", help="Output CSV path", default="leads.csv")

    args = parser.parse_args()

    urls_to_scrape = []
    if args.url:
        urls_to_scrape.append(args.url)
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ Error: File not found {args.file}", file=sys.stderr)
            sys.exit(1)
        urls_to_scrape = [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        parser.print_help()
        sys.exit(1)

    all_leads = []
    seen_emails = set()

    print(f"🔍 Starting lead extraction on {len(urls_to_scrape)} URL(s)...")
    for u in urls_to_scrape:
        leads = extract_leads_from_url(u)
        for lead in leads:
            if lead["email"] not in seen_emails:
                seen_emails.add(lead["email"])
                all_leads.append(lead)
        time.sleep(0.5)  # Friendly delay

    export_leads_to_csv(all_leads, args.output)
    print(f"✅ Success! {len(all_leads)} unique lead(s) exported to {args.output}")


if __name__ == "__main__":
    main()
