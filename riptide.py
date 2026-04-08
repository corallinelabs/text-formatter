#!/usr/bin/env python3
"""riptide — cleans up terminal-copied text

Usage:
    pbpaste | python riptide.py [--pr]
    pbpaste | python riptide.py [--pr] | pbcopy
"""

import argparse
import re
import sys


def clean_text(text: str) -> str:
    """Strip whitespace padding and unwrap hard-wrapped paragraphs."""
    lines = [line.strip() for line in text.splitlines()]

    # Group lines into blocks: paragraphs and bullet items
    # A bullet continuation is a non-blank, non-bullet line following a bullet
    blocks = []
    current_lines = []
    current_type = None  # "text" or "bullet"

    for line in lines:
        if line == "":
            if current_lines:
                blocks.append((current_type, current_lines))
                current_lines = []
                current_type = None
            continue

        is_bullet = line.startswith("- ")

        if is_bullet:
            # If we were accumulating text, flush it
            if current_type == "text" and current_lines:
                blocks.append((current_type, current_lines))
                current_lines = []
            current_type = "bullet"
            current_lines.append(line)
        elif current_type == "bullet":
            # Continuation of the previous bullet (wrapped line)
            current_lines[-1] += " " + line
        else:
            current_type = "text"
            current_lines.append(line)

    if current_lines:
        blocks.append((current_type, current_lines))

    # Build output: rejoin text lines, keep bullets separate
    result = []
    for block_type, block_lines in blocks:
        if result:
            result.append("")
        if block_type == "text":
            # Rejoin wrapped text into a single paragraph
            joined = " ".join(block_lines)
            # Normalize multiple spaces from joining
            joined = re.sub(r"  +", " ", joined)
            result.append(joined)
        else:
            for bullet in block_lines:
                # Normalize spaces within bullet
                result.append(re.sub(r"  +", " ", bullet))

    return "\n".join(result)


def format_pr(text: str) -> str:
    """Format cleaned text as a PR description: summary line + bullets."""
    cleaned = clean_text(text)
    lines = cleaned.split("\n")

    # Separate into paragraphs (split on blank lines)
    paragraphs = []
    current = []
    for line in lines:
        if line == "":
            if current:
                paragraphs.append(current)
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(current)

    if not paragraphs:
        return ""

    # First non-bullet paragraph becomes the summary
    summary = None
    bullets = []

    for para in paragraphs:
        for line in para:
            if line.startswith("- "):
                bullets.append(line)
            elif summary is None:
                summary = line
            else:
                # Additional non-bullet text becomes a bullet
                bullets.append(f"- {line}")

    if summary is None:
        if bullets:
            summary = re.sub(r"^- ", "", bullets.pop(0))
        else:
            return ""

    # Strip trailing period from summary
    summary = summary.rstrip(".")

    parts = [summary]
    if bullets:
        parts.append("")
        parts.extend(bullets)

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Clean up terminal-copied text.")
    parser.add_argument(
        "--pr", action="store_true", help="Output in PR format (summary + bullets)"
    )
    args = parser.parse_args()

    text = sys.stdin.read()

    if args.pr:
        print(format_pr(text))
    else:
        print(clean_text(text))


if __name__ == "__main__":
    main()
