#!/usr/bin/env python3
"""Convert SRT subtitles between Traditional and Simplified Chinese using OpenCC."""

import argparse
import sys
from pathlib import Path

from opencc import OpenCC

CONFIGS = {
    "t2s": "t2s",       # Traditional to Simplified
    "s2t": "s2t",       # Simplified to Traditional
    "t2tw": "t2tw",     # Traditional to Taiwan Standard
    "tw2s": "tw2s",     # Taiwan Traditional to Simplified
    "s2tw": "s2tw",     # Simplified to Taiwan Traditional
    "t2hk": "t2hk",     # Traditional to Hong Kong
    "hk2s": "hk2s",     # Hong Kong to Simplified
    "s2hk": "s2hk",     # Simplified to Hong Kong
    "tw2sp": "tw2sp",   # Taiwan Traditional to Simplified with phrases
    "s2twp": "s2twp",   # Simplified to Taiwan Traditional with phrases
}


def convert_srt(input_path: Path, output_path: Path, config: str) -> None:
    converter = OpenCC(config)
    text = input_path.read_text(encoding="utf-8")
    converted = converter.convert(text)
    output_path.write_text(converted, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert SRT subtitles between Chinese variants")
    parser.add_argument("input", type=Path, help="Input SRT file")
    parser.add_argument("-o", "--output", type=Path, help="Output SRT file (default: input_<config>.srt)")
    parser.add_argument(
        "-c", "--config", default="t2s", choices=sorted(CONFIGS),
        help="OpenCC conversion config (default: t2s)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    output = args.output or args.input.with_stem(f"{args.input.stem}_{args.config}")
    convert_srt(args.input, output, CONFIGS[args.config])
    print(f"Converted {args.input} -> {output} ({args.config})")


if __name__ == "__main__":
    main()
