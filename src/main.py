from htmlnode import HTMLNode
from textnode import TextNode, TextType

print("Hello world!")


def main():
    test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    node = TextNode("a", TextType.TEXT)
    print(test)
    print(node)

    test_prop = {
        "href": "https://www.google.com",
        "target": "_blank",
    }
    htmlnode = HTMLNode("a", "hello world", None, test_prop)
    # repr(htmlnode)
    htmlnode.props_to_html()


main()
