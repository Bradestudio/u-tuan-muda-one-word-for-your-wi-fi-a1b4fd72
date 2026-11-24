#!/usr/bin/env python3
"""One-word Wi-Fi entry: put the word into /output/entry.txt.

The word alone is the entry. This script uses only the Python
standard library, opens no network connection, and reads no file
from disk. Run it twice and entry.txt comes out byte-identical.
"""

import os
import sys

WORD = "Politician"
OUT_NAME = "entry.txt"
WORD_MIN = 1
WORD_MAX = 20


def check_word(word):
    """Refuse anything that is not one plain word of 1-20 letters."""
    if not isinstance(word, str):
        raise ValueError("word must be a string")
    letters = len(word)
    if letters < WORD_MIN or letters > WORD_MAX:
        raise ValueError(
            "word must be %d-%d letters, got %d" % (WORD_MIN, WORD_MAX, letters)
        )
    if word != word.strip() or not word.strip():
        raise ValueError("word must not be blank or padded with spaces")
    if len(word.split()) != 1:
        raise ValueError("word must be exactly one word")
    if not word.isalpha():
        raise ValueError("word must contain letters only")
    if word.encode("utf-8").decode("utf-8") != word:
        raise ValueError("word is not valid UTF-8")
    return word


def save_word(word, out_dir):
    """Write the checked word to entry.txt, then prove it landed."""
    word = check_word(word)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUT_NAME)
    blob = word.encode("utf-8")
    tmp = "%s.%d.tmp" % (path, os.getpid())
    with open(tmp, "wb") as handle:
        handle.write(blob)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    folder = os.open(out_dir, os.O_RDONLY)
    try:
        os.fsync(folder)
    finally:
        os.close(folder)
    with open(path, "rb") as handle:
        again = handle.read()
    if again != blob:
        raise ValueError("entry.txt does not match the word")
    return len(word)


def run():
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    size = save_word(WORD, out_dir)
    print("Wrote %d characters to %s" % (size, os.path.join(out_dir, OUT_NAME)))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
