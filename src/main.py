from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


def main():
    test1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    test2 = HTMLNode(props={"a": 1, "b": 2, "c": 3})
    test3 = LeafNode("a", "This is a leaf node")
    print(test1)
    print(test2.props_to_html())
    print(test3.to_html())


main()
