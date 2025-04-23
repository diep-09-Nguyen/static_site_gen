import unittest

from textnode import TextNode, TextType
from split_nodes_delimiter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://link.com/link.png) and another [link2](https://link2.com/link2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://link.com/link.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://link2.com/link2.png"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
