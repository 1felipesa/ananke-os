#!/usr/bin/env python3
"""
Skill: performance-profiling
Script: bundle_analyzer.py
Purpose: Analyze build output sizes (JS/CSS) to prevent bloated deployments
Usage: python bundle_analyzer.py <project_path>
"""
import sys
import os
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Fix Windows console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

# Budgets in bytes
JS_BUDGET = 2 * 1024 * 1024  # 2 MB limit for JS
CSS_BUDGET = 500 * 1024      # 500 KB limit for CSS

def get_directory_size_by_ext(directory: Path, extension: str) -> int:
    total_size = 0
    for root_dir, _, files in os.walk(directory):
        for f in files:
            if f.endswith(extension):
                fp = os.path.join(root_dir, f)
                total_size += os.path.getsize(fp)
    return total_size

def format_size(size_in_bytes: int) -> str:
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    else:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"

def analyze_bundle(project_path: Path):
    # Common build directories
    build_dirs = ["build", "dist", ".next", "out"]
    
    target_dir = None
    for d in build_dirs:
        candidate = project_path / d
        if candidate.exists() and candidate.is_dir():
            target_dir = candidate
            break
            
    if not target_dir:
        print(f"{Colors.YELLOW}⚠️  No build directory found (looked for: {', '.join(build_dirs)}). Run build command first. Skipping bundle analysis.{Colors.ENDC}")
        return True

    print(f"{Colors.BLUE}🔍 Analyzing bundle size in '{target_dir.name}'...{Colors.ENDC}")
    
    js_size = get_directory_size_by_ext(target_dir, ".js")
    css_size = get_directory_size_by_ext(target_dir, ".css")
    
    print(f"📦 Total JS Size:  {format_size(js_size)} (Budget: {format_size(JS_BUDGET)})")
    print(f"🎨 Total CSS Size: {format_size(css_size)} (Budget: {format_size(CSS_BUDGET)})")
    
    errors = 0
    if js_size > JS_BUDGET:
        print(f"{Colors.RED}❌ ERROR: JavaScript bundle size exceeds {format_size(JS_BUDGET)} budget!{Colors.ENDC}")
        errors += 1
    
    if css_size > CSS_BUDGET:
        print(f"{Colors.RED}❌ ERROR: CSS bundle size exceeds {format_size(CSS_BUDGET)} budget!{Colors.ENDC}")
        errors += 1
        
    if errors > 0:
        print(f"\n{Colors.RED}❌ Bundle analysis FAILED. Bloated assets detected.{Colors.ENDC}")
        return False
    else:
        print(f"\n{Colors.GREEN}✅ Bundle analysis PASSED. Asset sizes are within budgets.{Colors.ENDC}")
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python bundle_analyzer.py <project_path>")
        sys.exit(1)
        
    project_path = Path(sys.argv[1]).resolve()
    
    success = analyze_bundle(project_path)
    
    if not success:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
