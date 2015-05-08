"""
    The Bhreus HTML parser module. Presently only can handle a
    minimal subset of html syntax; will fail loudly otherwise.
"""

import string
from bhreus import dom


class Parser(object):
    """
    Parser object.
    """
    whitespace = string.whitespace
    alphanum = string.letters+string.digits

    def __init__(self, html=""):
        self.set_html(html)

    def set_html(self, html):
        self.pos = 0
        # Filter characters to ascii
        self.html = "".join(filter(lambda c: c in string.printable, html))

    ###################
    # PARSING METHODS #
    ###################

    # Parse the entire source file
    def parse(self):
        nodes = self.parse_nodes()
        # If there's a root node, return that.
        if len(nodes) == 1:
            return nodes[0]
        # Otherwise, make one.
        return dom.ElementNode(
            ElementData("html", {}),
            nodes)

    # Parse one node
    def parse_node(self):
        if self.next_char() == "<":
            return self.parse_element()
        return self.parse_text()

    # Parse a text node
    def parse_text(self):
        return dom.TextNode(self.consume_while(lambda c: c != "<"))

    # Parse an element node
    def parse_element(self):
        element = ""
        # Element tag
        assert self.consume_char() == "<"
        tag_name = self.consume_alphanum()
        attributes = self.parse_attributes()
        assert self.consume_char() == ">"

        # Element content
        children = self.parse_nodes()

        # Element closing tag
        assert self.consume_char() == "<"
        assert self.consume_char() == "/"
        closing_tag_name = self.consume_alphanum()
        assert closing_tag_name == tag_name
        assert self.consume_char() == ">"
        return dom.ElementNode(dom.ElementData(tag_name, attributes), children)

    # Parse a tag attribute
    def parse_attribute(self):
        name = self.consume_alphanum()
        assert self.consume_char() == "="
        value = self.parse_attribute_value()
        return (name, value)

    # Parse an attribute value
    def parse_attribute_value(self):
        openquote = self.consume_char()
        assert openquote in ("'", "\"")
        value = self.consume_while(lambda c: c != openquote)
        assert self.consume_char() == openquote
        return value

    # Parse all attributes of a tag
    def parse_attributes(self):
        attributes = {}
        while True:
            self.consume_whitespace()
            if self.next_char() != ">":
                name, value = self.parse_attribute()
                attributes[name] = value
            else:
                break
        return attributes

    # Parse all child nodes
    def parse_nodes(self):
        nodes = []
        while True:
            self.consume_whitespace()
            if self.eof() or self.startswith("</"):
                break
            nodes.append(self.parse_node())
        return nodes

    #####################
    # CHARACTER METHODS #
    #####################

    # Return next character without consuming
    def next_char(self):
        return self.html[self.pos]

    # Consume and return one character
    def consume_char(self):
        cur_char = self.html[self.pos]
        self.pos += 1
        return cur_char

    # Consume characters as long as they pass test.
    def consume_while(self, test=lambda x: False):
        result = ""
        while not self.eof() and test(self.next_char()):
            result += self.consume_char()
        return result

    # Consume characters as long as they're whitespace
    def consume_whitespace(self):
        return self.consume_while(lambda a: a in self.whitespace)

    # Consume characters as long as they're alphanumeric
    def consume_alphanum(self):
        return self.consume_while(lambda a: a in self.alphanum)

    ########################
    # STATUS CHECK METHODS #
    ########################

    # Check if the remaining html starts with a given string
    def startswith(self, s):
        return self.html[self.pos:].startswith(s)

    # Check if we're at the end of the file
    def eof(self):
        return not self.pos < len(self.html)


def main():
    """
    Example.
    """
    example_html = (
        "<html><body>"
        "<p id='first-line'>Thunderbolts and lightning</p>"
        "<p id='second-line'>Very very frightening</p>"
        "</body></html>"
        )
    example_parser = Parser(example_html)
    example_dom = example_parser.parse()
    example_dom.pp()

if __name__ == "__main__":
    main()
