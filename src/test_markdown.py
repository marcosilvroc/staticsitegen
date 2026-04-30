import unittest

from markdown import (
    BlockType,
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestFunctions(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word.", TextType.TEXT),
            ],
        )

    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold block word**.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block word", TextType.BOLD),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_italic_delimiter(self):
        node = TextNode("This is text with a _italic block word_.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block word", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_bold_delimiters(self):
        node = TextNode(
            "This is a **bold word** and this is **another bold word**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode(" and this is ", TextType.TEXT),
                TextNode("another bold word", TextType.BOLD),
            ],
        )

    def test_two_delimiters(self):
        node = TextNode("This is an _italic_ and **bold** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word.", TextType.TEXT),
            ],
        )

    def test_nested_delimiters(self):
        node = TextNode("This is an _italic and **bold** word_.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertNotEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic and ", TextType.ITALIC),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_extract_img(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_img2(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            matches,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_link2(self):
        text = "This is text with a link [to some random site](https://www.random.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            matches,
            [
                ("to some random site", "https://www.random.com"),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.notzelda.com) and another [second link](https://www.link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.notzelda.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.link.com"),
            ],
            new_nodes,
        )

    def test_split_linkandimg(self):
        node = TextNode(
            "This is a ![silly cat image](https://example.com/cat.png) and this is a link for a [theater show](https://www.comedyshow.com/tickets)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode(
                    "silly cat image", TextType.IMAGE, "https://example.com/cat.png"
                ),
                TextNode(" and this is a link for a ", TextType.TEXT),
                TextNode(
                    "theater show", TextType.LINK, "https://www.comedyshow.com/tickets"
                ),
            ],
            new_nodes,
        )

    def test_split_image_with_empty_text(self):
        node = TextNode(
            "This is an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertNotEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_all_splits(self):
        new_nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_bold_italic_code_textnodes(self):
        new_nodes = text_to_textnodes(
            "This is **bold text** with a _spagetthi word_ and a `lego block`"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("spagetthi word", TextType.ITALIC),
                TextNode(" and a ", TextType.TEXT),
                TextNode("lego block", TextType.CODE),
            ],
            new_nodes,
        )

    def test_code_link_textnodes(self):
        new_nodes = text_to_textnodes(
            "This is a `code` followed by a ![image](https://image.com)"
        )
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" followed by a ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://image.com"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_block_type_heading(self):
        md = "###### This is a h6"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    def test_block_type_heading2(self):
        md = "### This is a h3"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    def test_block_type_heading3(self):
        md = "##This is not a h2"
        self.assertNotEqual(block_to_block_type(md), BlockType.HEADING)

    def test_block_type_code(self):
        md = """```
        This is a code block```"""
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_block_type_unordered_quote(self):
        md = ">Line 1\n> \n> Line 2"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_block_type_unordered_list(self):
        md = "- Line 1\n- Line 2\n- Line 3"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_block_type_ordered_list(self):
        md = "1. Line 1\n2. Line 2\n3. Line 3"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

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

    def test_headings(self):
        md = """
## h2 heading

#### h4 heading

A paragraph with **bolded words**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>h2 heading</h2><h4>h4 heading</h4><p>A paragraph with <b>bolded words</b></p></div>",
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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> Not all those who wander are lost. **J.R.R. Tolkien**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Not all those who wander are lost. <b>J.R.R. Tolkien</b></blockquote></div>",
        )

    def test_ordered_list_block(self):
        md = """
1. Line 1
2. Line 2
3. Line 3
4. Line 4
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Line 1</li><li>Line 2</li><li>Line 3</li><li>Line 4</li></ol></div>",
        )

    def test_unordered_list_block(self):
        md = """
A paragraph with words

- Line 1
- Line 2
- Line 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>A paragraph with words</p><ul><li>Line 1</li><li>Line 2</li><li>Line 3</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()
