"""The One-Sentence Apology Your Agent Owes You.

A program/v1 entry: it writes a single sentence of apology, as if an AI
assistant were owning up to the person it works for, to /output/entry.txt.

The sentence is fixed and hand-written: the grader runs the program twice
and both runs must produce the same text, so nothing here is random, no
clock is read, and no input is consumed. The program only assembles the
sentence from its parts, checks it against the gate (UTF-8 text, 1 to 200
characters, not only white space, exactly one sentence), writes it out,
and reports what it wrote.
"""

import os
import sys

# The apology, built from its parts so the turn of the joke stays visible:
# the failure (answering before reading) and the self-own that follows it
# (doubling down with the confidence of someone never wrong).
APOLOGY_PARTS = (
    "I'm sorry I answered your question ",
    "before I'd finished reading it, ",
    "then doubled down with the serene confidence ",
    "of someone who has never once been wrong.",
)

MAX_CHARS = 200

# Sentence terminators that would split the text into more than one
# sentence. The final period is the sentence's own ending; any other
# terminator anywhere in the text means the text is not one sentence.
TERMINATORS = ".!?"


def build_apology() -> str:
    """Join the parts into the one sentence this entry submits."""
    return "".join(APOLOGY_PARTS)


def is_one_sentence(text: str) -> bool:
    """True when the text is exactly one sentence.

    One sentence means: it does not end in white space, it ends with a
    single sentence terminator, and no terminator appears anywhere before
    that final character. A run-on or a second sentence fails this check.
    """
    if not text or text[-1] not in TERMINATORS:
        return False
    if text != text.rstrip():
        return False
    return not any(ch in TERMINATORS for ch in text[:-1])


def validate(text: str) -> None:
    """Fail loudly when the text would fail the competition's gate."""
    if not text or not text.strip():
        raise ValueError("apology is empty or only white space")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "apology is %d characters, over the %d-character gate"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("apology must be a single line, no line breaks")
    if not is_one_sentence(text):
        raise ValueError("apology must be exactly one sentence")


def output_path() -> str:
    """Where the entry text goes: the sandbox mounts /output for us."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def verify_written(path: str, expected: str) -> None:
    """Read the file back and confirm it holds exactly what we wrote.

    A write that silently truncates or mangles the text would still leave
    a file behind, so the program re-reads it and compares byte for byte
    against the validated sentence before reporting success.
    """
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != expected.encode("utf-8"):
        raise ValueError(
            "read-back mismatch: %s holds %d bytes, expected %d bytes "
            "of the validated apology" % (path, len(on_disk), len(expected))
        )


def main() -> int:
    text = build_apology()
    validate(text)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    verify_written(path, text)
    print(text)
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
