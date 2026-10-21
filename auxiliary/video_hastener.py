#!/usr/bin/env python3
"""
Speed up all .webm files in a directory by 4x, removing audio.
Requires ffmpeg to be installed and available on PATH.
"""

from pathlib import Path
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from moviepy import VideoFileClip


SPEED_FACTOR = 4.0
INPUT_DIR = "/home/maxlg/Videos/Screencasts"   # Change this to your source directory
OUTPUT_DIR = "/home/maxlg/Videos/Screencasts/Speedups" # Change this to your desired output directory
FFMPEG_BIN = "/home/maxlg/ffmpeg-master-latest-linux64-gpl/bin/ffmpeg"

def speed_up_video(input_path: Path, output_path: Path, speed: float) -> tuple[str, bool, str]:
    """Speed up a single video, strip audio, and save as mp4.
    Returns (filename, success, error_message).
    """
    try:
        with VideoFileClip(str(input_path)) as clip:
            sped_up = clip.with_speed_scaled(speed).without_audio()
            sped_up.write_videofile(
                str(output_path),
                codec="libx264",
                preset="fast",
                logger="bar",   # shows a progress bar per file
            )
        return (input_path.name, True, "")
    except Exception as e:
        return (input_path.name, False, str(e))
 
 
def main():
    input_dir = Path(INPUT_DIR)
    output_dir = Path(OUTPUT_DIR)
 
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)
 
    webm_files = sorted(input_dir.glob("*.webm"))
    if not webm_files:
        print(f"No .webm files found in '{input_dir}'.")
        sys.exit(0)
 
    output_dir.mkdir(parents=True, exist_ok=True)
 
    print(f"Found {len(webm_files)} .webm file(s) in '{input_dir}'.")
    print(f"Speed factor: {SPEED_FACTOR}x | Audio: removed | Encoder: libx264")
    print(f"Output directory: '{output_dir}'\n")
 
    success_count = 0
    fail_count = 0
 
    max_workers = 9
    print(f"Parallel workers: {max_workers}\n")

    future_to_job = {}
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i, input_path in enumerate(webm_files, start=1):
            output_path = output_dir / (input_path.stem + ".mp4")
            print(f"[{i}/{len(webm_files)}] Queued {input_path.name}")
            future = executor.submit(speed_up_video, input_path, output_path, SPEED_FACTOR)
            future_to_job[future] = (input_path, output_path)

        for future in as_completed(future_to_job):
            input_path, output_path = future_to_job[future]
            try:
                filename, ok, err = future.result()
            except Exception as e:
                filename, ok, err = input_path.name, False, str(e)

            if ok:
                print(f"  ✓ Done {filename} -> {output_path.name}\n")
                success_count += 1
            else:
                print(f"  ✗ FAILED {filename}: {err}\n")
                fail_count += 1
 
    print(f"Done. {success_count} succeeded, {fail_count} failed.")
 
 
if __name__ == "__main__":
    main()
