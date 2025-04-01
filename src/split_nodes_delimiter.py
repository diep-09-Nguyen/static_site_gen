from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType | str):
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
