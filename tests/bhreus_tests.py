from nose.tools import *
import bhreus.parse
import bhreus.dom


def test_consume():
    test_html = "Hello"
    p = bhreus.parse.Parser(test_html)
    for i in xrange(len(test_html)):
        assert p.consume_char() == test_html[i]


def test_consume_whiles():
    test_html = "     Hello     "

    p = bhreus.parse.Parser(test_html)
    assert p.consume_alphanum() == ""
    assert p.consume_whitespace() == "     "
    assert p.consume_whitespace() == ""
    assert p.consume_alphanum() == "Hello"
    assert p.consume_alphanum() == ""
    assert p.consume_whitespace() == "     "
    assert p.consume_whitespace() == ""
    assert p.consume_alphanum() == ""


def test_parse():
    """
    Test the full parse functionality on a simple DOM tree.
    """

    test_html = (
        "<html><body>"
        "<p id='first-line'>Thunderbolts and lightning!</p>"
        "<p id='second-line'>Very very frightening!</p>"
        "</body></html>"
        )
    p = bhreus.parse.Parser(test_html)

    root_node = p.parse()
    assert root_node.node_type == "element"
    assert root_node.element_data.tag_name == "html"
    assert root_node.element_data.attributes == {}
    assert len(root_node.get_children()) == 1

    body_node = root_node.get_children()[0]
    assert body_node.node_type == "element"
    assert body_node.element_data.tag_name == "body"
    assert body_node.element_data.attributes == {}
    assert len(body_node.get_children()) == 2

    p1_node = body_node.get_children()[0]
    assert p1_node.node_type == "element"
    assert p1_node.element_data.tag_name == "p"
    assert p1_node.element_data.attributes == {"id": "first-line"}
    assert len(p1_node.get_children()) == 1

    t1_node = p1_node.get_children()[0]
    assert t1_node.node_type == "text"
    assert t1_node.text == "Thunderbolts and lightning!"
    assert len(t1_node.get_children()) == 0

    p2_node = body_node.get_children()[1]
    assert p2_node.node_type == "element"
    assert p2_node.element_data.tag_name == "p"
    assert p2_node.element_data.attributes == {"id": "second-line"}
    assert len(p2_node.get_children()) == 1

    t2_node = p2_node.get_children()[0]
    assert t2_node.node_type == "text"
    assert t2_node.text == "Very very frightening!"
    assert len(t2_node.get_children()) == 0
