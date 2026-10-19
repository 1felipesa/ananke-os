#!/usr/bin/env python3
"""
Extract Stills CLI - Ananke OS Programmatic Video Suite
=====================================================

Extracts keyframes/stills from a reference video or rendering output using FFmpeg.
Prevents coding agents from attempting to buffer full MP4 binaries.

Usage:
    python extract_stills.py <input_video.mp4> <output_dir> [--fps 1]
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def extract_stills(video_path: str, output_dir: str, fps: float = 1.0) -> bool:
    input_path = Path(video_path).resolve()
    out_dir = Path(output_dir).resolve()

    if not input_path.exists():
        print(f"❌ Error: Video file not found at {input_path}")
        return False

    out_dir.mkdir(parents=True, exist_ok=True)

    # Output pattern
    out_pattern = str(out_dir / "frame-%03d.jpg")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vf", f"fps={fps}",
        "-q:v", "2",
        out_pattern
    ]

    print(f"🎬 Extracting stills from: {input_path.name}")
    print(f"📁 Destination: {out_dir}")
    print(f"⚡ Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"❌ FFmpeg execution failed:\n{result.stderr}")
            return False

        frames = list(out_dir.glob("frame-*.jpg"))
        print(f"✅ Successfully extracted {len(frames)} frames.")
        return True
    except FileNotFoundError:
        print("❌ Error: 'ffmpeg' not found in system PATH. Please ensure FFmpeg is installed.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Extract video stills using FFmpeg.")
    parser.add_argument("video", help="Path to input MP4 video")
    parser.add_argument("output", help="Directory to save extracted stills")
    parser.add_argument("--fps", type=float, default=1.0, help="Frames per second to extract (default: 1.0)")

    args = parser.parse_args()
    success = extract_stills(args.video, args.output, args.fps)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
