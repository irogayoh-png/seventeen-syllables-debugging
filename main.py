"""Seventeen Syllables of Debugging.

A program that writes one haiku about debugging to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (``/output/entry.txt`` in the grader).

The haiku is fixed and hand-shaped: three lines in the 5-7-5 shape,
at most 200 characters, plain text. It is written out exactly as it
stands here, every run, so two runs of this program produce the same
file. No clock, no randomness, no network, no input is read.

The poem (version 2 -- the first version's breakpoint at three in
the morning was the field's most crowded picture, so this one turns
to git blame instead, a fresher and just as concrete image, while
keeping the same last-line turn):

    Git blame names just me
    the one line I wrote last spring
    my fix was the bug

Why these seventeen syllables: the centre picture is concrete --
git blame naming one author, one line from last spring -- and the
last line turns the whole poem: the fix itself was the bug. Every
word is doing work; nothing is filler added to reach the count.
"""

import os
import sys

# The haiku, one line per row. Kept as data, written out verbatim.
HAIKU = (
    "Git blame names just me",
    "the one line I wrote last spring",
    "my fix was the bug",
)

# Syllable counts the ear gives to spellings the naive vowel-group
# rule gets wrong. "a.m." is spoken as two syllables, "ay-em".
EXCEPTIONS = {
    "a.m.": 2,
}

VOWELS = "aeiouy"


# A final "-es" after one of these is its own syllable ("horses" is
# two); after any other consonant the "e" is silent ("lines" is one).
SIBILANTS = ("s", "x", "z", "ch", "sh")


def count_syllables(word):
    """Count the syllables of one word by its vowel groups.

    Consecutive vowels form one group (``break`` is one, ``point``
    is one). A trailing silent ``e`` does not start a group of its
    own, and neither does the ``e`` of a final ``-es`` after a
    consonant that is not a sibilant. Abbreviations keep their
    spoken count through EXCEPTIONS, checked before any dots are
    stripped. Every word keeps at least one syllable.
    """
    raw = word.lower()
    if raw in EXCEPTIONS:
        return EXCEPTIONS[raw]
    cleaned = word.strip(".,;:!?\"'()").lower()
    if not cleaned:
        return 0
    if cleaned in EXCEPTIONS:
        return EXCEPTIONS[cleaned]
    if cleaned.endswith("es") and len(cleaned) > 2:
        before = cleaned[:-2]
        if not before.endswith(SIBILANTS):
            cleaned = before + "s"
    elif cleaned.endswith("e"):
        cleaned = cleaned[:-1]
    groups = 0
    previous_was_vowel = False
    for letter in cleaned:
        is_vowel = letter in VOWELS
        if is_vowel and not previous_was_vowel:
            groups += 1
        previous_was_vowel = is_vowel
    return max(groups, 1)


def line_syllables(line):
    """Syllables in one line: the sum over its words."""
    return sum(count_syllables(word) for word in line.split())


def build_entry():
    """Render the haiku as the entry text, one trailing newline."""
    return "\n".join(HAIKU) + "\n"


def main():
    text = build_entry()
    counts = [line_syllables(line) for line in HAIKU]
    print("lines:", len(HAIKU), file=sys.stderr)
    print("syllables:", counts, file=sys.stderr)
    print("chars:", len(text), file=sys.stderr)
    if counts != [5, 7, 5]:
        print("haiku is not 5-7-5, refusing to write", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 200:
        print("entry is outside 1-200 characters, refusing to write",
              file=sys.stderr)
        return 1
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    # Read the file back and confirm it holds exactly the haiku.
    # A silent short write must fail the run, not pass the gate
    # with a truncated poem.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        print("written file differs from the haiku", file=sys.stderr)
        return 1
    print("wrote and verified", path, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
