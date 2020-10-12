import re

import docutils.frontend
import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import polib
from spellchecker import SpellChecker


def is_sphinx_role(s):
    return re.match(r"^:\w+:", s)


def is_rst_format(s):
    for f in rst_format:
        if s.startswith(f) or s.endswith(f):
            return True
    return False


def is_rst_ref(s):
    if s.startswith("[") and s.endswith("]_"):
        return True
    else:
        return False


def is_number(s):
    try:
        _ = float(s)
        return True
    except ValueError:
        return False


def valid_word(s):
    if is_sphinx_role(s) or is_rst_format(s) or is_rst_ref(s) or is_number(s):
        return False
    return True


def clean_word(s):
    punctuation = (".", ";", ",", '"', "(", ")", ":")
    for p in punctuation:
        if s.endswith(p):
            s = s[:-1]
        if s.startswith(p):
            s = s[1:]
    return s


def parse_rst(text: str) -> docutils.nodes.document:
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components=components).get_default_values()
    settings.report_level = 4
    document = docutils.utils.new_document("<rst-doc>", settings=settings)
    parser.parse(text, document)
    return document


def clean_rst_parsed(s):
    doc = parse_rst(s)
    # Remove content
    doc = re.sub(r"<emphasis>.*?</emphasis>", "", str(doc))
    doc = re.sub(r"<problematic .*?>.*?</problematic>", "", str(doc))
    doc = re.sub(r"<literal>.*?</literal>", "", str(doc))
    doc = re.sub(r"<footnote_reference .*?>.*?</footnote_reference>", "", str(doc))

    # Extract content, and get the first element since the others are problems
    return re.findall("<paragraph>(.*?)</paragraph>", doc)[0]


def check_spell(po):
    for entry in po:
        doc = clean_rst_parsed(entry.msgstr)
        words = doc.split(" ")
        for s in words:
            if not valid_word(s):
                continue
            s = clean_word(s)
            if s:
                if not spell[s]:
                    print(f"{filename}:{entry.linenum}:{s}")


if __name__ == "__main__":
    rst_format = ("``", "*")
    spell = SpellChecker(language="es", case_sensitive=True)
    spell.word_frequency.load_text_file("dict.txt")

    # Wrap file
    filename = "bytes.po"
    po = polib.pofile(filename, wrap_width=79, break_long_words=True, replace_whitespace=False)
    po.save()

    check_spell(po)
