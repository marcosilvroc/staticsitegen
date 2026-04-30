import unittest

from gencontent import extract_title


class Test_GenContent(unittest.TestCase):
    def test_md_title(self):
        md = "# Hello World"
        title = extract_title(md)
        self.assertEqual(title, "Hello World")

    def test_md_title2(self):
        md = "# #Hello World#"
        title = extract_title(md)
        self.assertEqual(title, "#Hello World#")

    def test_md_title3(self):
        md = """
this is lines
of text

# with a title in middle of it

- and
- list
"""
        title = extract_title(md)
        self.assertEqual(title, "with a title in middle of it")

    def test_no_title(self):
        with self.assertRaises(Exception) as e:
            md = "### Hello World"
            extract_title(md)
        self.assertEqual(str(e.exception), "H1 header not found.")
