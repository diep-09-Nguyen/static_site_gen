import unittest


from textnode import TextNode, TextType


class Test_TextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("", TextType.ITALIC)
        node4 = TextNode("", TextType.ITALIC)
        node5 = TextNode(None, None)

        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node4)
        self.assertNotEqual(node, node5)

    def test_text_type(self):
        node1 = TextNode("", TextType.ITALIC)
        node2 = TextNode("", TextType.ITALIC)
        node3 = TextNode("", TextType.BOLD)
        node4 = TextNode("", TextType.BOLD)
        node5 = TextNode("", TextType.NORMAL)
        node6 = TextNode("", TextType.NORMAL)
        node7 = TextNode("", TextType.CODE)
        node8 = TextNode("", TextType.CODE)
        node9 = TextNode("", TextType.LINK)
        node10 = TextNode("", TextType.LINK)
        node11 = TextNode("", TextType.IMAGE)
        node12 = TextNode("", TextType.IMAGE)

        self.assertEqual(node1, node2)
        self.assertEqual(node3, node4)
        self.assertEqual(node5, node6)
        self.assertEqual(node7, node8)
        self.assertEqual(node9, node10)
        self.assertEqual(node11, node12)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node2, node4)
        self.assertNotEqual(node5, node7)
        self.assertNotEqual(node6, node8)
        self.assertNotEqual(node9, node11)
        self.assertNotEqual(node10, node12)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.example.com")
        node2 = TextNode(
            "This is a text node", TextType.BOLD, "https://www.example.com"
        )
        node3 = TextNode("This is a text node", TextType.BOLD, None)
        node4 = TextNode("This is a text node", TextType.BOLD, None)

        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node4)


if __name__ == "__main__":
    unittest.main()
