import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        htmlnode = HTMLNode("a", "hello world")
        htmlnode2 = HTMLNode("a", "hello world")
        self.assertEqual(htmlnode, htmlnode2)

    def test_htmlnode2(self):
        htmlnode = HTMLNode("a", "hello world", None, "")
        htmlnode2 = HTMLNode("b", "hello", None, {"href": "cloud"})
        self.assertNotEqual(htmlnode, htmlnode2)

    def test_propstohtml(self):
        test_prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        htmlnode = HTMLNode("a", "hello world", None, test_prop)
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', htmlnode.props_to_html()
        )

    def test_propstohtml2(self):
        test_prop = {"href": "none", "target": "url", "key": "value"}
        htmlnode = HTMLNode("h1", "hello prop", None, test_prop)
        self.assertEqual(
            ' href="none" target="url" key="value"', htmlnode.props_to_html()
        )


if __name__ == "__main__":
    unittest.main()
