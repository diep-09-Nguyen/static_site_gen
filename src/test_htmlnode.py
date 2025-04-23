# pyright:ignore

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        # not equal nodes
        self.assertNotEqual(
            node.to_html(), "<p> Hello, world!</p>", "node and node3 are not equal"
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        parentparent_node = ParentNode("div", [parent_node])

        empty_children = ParentNode("div", [])
        empty_tag = ParentNode("", [child_node])
        invalid_child_type = ParentNode("div", ["not a node"])

        empty_nodes = [
            (empty_children, "ParentNode expects children"),
            (empty_tag, "ParentNode expects a tag"),
        ]

        # exception assert
        for node in empty_nodes:
            with self.assertRaisesRegex(ValueError, node[1]):
                node[0].to_html()

        # invalid child node
        with self.assertRaises(AttributeError):
            invalid_child_type.to_html()

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

        self.assertEqual(
            parentparent_node.to_html(),
            "<div><div><span><b>grandchild</b></span></div></div>",
        )
