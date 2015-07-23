import re


def double_http(wikitext, validation):
    RE = re.compile(r'https?:/?/?https?://', re.I)

    m = RE.search(wikitext)
    while m:
        validation.add_error('Double http:// in URL', m.pos, m.endpos)
        m = RE.search(wikitext, m.pos + 1)

ALL_CHECKERS = [
    double_http
]
