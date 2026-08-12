"""Entry point for live video stream processing.

Run directly:
    python main.py                    # synthetic stream, text GUI
    python main.py --stream 0         # local webcam index 0
    python main.py --stream rtsp://...# RTSP source
    python main.py --image path.jpg   # analyze a single image and exit

Environment:
    GEMINI_API_KEY                    enables the Gemini engines (optional)
"""

from __future__ import annotations

import argparse
import sys

from ui import TextGUI


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Vision AI - autonomous scene understanding")
    p.add_argument("--stream", default=None,
                   help="Camera source: webcam index (e.g. 0), RTSP URL, or 'synthetic'")
    p.add_argument("--image", default=None,
                   help="Analyze a single image file and exit")
    p.add_argument("--ask", default="",
                   help="Natural-language instruction for the vision agent")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    gui = TextGUI()
    if args.ask:
        gui.instruction = args.ask

    if args.image:
        gui.handle(f"image {args.image}")
        return 0

    if args.stream is not None:
        if args.stream.lower() in ("synthetic", "synth", ""):
            gui.handle("stream")
        elif args.stream.isdigit():
            gui.handle(f"webcam {args.stream}")
        else:
            gui.handle(f"stream {args.stream}")
    else:
        gui.handle("stream")

    gui.loop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
