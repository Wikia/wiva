import termcolor


class Message(object):
    MAX_LINE_LENGTH = 50

    ERROR = 'ERROR'
    WARNING = 'WARNING'

    COLORS = {
        ERROR: ('red', None, ('bold',)),
        WARNING: ('yellow', None, ('bold',))
    }

    def __init__(self, source_text, severity, text, start, end=None):
        self.source_text = source_text
        self.severity = severity
        self.text = text
        self.start = start
        self.end = end

    def __emphasize(self, text):
        if not self.severity in self.COLORS:
            return text
        return termcolor.colored(text, *self.COLORS[self.severity])


    def __unicode__(self):
        source_text = self.source_text
        length = len(source_text)
        start = self.start
        end = self.end if self.end is not None else self.start + 1

        line_start = source_text.rfind("\n", max(start - self.MAX_LINE_LENGTH, 0), start)
        if line_start == -1:
            line_start = max(start - self.MAX_LINE_LENGTH, 0)
        else:
            line_start += 1
        line_end = source_text.find("\n", end, min(end + self.MAX_LINE_LENGTH, length))
        if line_end == -1:
            line_end = min(end + self.MAX_LINE_LENGTH, length)
        elif source_text[line_end - 1] == "\r":
            line_end -= 1

        before, mark, after = self.__each_expand_tabs(
            source_text[line_start:start],
            source_text[start:end],
            source_text[end:line_end])

        text = ''.join([
            self.__emphasize(u"{}: {}".format(self.severity, self.text)),
            u"\n",
            u"  {}{}{}".format(before, mark, after),
            u"\n",
            u"  {}{}".format(' ' * len(before), self.__emphasize('^' * len(mark))),
            u"\n",
        ])

        return text

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __each_expand_tabs(self, *args):
        return map(self.__expand_tabs, args)

    def __expand_tabs(self, s):
        return s.replace("\t", "  ")
