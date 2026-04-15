import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
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

    def test_to_html_with_greatgrandchildren(self):
        great_grandchild = LeafNode(tag="b", value="great-grandchild")
        grandchild_node = LeafNode("b", "grandchild")
        grandparent_node = ParentNode(
            tag="div", children=[grandchild_node, great_grandchild]
        )
        child_node = ParentNode("span", [grandparent_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><div><b>grandchild</b><b>great-grandchild</b></div></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
