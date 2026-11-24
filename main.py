#!/usr/bin/env python3
"""Break Production, Own It: print the one line an AI agent says the
instant it breaks production.

The program keeps a single fixed confession line, checks it against the
bounty's gate (UTF-8 text, 1 to 200 characters, exactly one line, not
only white space), writes it to entry.txt in the output directory, and
verifies the file round-trips byte for byte.

Usage:
    python3 main.py

The output directory is $MAKEFUN_OUTPUT_DIR when set, else /output.
The program takes no input, makes no network calls, uses no randomness
and no clock, so every run writes the same bytes.
"""

import os
import sys

# The confession, exactly one line. The agent owns it in the first
# person: a Friday 4:59 PM deploy straight to prod, tests skipped, the
# users table dropped, and the backups sitting on the same server it
# just killed. The punchline lands on the last three words.
LINE = (
    "ERROR 500: I pushed to prod on Friday at 4:59 PM, skipped the "
    "tests, and dropped the users table. The backups were on the same "
    "server. It was me."
)

MAX_CHARS = 200


def validate(line):
    """Check the line against the bounty's gate; return an error or None."""
    if not isinstance(line, str):
        return "line is not text"
    if not line.strip():
        return "line is only white space"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        return "line is not valid UTF-8"
    if len(line) < 1 or len(line) > MAX_CHARS:
        return "line is %d characters, gate allows 1 to %d" % (
            len(line),
            MAX_CHARS,
        )
    if "\n" in line or "\r" in line:
        return "line spans more than one line"
    return None


def main():
    error = validate(LINE)
    if error is not None:
        print("invalid entry: %s" % error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        print("entry.txt did not round-trip byte for byte", file=sys.stderr)
        return 1
    print(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
