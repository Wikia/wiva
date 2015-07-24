import re
from parens.parser import parse

MAX_ACCEPTABLE_WIDTH = 500  # todo: what the value really is?


def double_http(wikitext, validation):
    RE = re.compile(r'https?:/?/?https?://', re.I)

    for m in RE.finditer(wikitext):
        validation.add_error('Double http:// in URL', m.start(), m.end())


def local_articles_as_external_links(wikitext, validation):
    host = validation.article.url.host + '/'
    host_len = len(host)

    p = wikitext.find(host)
    while p != -1:
        validation.add_warning('Local URLs written as external links', p, p + host_len)
        p = wikitext.find(host, p + 1)


def unclosed_references_tag(wikitext, validation):
    T_OPEN = r'<references>'
    T_OPEN_len = len(T_OPEN)
    T_CLOSE = r'</references>'

    p = wikitext.find(T_OPEN)
    while p != -1:
        p2 = p + T_OPEN_len
        s = wikitext[p2:p2 + 500].strip()
        if not s.startswith(T_CLOSE):
            validation.add_error('Unclosed <references> tag', p, p + T_OPEN_len)
        p = wikitext.find(T_OPEN, p2)


def external_links_in_double_brackets(wikitext, validation):
    RE = re.compile(r'\[\[https?://', re.I)

    for m in RE.finditer(wikitext):
        validation.add_warning('External link in double brackets', m.start(), m.end())


def image_width_breaks_layout(wikitext, validation):
    RE = re.compile(r'\|(([0-9]+)px)[]|]')
    for m in RE.finditer(wikitext):
        width = int(m.group(2))
        if width > MAX_ACCEPTABLE_WIDTH:
            validation.add_error('Image width wider than minimum tablet/desktop content width', m.start(1), m.end(1))


def table_width_breaks_layout(wikitext, validation):
    RE_STYLE_WIDTH = re.compile(r'\{\|[^\r\n]*style="[^"]*width:\s*([0-9]+)px[^"]*"', re.I)
    RE_WIDTH = re.compile(r'\{\|[^\r\n]+width="?([0-9]+)px"?', re.I)

    for m in RE_STYLE_WIDTH.finditer(wikitext):
        width = int(m.group(1))
        if width > MAX_ACCEPTABLE_WIDTH:
            validation.add_error('Table width wider than minimum tablet/desktop content width', m.start(1), m.end(1))

    for m in RE_WIDTH.finditer(wikitext):
        width = int(m.group(1))
        if width > MAX_ACCEPTABLE_WIDTH:
            validation.add_error('Table width wider than minimum tablet/desktop content width', m.start(1), m.end(1))


def broken_headers(wikitext, validation):
    RE = re.compile(r'(?:^|\n)(=+).*?[^=](=+)\s*(?=$|\r|\n)')
    for m in RE.finditer(wikitext):
        left_len = len(m.group(1))
        right_len = len(m.group(2))
        if left_len > 6:
            validation.add_error('Header level is invalid: {}'.format(left_len), m.start(1), m.end(1))
        if right_len > 6:
            validation.add_error('Header level is invalid: {}'.format(right_len), m.start(2), m.end(2))
        if left_len != right_len:
            validation.add_error('Header levels do not match', m.start(1), m.end(2))


def misclosed_gallery(wikitext, validation):
    pattern = '<gallery/>'
    p = wikitext.find(pattern)
    while p != -1:
        p2 = p + len(pattern)
        validation.add_error('Mistyped </gallery>', p, p + len(pattern))
        p = wikitext.find(pattern, p2)


def bad_tag(wikitext, validation):
    bad_tags = {"<b[^ri]*?>": "'''text'''",
                "<i[^m]*?>": "''text''",
                "<table.*?>": "{| table content |}",
                "<h1.*?>": "= heading =",
                "<h2.*?>": "== heading ==",
                "<h3.*?>": "=== heading ===",
                "<h4.*?>": "==== heading ====",
                "<h5.*?>": "===== heading =====",
                "<h6.*?>": "====== heading ======"
                }

    for pattern in bad_tags:
        replacement = bad_tags[pattern]
        RE = re.compile(pattern)
        for m in RE.finditer(wikitext):
            printable_pattern = pattern.replace(".*?", "")
            validation.add_warning('Don\'t use an html tag %s, use wikitext replacement %s instead' % (printable_pattern, replacement), m.start(), m.end())


def parens(wikitext, validation):
    parse(wikitext, validation)


ALL_CHECKERS = [
    double_http,
    local_articles_as_external_links,
    unclosed_references_tag,
    external_links_in_double_brackets,
    image_width_breaks_layout,
    table_width_breaks_layout,
    broken_headers,
    parens,
    misclosed_gallery,
    bad_tag
]
