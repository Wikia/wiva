# coding=utf-8
import copy
import logging
import urllib
import urlparse
import sys

import requests
import requests.adapters

logger = logging.getLogger(__name__)


def str2hex(s):
    return " ".join("0x{:02x}".format(ord(c)) for c in s)


class Url(object):
    def __init__(self, url):
        parsed_url = urlparse.urlparse(url)
        page = parsed_url.path
        self.has_wiki_prefix = page.startswith('/wiki/')
        if self.has_wiki_prefix:
            page = page[5:]
        page = page.lstrip('/')

        self.url = url
        self.domain = parsed_url.hostname
        self.host = parsed_url.scheme + "://" + parsed_url.hostname
        self.path = parsed_url.path
        self.page = page

    def set_page(self, page):
        self.page = page
        path = '/'
        if self.has_wiki_prefix:
            path += 'wiki/'
        path += page
        self.path = path
        self.url = self.host + self.path

    @property
    def wikitext_url(self):
        return "{url}?action=raw".format(url=self.url)

    def new_page(self, new_page_name):
        new_url = copy.copy(self)
        new_url.set_page(new_page_name)
        return new_url


class Article(object):
    def __init__(self, url, session=None):
        if not isinstance(url, Url):
            url = Url(url)
        self.url = url
        self._wikitext = None

        if not session:
            self.session = requests.Session()
            self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))
        else:
            self.session = session

    @property
    def wikitext(self):
        if self._wikitext is None:
            r = self.session.get(self.url.wikitext_url)
            r.raise_for_status()
            self._wikitext = r.content.decode('utf-8')
        return self._wikitext


class Wiki(object):
    def __init__(self, url):
        if not isinstance(url, Url):
            url = Url(url)
        self.url = url
        self.session = requests.Session()
        self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))

    def next_page_url(self, base_query_url, response):
        try:
            if 'query-continue' in response:
                apfrom = response['query-continue']['allpages']['apfrom']
                apfrom = self.__fix_encoding(apfrom)
                apfrom = urllib.unquote(apfrom)
                return base_query_url + '&' + urllib.urlencode({'apfrom': apfrom})
            else:
                return None
        except UnicodeError:
            return None

    def iterarticles(self, start=None):
        base_query_url = self.url.host + '/api.php?action=query&list=allpages&format=json&aplimit=100'
        query_url = base_query_url
        if start is not None:
            query_url += '&' + urllib.urlencode({'apfrom': start})

        while query_url:
            # print >> sys.stderr, query_url
            try:
                response = self.session.get(query_url)
            except requests.exceptions.RequestException:
                break

            response = response.json()
            if 'query' not in response:
                print >> sys.stderr, response
                break
            for page_data in response['query']['allpages']:
                try:
                    page_url = self.url.new_page(self.__fix_encoding(page_data['title']))
                except UnicodeEncodeError:
                    logger.error('Invalid title skipped')
                    continue
                yield Article(page_url, session=self.session)

            query_url = self.next_page_url(base_query_url, response)

    def __fix_encoding(self, s):
        s = s.replace('?', '%3F')
        s = s.encode('iso-8859-1')
        s = self.__fix_broken_url_encodes(s)
        s = unicode(s, encoding='iso-8859-1')
        s = s.encode()
        return s

    @staticmethod
    def __fix_broken_url_encodes(s):
        def is_hex_char(z):
            z = z.lower()
            return '0' <= z <= '9' or 'a' <= z <= 'f'

        c = list(s)
        l = len(c)
        for i in range(l):
            if c[i] == '%':
                h = c[i + 1:i + 3]
                if len(h) < 2 or not is_hex_char(h[0]) or not is_hex_char(h[1]):
                    c[i] = '%25'
        return ''.join(c)
