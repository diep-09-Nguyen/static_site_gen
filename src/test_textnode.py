import unittest

from enum import Enum
from textnode import TextNode, TextType
from htmlnode import LeafNode


class Test_TextNode(unittest.TestCase):
    def test_eq_same(self):
        a = TextNode("hello", TextType.TEXT)
        b = TextNode("hello", TextType.TEXT)
        self.assertEqual(a, b)

    def test_eq_different_text(self):
        a = TextNode("hello", TextType.TEXT)
        b = TextNode("world", TextType.TEXT)
        self.assertNotEqual(a, b)

    def test_eq_different_type(self):
        a = TextNode("hello", TextType.TEXT)
        self.assertNotEqual(a, "hello")

    def test_to_html_node_text(self):
        node = TextNode("hello", TextType.TEXT)
        expected = LeafNode("", "hello")
        self.assertEqual(node.text_node_to_html_node(), expected)

    def test_to_html_node_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        expected = LeafNode("b", "bold text")
        self.assertEqual(node.text_node_to_html_node(), expected)

    def test_to_html_node_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        expected = LeafNode("i", "italic text")
        self.assertEqual(node.text_node_to_html_node(), expected)

    def test_to_html_node_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        expected = LeafNode("code", "print('hi')")
        self.assertEqual(node.text_node_to_html_node(), expected)

    def test_to_html_node_link(self):
        node = TextNode("click me", TextType.LINK, "http://example.com")
        expected = LeafNode("a", "click me", [], {"href": "http://example.com"})
        self.assertEqual(node.text_node_to_html_node(), expected)

    def test_to_html_node_image(self):
        node = TextNode("an image", TextType.IMAGE, "http://image.url")
        expected = LeafNode(
            "img", "", [], {"src": "http://image.url", "alt": "an image"}
        )
        self.assertEqual(node.text_node_to_html_node(), expected)

    def test_to_html_node_invalid_type(self):
        class FakeType(Enum):
            UNKNOWN = "unknown"

        with self.assertRaises(ValueError):
            node = TextNode("oops", TextType(FakeType.UNKNOWN))
            node.text_node_to_html_node()


if __name__ == "__main__":
    unittest.main()
