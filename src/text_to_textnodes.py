from textnode import TextNode
from split_nodes_delimiter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Takes in a string and returns a list of TextNodes split based on bold, italic, code, image, and link
    """
    text_nodes = [TextNode(text, "text")]
    text_nodes = split_nodes_delimiter(text_nodes, "**", "bold")
    text_nodes = split_nodes_delimiter(text_nodes, "_", "italic")
    text_nodes = split_nodes_delimiter(text_nodes, "`", "code")
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
