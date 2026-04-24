import re
from enum import Enum

from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unlist"
    ORDERED_LIST = "ordlist"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            node_split = node.text.split(delimiter)
            node_range = len(node_split)
            if node_range % 2 == 0:  # found no end delimiter
                raise Exception("Invalid Markdown syntax, please check the text input.")
            else:
                temp_nodes = []
                for i in range(node_range):
                    if node_split[i] == "":
                        continue
                    if i % 2 == 0:
                        temp_nodes.append(TextNode(node_split[i], TextType.TEXT))
                    else:
                        temp_nodes.append(TextNode(node_split[i], text_type))
                new_nodes.extend(temp_nodes)
    return new_nodes


def extract_markdown_images(text):
    if not isinstance(text, str):
        raise TypeError("Input is not a raw text.")
    else:
        matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return matches


def extract_markdown_links(text):
    if not isinstance(text, str):
        raise TypeError("Input is not a raw text.")
    else:
        matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        else:
            matches = extract_markdown_images(node.text)
            if len(matches) == 0:  # node is text but no match was found
                new_nodes.append(node)

            else:
                match_nodes = []
                remaining_text = node.text
                for match in matches:
                    splits = remaining_text.split(f"![{match[0]}]({match[1]})", 1)
                    if splits[0] != "":
                        match_nodes.append(TextNode(splits[0], TextType.TEXT))
                    match_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
                    remaining_text = splits[1]
                if remaining_text != "":
                    match_nodes.append(TextNode(remaining_text, TextType.TEXT))
                new_nodes.extend(match_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        else:
            matches = extract_markdown_links(node.text)
            if len(matches) == 0:  # node is text but no match was found
                new_nodes.append(node)

            else:
                match_nodes = []
                remaining_text = node.text
                for match in matches:
                    splits = remaining_text.split(f"[{match[0]}]({match[1]})", 1)
                    if splits[0] != "":
                        match_nodes.append(TextNode(splits[0], TextType.TEXT))
                    match_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
                    remaining_text = splits[1]
                if remaining_text != "":
                    match_nodes.append(TextNode(remaining_text, TextType.TEXT))
                new_nodes.extend(match_nodes)
    return new_nodes


def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = []
    splited = markdown.split("\n\n")
    for b in splited:
        if b != "":
            b = b.strip()
            blocks.append(b)

    return blocks


def block_to_block_type(markdown):
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE

    if markdown.startswith(">"):
        splited_md = markdown.split("\n")
        check = True
        for split in splited_md:
            if split.startswith(">"):
                continue
            else:
                check = False
        if check is True:
            return BlockType.QUOTE

    if markdown.startswith("- "):
        splited_md = markdown.split("\n")
        check = True
        for split in splited_md:
            if split.startswith("- "):
                continue
            else:
                check = False
        if check is True:
            return BlockType.UNORDERED_LIST

    if markdown.startswith("1. "):
        splited_md = markdown.split("\n")
        check = True
        counter = 1
        for split in splited_md:
            if split.startswith(f"{counter}. "):
                counter += 1
                continue
            else:
                check = False
        if check is True:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    children = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children


def html_node_from_block_type(block_type, block):
    match block_type:
        case BlockType.HEADING:
            count = 0
            for char in block:
                if char == "#":
                    count += 1
                else:
                    break

            children = text_to_children(block[count + 1 :])
            return ParentNode(f"h{count}", children)

        case BlockType.QUOTE:
            lines = block.split("\n")
            clean_lines = []
            for line in lines:
                if line.startswith(">"):
                    line = line[1:]
                line = line.strip()
                clean_lines.append(line)
            children = text_to_children(" ".join(clean_lines))
            return ParentNode("blockquote", children)

        case BlockType.UNORDERED_LIST:
            children = []
            list_split = block.split("\n")
            for item in list_split:
                child = text_to_children(item.removeprefix("- "))
                children.append(ParentNode("li", child))
            return ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            children = []
            list_split = block.split("\n")
            for i, item in enumerate(list_split, start=1):
                child = text_to_children(item.removeprefix(f"{i}. "))
                children.append(ParentNode("li", child))
            return ParentNode("ol", children)

        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            text = " ".join(lines)
            children = text_to_children(text)
            return ParentNode("p", children)


def code_to_html(block):
    if not block.startswith("```\n") or not block.endswith("```"):
        raise ValueError("Invalid code block.")

    text = block.removeprefix("```\n")
    text = text.removesuffix("```")
    text_node = TextNode(text, TextType.TEXT)
    code_block = ParentNode("code", [text_node_to_html_node(text_node)])
    return ParentNode("pre", [code_block])


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            outer_block = code_to_html(block)
        else:
            outer_block = html_node_from_block_type(block_type, block)

        blocks_children.append(outer_block)
    return ParentNode("div", blocks_children)
