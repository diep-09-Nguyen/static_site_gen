from textnode import TextType, TextNode
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(
    old_nodes: list, delimiter: str, text_type: TextType | str
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if 2 > node.text.count(delimiter):
            new_nodes.append(node)
            continue

        start = node.text.find(delimiter)
        end = node.text.rfind(delimiter) + len(delimiter)

        if 0 < start:
            new_nodes.append(TextNode(node.text[:start], node.text_type))

        inner_text = node.text[start + len(delimiter) : end - len(delimiter)]
        new_nodes.append(TextNode(inner_text, text_type))

        if len(node.text) > end:
            new_nodes.append(TextNode(node.text[end:], node.text_type))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(
            split_node(
                node.text, node.text_type, "image", extract_markdown_images(node.text)
            )
        )
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(
            split_node(
                node.text, node.text_type, "link", extract_markdown_links(node.text)
            )
        )
    return new_nodes


def split_node(
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
        new_nodes.extend(
            [TextNode(subtext, node_type), TextNode(item_text, item_type, item_url)]
        )
    if node_text:
        new_nodes.append(TextNode(node_text, node_type))
    return new_nodes


def splitter_format(type: str) -> str:
    prefix = "!" if type == "image" else ""
    return f"{prefix}[{{text}}]({{url}})"
