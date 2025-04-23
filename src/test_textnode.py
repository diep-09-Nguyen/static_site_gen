import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from split_nodes_delimiter import split_nodes_image, split_nodes_link


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
        expected = LeafNode("a", "click me", {"href": "http://example.com"})
        self.assertEqual(node.text_node_to_html_node(), expected)

    def test_to_html_node_(self):
        node = TextNode("an --line-number", TextType.IMAGE, "http://--line-number.url")
        expected = LeafNode(
            "img",
            "",
            {"src": "http://--line-number.url", "alt": "an --line-number"},
        )
        self.assertEqual(node.text_node_to_html_node(), expected)

    def test_to_html_node_invalid_type(self):
        node = TextNode("oops", "bold")
        node.text_type = "not a node"  # type: ignore

        with self.assertRaises(ValueError):
            node.text_node_to_html_node()

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(result, expected)

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(result, expected)
