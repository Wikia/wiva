import termcolor


class Message(object):
    MAX_LINE_LENGTH = 50

    ERROR = 'ERROR'
    WARNING = 'WARNING'

    COLORS = {
        ERROR: ('red', None, 'bold'),
        WARNING: ('yellow', None, 'bold')
    }

    def __init__(self, source_text, severity, text, start, end=None):
        self.source_text = source_text
        self.severity = severity
        self.text = text
        self.start = start
        self.end = end

    def __str__(self):
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
            line_end = length
        elif source_text[line_end - 1] == "\r":
            line_end -= 1

        before, mark, after = self.__each_expand_tabs(
            source_text[line_start:start],
            source_text[start:end],
            source_text[end:line_end])

        text_msg = "{}: {}".format(self.severity, self.text)
        if self.severity in self.COLORS:
            text_msg = termcolor.colored(text_msg, self.COLORS[self.severity])
        text_msg += "\n"
        text_msg += "  {}{}{}\n".format(before, mark, after)
        text_msg += "  {}{}\n".format(' ' * len(before), '^' * len(mark))

        return text_msg

    def __each_expand_tabs(self, *args):
        return map(self.__expand_tabs, args)

    def __expand_tabs(self, s):
        return s.replace("\t", "  ")
