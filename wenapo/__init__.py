#!/usr/bin/env python
import argparse
import os
import re
import sys

import docutils.frontend
import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import polib
from spellchecker import SpellChecker


def is_number(s: str) -> bool:
    try:
        _ = float(s)
        return True
    except ValueError:
        return False


def valid_word(s: str) -> bool:
    if is_number(s):
        return False
    return True


def clean_word(s: str) -> str:
    punctuation = (".", ";", ",", '"', "(", ")", ":", "%", "*")
    for p in punctuation:
        if s.endswith(p):
            s = s[:-1]
        if s.startswith(p):
            s = s[1:]
    # Remove null character
    s = s.replace("\x00", "")
    return s


def parse_rst(text: str) -> docutils.nodes.document:
    """Get a tag-based string from the input string, allowing to
    easily remove the tags we don't need"""
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    settings.report_level = 4
    document = docutils.utils.new_document("<rst-doc>", settings=settings)
    parser.parse(text, document)
    return document

def clean_rst_parsed(s: str) -> str:
    doc = parse_rst(s)
    # Remove content
    doc = re.sub(r"<emphasis>.*?</emphasis>", "", str(doc))
    doc = re.sub(r"<problematic .*?>.*?</problematic>", "", str(doc))
    doc = re.sub(r"<literal>.*?</literal>", "", str(doc))
    doc = re.sub(r"<footnote_reference .*?>.*?</footnote_reference>", "", str(doc))

    # Extract content, and get the first element since the others are problems
    return re.findall("<paragraph>(.*?)</paragraph>", doc)[0]


def check_spell(spell, po, filename, suggestion=False):
    for entry in po:
        doc = clean_rst_parsed(entry.msgstr)
        words = doc.split(" ")
        for s in words:
            if not valid_word(s):
                continue
            s = clean_word(s)
            if s:
                if not spell[s]:
                    if suggestion:
                        correction = spell.correction(s)
                        print(repr(correction), repr(s))
                        if correction == s:
                            print(f"{filename}:{entry.linenum}:{s} -> ???")
                        else:
                            print(f"{filename}:{entry.linenum}:{s} -> {correction}")
                    else:
                        print(f"{filename}:{entry.linenum}:{s}")


def check_options(o):
    print(o)
    if not os.path.isfile(o.dictionary):
        print(f"Dictionary file '{o.dictionary}' does not exist")
        return False
    for f in o.po_file:
        if not os.path.isfile(f):
            print(f"po file '{f}' does not exist")
            return False
    return True

def main():
    parser = argparse.ArgumentParser(prog="wenapo", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-p",
        "--personal-dict",
        action="store",
        dest="dictionary",
        help="Load a personal dictionary",
        default="dict.txt",
    )
    parser.add_argument(
        "-l",
        "--language",
        action="store",
        dest="language",
        help="Base language to use",
        default="es",
    )
    parser.add_argument(
        "-s", "--suggestion", action="store_true", help="Suggest the closest word (slow)"
    )
    parser.add_argument("po_file", nargs="+")
    options = parser.parse_args()
    if not check_options(options):
        sys.exit(-1)

    spell = SpellChecker(language=options.language, case_sensitive=True)
    spell.word_frequency.load_text_file(options.dictionary)

    # Wrap file
    for filename in options.po_file:
        # Open the file with a certain 'wrap_width' will wrap the file
        po = polib.pofile(filename, wrap_width=79, break_long_words=True, replace_whitespace=False)
        po.save()

        # Check Spelling
        check_spell(spell, po, filename, suggestion=options.suggestion)


if __name__ == "__main__":
    main()
