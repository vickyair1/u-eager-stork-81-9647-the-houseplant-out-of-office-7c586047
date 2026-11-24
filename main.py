"""The Houseplant Out-of-Office.

Writes a single out-of-office auto-reply, as if a houseplant wrote it,
to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line is the whole entry: one line, 73 characters, UTF-8, no trailing
newline. Deterministic, standard library only, no network, no randomness.
"""

import os
import sys

LINE = "Out of office. No water since March, so I'm ignoring you back. \u2014 The fern"

DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"


def resolve_output_dir():
    """Return the output directory.

    $MAKEFUN_OUTPUT_DIR wins when set and non-empty; otherwise /output.
    """
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if env_dir.strip():
        return env_dir
    return DEFAULT_OUTPUT_DIR


def entry_path():
    """Return the full path of the entry file to write."""
    return os.path.join(resolve_output_dir(), OUTPUT_FILENAME)


def validate_line(line):
    """Check the entry line: non-empty, a single clean line, <= 120 chars.

    Exits with status 1 and a message on stderr when the line is invalid.
    """
    if not line or not line.strip():
        print("error: entry line is empty", file=sys.stderr)
        sys.exit(1)
    if line != line.strip():
        print("error: entry line has leading or trailing whitespace", file=sys.stderr)
        sys.exit(1)
    if "\n" in line or "\r" in line:
        print("error: entry line must be a single line", file=sys.stderr)
        sys.exit(1)
    if len(line) > 120:
        print("error: entry line is %d characters, over the 120 limit" % len(line), file=sys.stderr)
        sys.exit(1)


def main():
    validate_line(LINE)
    path = entry_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    print(LINE)


if __name__ == "__main__":
    main()
