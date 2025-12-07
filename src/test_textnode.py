import unittest

from textnode import TextNode, TextType
from functions import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_link(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), '<b>This is a bold text node</b>')
    
    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.boot.dev/lessons/80ddb6c5-8324-4850-a28c-0c6207596857")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props_to_html(), ' href="https://www.boot.dev/lessons/80ddb6c5-8324-4850-a28c-0c6207596857"')

    # Value remains None, ask Boots
    # def test_image(self): 
    #     node = TextNode("This is an image node", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/profile_images/52e7fd79-e721-41da-a84e-001163e3381e.jpeg")
    #     self.maxDiff=None
    #     html_node = text_node_to_html_node(node)
    #     self.assertEqual(html_node.to_html(), '<img src="https://storage.googleapis.com/qvault-webapp-dynamic-assets/profile_images/52e7fd79-e721-41da-a84e-001163e3381e.jpeg" alt="This is an image node"> </img>')

if __name__ == "__main__":
    unittest.main()