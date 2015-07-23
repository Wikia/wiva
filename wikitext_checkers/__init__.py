import re


def double_http(wikitext, validation):
    RE = re.compile(r'https?:/?/?https?://', re.I)

    for m in RE.finditer(wikitext):
        validation.add_error('Double http:// in URL', m.start(), m.end())


def local_articles_as_external_links(wikitext, validation):
    host = validation.article.url.host
    host_len = len(host)

    p = wikitext.find(host)
    while p != -1:
        validation.add_error('Local URLs written as external links', p, p + host_len)
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
        validation.add_error('External link in double brackets', m.start(), m.end())


def image_width_breaks_mobile(wikitext, validation):
    RE = re.compile(r'\|(([0-9]+)px)[]|]')
    for m in RE.finditer(wikitext):
        width = int(m.group(2))
        if width > 300:
            validation.add_error('Image width wider than minimum tablet/desktop content width', m.start(1), m.end(1))


ALL_CHECKERS = [
    double_http,
    local_articles_as_external_links,
    unclosed_references_tag,
    external_links_in_double_brackets,
    image_width_breaks_mobile
]
