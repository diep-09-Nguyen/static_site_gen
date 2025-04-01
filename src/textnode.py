from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType | str, url: str | None = None):
        if isinstance(text_type, str):
            try:
                text_type = TextType(text_type)
            except ValueError:
                raise TypeError(f"invalid type for TextType: {text_type}")
        self.text = text
        self.text_type = text_type
        self.url = url

    def text_node_to_html_node(self) -> LeafNode:
        node_map = {
            TextType.TEXT: LeafNode("", self.text),
            TextType.BOLD: LeafNode("b", self.text),
            TextType.ITALIC: LeafNode("i", self.text),
            TextType.CODE: LeafNode("code", self.text),
            TextType.LINK: LeafNode("a", self.text, [], {"href": self.url}),
            TextType.IMAGE: LeafNode(
                "img", "", [], {"src": self.url, "alt": self.text}
            ),
        }
        try:
            return node_map[self.text_type]
        except KeyError:
            raise ValueError(f"Invalid text type: {self.text_type}")

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TextNode):
            return False

        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
