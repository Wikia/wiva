# coding=utf-8
__author__ = 'alistra'


class Node(object):
    def __init__(self):
        self.line = None
        self.pos = None
    pass


class TextNode(Node):
    def __init__(self, text):
        super(TextNode, self).__init__()
        self.text = text


class SquareNode(Node):
    def __init__(self, inside_node=None):
        super(SquareNode, self).__init__()
        self.inside_node = inside_node


class CurlyNode(Node):
    def __init__(self, inside_node=None):
        super(CurlyNode, self).__init__()
        self.inside_node = inside_node


class ParenNode(Node):
    def __init__(self, inside_node=None):
        super(ParenNode, self).__init__()
        self.inside_node = inside_node

