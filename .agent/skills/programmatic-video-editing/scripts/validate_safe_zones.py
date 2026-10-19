#!/usr/bin/env python3
"""
Validate Safe Zones - Ananke OS Programmatic Video Suite
========================================================

Verifies that elements in a vertical video layout (1080x1920) respect 
the strict safe zone boundaries of Instagram Reels, TikTok, and YouTube Shorts.

Usage:
    python validate_safe_zones.py [--json layout.json]
    python validate_safe_zones.py --check-element "title" --y 300 --h 80 --x 100 --w 800
"""

import sys
import json
import argparse
from typing import Dict, List, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920

# Safe zones definitions
SAFE_ZONES = {
    "graphics": {"min_y": 250, "max_y": 800},
    "face_card": {"min_y": 820, "max_y": 1300},
    "captions": {"min_y": 1360, "max_y": 1480},
    "blind_bottom": 1520,      # Everything below is obscured by UI (captions, music, username)
    "blind_right_edge": 950,    # 130px from right edge (1080 - 130) reserved for action buttons
    "min_lateral_padding": 90,  # At least 90px padding on left and right
}

def check_element(name: str, x: int, y: int, width: int, height: int, element_type: str = "general") -> List[str]:
    violations = []
    bottom_y = y + height
    right_x = x + width

    # Check horizontal margins
    if x < SAFE_ZONES["min_lateral_padding"]:
        violations.append(f"Element '{name}' starts at X={x}px (less than lateral safe margin {SAFE_ZONES['min_lateral_padding']}px).")

    if right_x > (CANVAS_WIDTH - SAFE_ZONES["min_lateral_padding"]):
        violations.append(f"Element '{name}' ends at X={right_x}px (exceeds lateral safe margin {CANVAS_WIDTH - SAFE_ZONES['min_lateral_padding']}px).")

    # Check right button collision
    if right_x > SAFE_ZONES["blind_right_edge"] and y > 600:
        violations.append(f"Element '{name}' overlaps right-hand action buttons area (X={right_x}px > {SAFE_ZONES['blind_right_edge']}px).")

    # Check bottom blind zone
    if bottom_y >= SAFE_ZONES["blind_bottom"]:
        violations.append(f"Element '{name}' reaches Y={bottom_y}px, falling into bottom UI dead zone (>= {SAFE_ZONES['blind_bottom']}px).")

    # Check specific layer zones if provided
    if element_type == "graphics":
        if y < SAFE_ZONES["graphics"]["min_y"] or bottom_y > SAFE_ZONES["graphics"]["max_y"]:
            violations.append(f"Graphic element '{name}' [Y: {y}-{bottom_y}px] outside graphics sweet spot ({SAFE_ZONES['graphics']['min_y']}-{SAFE_ZONES['graphics']['max_y']}px).")
    elif element_type == "captions":
        if y < SAFE_ZONES["captions"]["min_y"] or bottom_y > SAFE_ZONES["captions"]["max_y"]:
            violations.append(f"Caption element '{name}' [Y: {y}-{bottom_y}px] outside caption safe band ({SAFE_ZONES['captions']['min_y']}-{SAFE_ZONES['captions']['max_y']}px).")
    elif element_type == "face_card":
        if y < SAFE_ZONES["face_card"]["min_y"] or bottom_y > SAFE_ZONES["face_card"]["max_y"]:
            violations.append(f"Face card '{name}' [Y: {y}-{bottom_y}px] outside recommended face region ({SAFE_ZONES['face_card']['min_y']}-{SAFE_ZONES['face_card']['max_y']}px).")

    return violations

def validate_layout_dict(layout: Dict) -> bool:
    all_passed = True
    print("\n🔍 Validating Layout Safe Zones (Canvas: 1080x1920)\n" + "-"*50)
    elements = layout.get("elements", [])
    for el in elements:
        name = el.get("name", "unnamed")
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0)
        h = el.get("height", 0)
        el_type = el.get("type", "general")

        violations = check_element(name, x, y, w, h, el_type)
        if violations:
            all_passed = False
            print(f"❌ [{name}] Violations detected:")
            for v in violations:
                print(f"   • {v}")
        else:
            print(f"✅ [{name}] OK (X: {x}-{x+w}px, Y: {y}-{y+h}px)")

    print("-" * 50)
    if all_passed:
        print("🎉 ALL ELEMENTS WITHIN SAFE ZONES!\n")
    else:
        print("⚠️ SOME ELEMENTS VIOLATE SAFE ZONE LIMITS.\n")
    return all_passed

def main():
    parser = argparse.ArgumentParser(description="Validate video elements safe zones.")
    parser.add_argument("--json", dest="json_file", help="Path to JSON file containing layout elements")
    parser.add_argument("--check-element", help="Element name to test")
    parser.add_argument("--type", default="general", choices=["general", "graphics", "captions", "face_card"])
    parser.add_argument("--x", type=int, default=100)
    parser.add_argument("--y", type=int, default=300)
    parser.add_argument("--w", type=int, default=800)
    parser.add_argument("--h", type=int, default=100)

    args = parser.parse_args()

    if args.json_file:
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        passed = validate_layout_dict(data)
        sys.exit(0 if passed else 1)
    elif args.check_element:
        violations = check_element(args.check_element, args.x, args.y, args.w, args.h, args.type)
        if violations:
            print(f"❌ Violations for '{args.check_element}':")
            for v in violations:
                print(f"   • {v}")
            sys.exit(1)
        else:
            print(f"✅ Element '{args.check_element}' is within safe zones.")
            sys.exit(0)
    else:
        # Default self-test layout
        test_layout = {
            "elements": [
                {"name": "hook_title", "type": "graphics", "x": 100, "y": 300, "width": 800, "height": 150},
                {"name": "face_window", "type": "face_card", "x": 140, "y": 850, "width": 750, "height": 400},
                {"name": "subtitles", "type": "captions", "x": 120, "y": 1380, "width": 800, "height": 80}
            ]
        }
        passed = validate_layout_dict(test_layout)
        sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
