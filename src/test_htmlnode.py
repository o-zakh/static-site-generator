import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode

default_props = {
                "href": "https://www.google.com",
                "target": "_blank"
            }

default_child = HTMLNode(props=default_props)


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props=default_props)
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_empty_props_to_html(self):
        node = HTMLNode()
        expected = ''
        self.assertEqual(node.props_to_html(), expected)
    
    def test_full_values(self):
        node = HTMLNode(
            tag="a",
            value="value",
            children=HTMLNode(),
            props= default_props
        )
        expected_repr = "HTMLNode(a, value, HTMLNode(None, None, None, None), {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(repr(node), expected_repr)
    
    # def test_full_values_called_child(self):
    #     node = HTMLNode(
    #         tag="a",
    #         value="value",
    #         children=default_child,
    #         props= {
    #             "href": "https://www.smeshnaya_popa.com",
    #             "target": "_top",
    #         }
    #     )
    #     self.maxDiff = None
    #     expected_repr = "HTMLNode(a, 'value', HTMLNode(props={'href': 'https://www.google.com', 'target': '_blank'}), {'href': 'https://www.smeshnaya_popa.com', 'target': '_top'})"
    #     expected_props_to_html = " href='https://www.smeshnaya_popa.com' target='_top'"
    #     self.assertEqual(repr(node), expected_repr)
    #     self.assertEqual(node.props_to_html(), expected_props_to_html)

    def test_skipped_value(self):
        node = HTMLNode(
            tag="p",
            props= default_props
        )
        expected = "HTMLNode(p, None, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(repr(node), expected)

    def test_repr(self):
        node = HTMLNode(
            tag="a",
            value="link",
            children=None,
            props={"href": "https://example.com"},
        )
        expected = "HTMLNode(a, link, None, {'href': 'https://example.com'})"
        self.assertEqual(repr(node), expected)

    def test_exception(self):
        node = HTMLNode(
            props= default_props
        )

        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_notag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_p_nonevalue(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()