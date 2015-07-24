import copy
import urlparse
import requests


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
    def __init__(self, url):
        if not isinstance(url,Url):
            url = Url(url)
        self.url = url
        self._wikitext = None

    @property
    def wikitext(self):
        if self._wikitext is None:
            r = requests.get(self.url.wikitext_url)
            self._wikitext = r.content.decode('utf-8')
        return self._wikitext
