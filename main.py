#!/usr/bin/env python3
"""One Word for Your Wi-Fi — the entry program.

Writes exactly one word (10 characters) to /output/entry.txt.
Standard library only. No network, no reading of files outside this
program, no local imports. The write is atomic (temp file + rename)
and verified by reading the file back byte-for-byte.
"""

import os
import sys
import tempfile
import unicodedata

ENTRY = "Politician"

MAX_CHARS = 20


def validate(text):
    """Check the entry against the gate: 1-20 chars, one word, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be whitespace only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if " " in text or "\t" in text:
        raise ValueError("entry must be a single word")
    for char in text:
        if unicodedata.category(char) == "Cc":
            raise ValueError(
                "entry must not contain control character U+%04X" % ord(char)
            )
    # UTF-8 must round-trip exactly: encode, decode, compare.
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry is not valid UTF-8 text")
    return text


def write_entry(output_dir):
    """Atomically write the validated entry and verify it by read-back."""
    text = validate(ENTRY)
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, "entry.txt")
    data = text.encode("utf-8")
    fd, tmp_path = tempfile.mkstemp(
        dir=output_dir, prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, target)
        # Fsync the directory too, so the rename itself is durable
        # and a crash cannot lose the finished entry.
        dir_fd = os.open(output_dir, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    with open(target, "rb") as handle:
        read_back = handle.read()
    if read_back != data:
        raise ValueError("read-back mismatch: entry.txt differs from entry")
    if read_back.decode("utf-8") != text:
        raise ValueError("read-back mismatch: entry.txt is not the entry text")
    return len(text)


def main():
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    count = write_entry(output_dir)
    print("Wrote %d characters to %s" % (count, os.path.join(output_dir, "entry.txt")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
