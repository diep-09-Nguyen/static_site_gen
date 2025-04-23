import unittest

from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class Test_textToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        input_text = "This is just plain text."
        expected = [TextNode("This is just plain text.", "text")]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected)

    def test_bold_text(self):
        input_text = "This is **bold** text."
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text.", "text"),
        ]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected)

    def test_italic_text(self):
        input_text = "This is _italic_ text."
        expected = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text.", "text"),
        ]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected)

    def test_code_text(self):
        input_text = "Here is `code`."
        expected = [
            TextNode("Here is ", "text"),
            TextNode("code", "code"),
            TextNode(".", "text"),
        ]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected)

    def test_image(self):
        input_text = "Look at this ![cat](http://cat.png)"
        expected = [
            TextNode("Look at this ", "text"),
            TextNode("cat", "image", "http://cat.png"),
        ]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected)

    def test_link(self):
        input_text = "Click [here](http://example.com)"
        expected = [
            TextNode("Click ", "text"),
            TextNode("here", "link", "http://example.com"),
        ]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected)

    def test_combined(self):
        input_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
