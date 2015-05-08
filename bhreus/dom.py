"""
    The Bhreus DOM module.
    Contains data structures for modeling DOM objects.
"""

DEFAULT_TEXT_VALUE = "The cake is both a group and a smooth manifold!"


class Node(object):
    """
    Superclass for all DOM nodes. Handles nodetypes, child types and children.
    Also provides basic prettyprinting.
    """
    def __init__(self, node_type="text", ctypes=[], children=[]):
        self.node_type = node_type
        self.children = []
        self.ctypes = ctypes  # valid types of children
        for child in children:
            self.add_child(child)

    # Add a child node to this node
    def add_child(self, n):
        # Only add a child node if it's the right nodetype
        if n.node_type in self.ctypes:
            self.children.append(n)
            return True
        return False

    def get_children(self):
        return self.children

    def pp(self, prefix=" "):
        """
        Basic prettyprinting of a DOM tree.def
        """
        print prefix+str(self)
        [child.pp(prefix + "  ") for child in self.get_children()]
        if isinstance(self, ElementNode):
            print prefix+self.close()

##############
# Node types #
##############


class TextNode(Node):

    def __init__(self, text=DEFAULT_TEXT_VALUE, children=[]):
        Node.__init__(self, "text", [], children)
        self.text = text

    def __str__(self):
        return self.text


class ElementNode(Node):

    def __init__(self, element_data, children=[]):
        self.element_data = element_data
        Node.__init__(self, "element", ["text", "element"], children)

    def __str__(self):
        s = "<"+str(self.element_data.tag_name)
        for attribute, value in self.element_data.attributes.items():
            s = "".join(s, " ", attribute, "=\"", value, "\"")
        return s+">"

    def close(self):
        return "</"+self.element_data.tag_name+">"


# Element Data
class ElementData(object):
    tag_name = ""
    attributes = {}

    def __init__(self, tag_name='p', attributes={}):
        self.tag_name = tag_name
        self.attributes = attributes

if __name__ == "__main__":
    main()
