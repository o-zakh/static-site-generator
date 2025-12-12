import unittest
from blocktype import *
from md_functions import block_to_block_type


class TestHtmlNode(unittest.TestCase):
    def test_heading_correct(self):
        expected = "heading"
        text = "# Heading"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_heading_wrong1(self):
        expected = "paragraph"
        text = "#Heading"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_heading_wrong2(self):
        expected = "paragraph"
        text = "####### Heading"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_heading_wrong3(self):
        expected = "paragraph"
        text = " # Heading"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_code_correct(self):
        expected = "code"
        text = "```code```"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_code_wrong1(self):
        expected = "paragraph"
        text = "```code"
        self.assertEqual(block_to_block_type(text).name, expected)
    
    def test_code_wrong2(self):
        expected = "paragraph"
        text = "code```"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_code_wrong3(self):
        expected = "paragraph"
        text = "``co``de``"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_quote_correct(self):
        expected = "quote"
        text = ">this it a quote block"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_quote_correct2(self):
        expected = "quote"
        text = ">this it a quote block\n>this is another quote line"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_quote_wrong1(self):
        expected = "paragraph"
        text = " >this is a quote"
        self.assertEqual(block_to_block_type(text).name, expected)
    
    def test_quote_wrong2(self):
        expected = "paragraph"
        text = """
>this it a quote block
this is another quote line
        """
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_quote_wrong3(self):
        expected = "paragraph"
        text = "this it a quote block\nthis is another quote line"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_unor_list_correct(self):
        expected = "unordered_list"
        text = "- this it a quote block"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_unor_list_correct2(self):
        expected = "unordered_list"
        text = "- this it a quote block\n- this is another quote line"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_unor_list_wrong1(self):
        expected = "paragraph"
        text = " -this is a quote"
        self.assertEqual(block_to_block_type(text).name, expected)
    
    def test_unor_list_wrong2(self):
        expected = "paragraph"
        text = """
- this it a quote block
this is another quote line
        """
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_unor_list_wrong3(self):
        expected = "paragraph"
        text = "-this it a quote block\nthis is another quote line"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_or_list_correct(self):
        expected = "ordered_list"
        text = "1. this it a quote block"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_or_list_correct2(self):
        expected = "ordered_list"
        text = "1. this it a quote block\n2. this is another quote line"
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_or_list_wrong1(self):
        expected = "paragraph"
        text = "1.this is a quote"
        self.assertEqual(block_to_block_type(text).name, expected)
    
    def test_or_list_wrong2(self):
        expected = "paragraph"
        text = """
1. >this it a quote block
3. this is another quote line
        """
        self.assertEqual(block_to_block_type(text).name, expected)

    def test_or_list_wrong3(self):
        expected = "paragraph"
        text = "2.this it a quote block\n3.this is another quote line"
        self.assertEqual(block_to_block_type(text).name, expected)


if __name__ == "__main__":
    unittest.main()