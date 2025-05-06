import re
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from text_to_textnodes import text_to_textnodes
from textnode import TextNode


class Blocktype(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


text_map = [
    (r"^#{1,6}[\s]+([^#]*)", Blocktype.HEADING),
    (r"(?<=```)([\s\S]*)(?=```)", Blocktype.CODE),
    (r">[\s]*([^>]*)[\n]*", Blocktype.QUOTE),
    (r"- (.*)[\n]*", Blocktype.UNORDERED_LIST),
    (r"\d\. (.*)[\n]*", Blocktype.ORDERED_LIST),
]


def markdown_to_blocks(markdown: str) -> list[str]:
    if not markdown.strip():
        return []
    blocks = markdown.strip().split("\n\n")
    blocks = [block.replace("  ", "") for block in blocks if block.strip()]
    return blocks


# Assumes block is already stripped
# Return block type matching pattern
def block_to_block_type(block: str) -> Blocktype:
    for pattern, blocktype in text_map:
        match = re.findall(pattern, block)
        if match:
            if blocktype == Blocktype.ORDERED_LIST and not is_ORDERED(block):
                return Blocktype.PARAGRAPH
            return blocktype
    return Blocktype.PARAGRAPH


# Returns list of str stripped of pattern
def pattern_matching(text: str) -> list[str]:
    for pattern, _ in text_map:
        match = re.findall(pattern, text)
        if match:
            return match
    return []


def is_ORDERED(block: str) -> bool:
    num = 1
    for line in block.split("\n"):
        if not re.match(rf"{num}\. .*[\n]*", line):
            return False
        num += 1
    return True


def block_to_html_node(block: str, blocktype: Blocktype) -> HTMLNode:
    if blocktype == Blocktype.UNORDERED_LIST or blocktype == Blocktype.ORDERED_LIST:
        children = text_to_list_item(block)
    else:
        children = text_to_children(block)
    type_map = {
        Blocktype.PARAGRAPH: ParentNode("p", children, None),
        Blocktype.QUOTE: ParentNode("blockquote", children, None),
        Blocktype.HEADING: ParentNode(f"h{block.count('#')}", children, None),
        Blocktype.CODE: ParentNode(
            "pre",
            [
                TextNode(
                    block.strip("\r\n").strip("`").lstrip("\r\n"), "code", None
                ).text_node_to_html_node()
            ],
            None,
        ),
        Blocktype.UNORDERED_LIST: ParentNode("ul", children, None),
        Blocktype.ORDERED_LIST: ParentNode("ol", children, None),
    }
    return type_map[blocktype]


def text_to_children(text: str):
    children = []

    string = text.replace("\n", " ").replace("\r", " ")
    if not string:
        return []

    matches = pattern_matching(string)
    if matches:
        string = ""
        for match in matches:
            string += match

    nodes = text_to_textnodes(string.replace("  ", " "))
    for node in nodes:
        children.append(node.text_node_to_html_node())
    return children


def text_to_list_item(text: str):
    children = []
    matches = pattern_matching(text)
    nodes = []
    for match in matches:
        nodes.append(text_to_textnodes(match))

    for node in nodes:
        temp = []
        for item in node:
            temp.append(item.text_node_to_html_node())
        children.append(ParentNode("li", temp))
    return children


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        node = block_to_html_node(block, blocktype)
        children.append(node)
    return ParentNode("div", children, None)
