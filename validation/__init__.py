from .message import Message

class Validation(object):
    def __init__(self, article, checkers):
        self.article = article
        self.wikitext = article.wikitext
        self._messages = None
        self.checkers = checkers

    def execute(self):
        self._messages = []

        wikitext = self.wikitext
        for checker in self.checkers:
            new_messages = checker(wikitext, self)
            if new_messages is not None:
                self._messages.extend(new_messages)

    def add_error(self, text, start, end=None):
        message = Message(self.wikitext, Message.ERROR, text, start, end)
        self._messages.append(message)

    def add_warning(self, text, start, end=None):
        message = Message(self.wikitext, Message.WARNING, text, start, end)
        self._messages.append(message)

    @property
    def messages(self):
        if self._messages is None:
            self.execute()
        return self._messages