import unittest

from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter


class test_split_nodes_delimiter(unittest.TestCase):
    def test_single_delimiter_pair(self):
        nodes = [TextNode("This is `code`.", "text")]
        result = split_nodes_delimiter(nodes, "`", "code")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        nodes = [TextNode("This is normal.", "text")]
        result = split_nodes_delimiter(nodes, "`", "code")
        expected = nodes

        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        nodes = [TextNode("This is `broken.", "text")]
        result = split_nodes_delimiter(nodes, "`", "code")
        expected = nodes

        self.assertEqual(result, expected)

    def test_delimiter_at_start(self):
        nodes = [TextNode("`start` of line.", "text")]
        result = split_nodes_delimiter(nodes, "`", "code")
        expected = [
            TextNode("start", "code"),
            TextNode(" of line.", "text"),
        ]

        self.assertEqual(result, expected)

    def test_delimiter_at_end(self):
        nodes = [TextNode("end of `line.`", "text")]
        result = split_nodes_delimiter(nodes, "`", "code")
        expected = [
            TextNode("end of ", "text"),
            TextNode("line.", "code"),
        ]

        self.assertEqual(result, expected)

    def test_multiple_nodes_mixed(self):
        nodes = [
            TextNode("This is `code`.", "text"),
            TextNode("This is normal.", "text"),
            TextNode("`start` of line.", "text"),
        ]
        result = split_nodes_delimiter(nodes, "`", "code")
        expected = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(".", "text"),
            TextNode("This is normal.", "text"),
            TextNode("start", "code"),
            TextNode(" of line.", "text"),
        ]

        self.assertEqual(result, expected)
