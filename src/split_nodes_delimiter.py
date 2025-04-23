from textnode import TextType, TextNode
from extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
)
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
        escaped = re.escape(delimiter)
        rege = r"{0}([^{0}]*){0}".format(escaped)

        matches = re.findall(rege, node.text)
        # start = node.text.find(delimiter)
        # end = node.text.rfind(delimiter) + len(delimiter)
        new_nodes.extend(
            split_node(node.text, node.text_type, text_type, matches, delimiter)
        )
        # if 0 < start:
        #     new_nodes.append(TextNode(node.text[:start], node.text_type))
        #
        # inner_text = node.text[start + len(delimiter) : end - len(delimiter)]
        # new_nodes.append(TextNode(inner_text, text_type))
        #
        # if len(node.text) > end:
        #     new_nodes.append(TextNode(node.text[end:], node.text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        new_nodes.extend(
            split_node_url(
                node.text, node.text_type, "image", extract_markdown_images(node.text)
            )
        )
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        new_nodes.extend(
            split_node_url(
                node.text, node.text_type, "link", extract_markdown_links(node.text)
            )
        )
    return new_nodes


# Method is similar to the below except it takes in the delimiter as well.
# It's supposed to take the delimiter and split the text based on the extracted markdown.
# Same with split_node_url basically. Only difference is that the list passed in is just a list of strings.
def split_node(
    node_text: str, node_type: TextType, item_type: str, lst: list[str], delimiter: str
) -> list[TextNode]:
    if not lst:
        return [TextNode(node_text, node_type)]
    new_nodes = []
    template = "{delimiter}{text}{delimiter}"

    for item_text in lst:
        splitter = template.format(delimiter=delimiter, text=item_text)
        subtext, node_text = node_text.split(splitter, 1)
        if subtext:
            new_nodes.append(TextNode(subtext, node_type))
        new_nodes.append(TextNode(item_text, item_type))
    if node_text:
        new_nodes.append(TextNode(node_text, node_type))
    return new_nodes


# Iterates through the list and uses the matched list of expressions as a delimiter
# Attaches if the text exists in front and at the end
# Otherwise it'll just append only the extracted markdown
# This will prevent appending and prepending empty TextNodes to the return list
def split_node_url(
    node_text: str,
    node_type: TextType,
    item_type: str,
    lst: list[tuple[str, str]],
) -> list[TextNode]:
    if not lst:
        return [TextNode(node_text, node_type)]

    new_nodes = []
    template = splitter_format(item_type)
    for item_text, item_url in lst:
        splitter = template.format(text=item_text, url=item_url)
        subtext, node_text = node_text.split(splitter, 1)
        if subtext:
            new_nodes.append(TextNode(subtext, node_type))
        new_nodes.append(TextNode(item_text, item_type, item_url))
    if node_text:
        new_nodes.append(TextNode(node_text, node_type))
    return new_nodes


def splitter_format(type: str) -> str:
    prefix = "!" if type == "image" else ""
    return f"{prefix}[{{text}}]({{url}})"
