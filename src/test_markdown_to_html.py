import unittest

from functions import *


class TestTextNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_link(self):
        md = "Visit [OpenAI](https://openai.com) now."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Visit <a href=\"https://openai.com\">OpenAI</a> now.</p></div>"
        )

    def test_headers(self):
        md = "# Title\n\n## Subtitle\n\n### Smaller"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><h2>Subtitle</h2><h3>Smaller</h3></div>"
        )

    def test_image(self):
        md = "Here is an image: ![alt text](https://example.com/img.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Here is an image: <img src=\"https://example.com/img.png\" alt=\"alt text\"></img></p></div>"
        )

    def test_unordered_list(self):
        md = "- Item one\n- Item two\n- Item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>"
        )

    def test_blockquote(self):
        md = "> This is a quote\n> And another line"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nAnd another line</blockquote></div>"
        )

    # def test_mixed_inline(self): - Not currently supported
    #     md = "Text with **bold and _italic_ inside**."
    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><p>Text with <b>bold and <i>italic</i> inside</b>.</p></div>"
    #     )