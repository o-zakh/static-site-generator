import unittest

from html_gen_functions import extract_title

class TestHtmlNode(unittest.TestCase):
    def test_extract_beginning_title(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
        """
        self.assertEqual(extract_title(md), 'Tolkien Fan Club')

    def test_extract_mid_title(self):
        md = """
![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

# Tolkien Fan Club

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
        """
        self.assertEqual(extract_title(md), 'Tolkien Fan Club')

    def test_extract_ending_title(self):
        md = """
![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
# Another Fan Club
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
# Tolkien Fan Club
        """
        self.assertEqual(extract_title(md), 'Another Fan Club')

if __name__ == "__main__":
    unittest.main()