import unittest

from htmlnode import HTMLNode, LeafNode


class Test_HTMLNode(unittest.TestCase):
    def test_propstohtml(self):
        test = ' a="1" b="2" c="3"'
        test2 = ' a="1" b="2"'
        node1 = HTMLNode(props={"a": 1, "b": 2, "c": "3"})
        node2 = HTMLNode()
        node3 = HTMLNode()
        node4 = HTMLNode(props={"a": "1", "b": "2", "c": 3})
        node5 = HTMLNode(props={"a": 1, "b": 2, "c": "3"})

        self.assertEqual(test, node1.props_to_html(), "props is not proper format")
        self.assertEqual(
            node1.props_to_html(),
            node5.props_to_html(),
            "two nodes not equal to each other",
        )
        self.assertNotEqual(node4, node5, "node4, node5: two nodes equal to each other")
        self.assertNotEqual(
            node1.props_to_html(),
            node2.props_to_html(),
            "a None node is equal to a not None node",
        )
        self.assertEqual(
            node2.props_to_html(),
            node3.props_to_html(),
            "None node not equal to None node",
        )
        self.assertNotEqual(test2, node4, "shorter props is equal to longer props")

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        noTag = LeafNode(tag=None, value="no tag")
        noValue = LeafNode(tag="a", value=None)

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        # not equal nodes
        self.assertNotEqual(
            node.to_html(), "<p> Hello, world!</p>", "node and node3 are not equal"
        )

        # requires a value
        self.assertRaises(ValueError, noValue.to_html)

        # requires a tag
        self.assertEqual(noTag.value, "no tag", "noTag value is not None")
