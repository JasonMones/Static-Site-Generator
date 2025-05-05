import unittest

from parentnode import *
from leafnode import *


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.children, [child_node])
        

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("p", [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<p><span>child1</span><b>child2</b><span>child3</span></p>")

    def test_to_html_with_main_parent_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"color": "red"})
        self.assertEqual(parent_node.to_html(), "<div color=\"red\"><span>child</span></div>")

    def test_to_html_with_child_props(self):
        child_node1 = LeafNode("span", "child1", {"color": "red"})
        child_node2 = LeafNode("b", "child2", {"color": "green"})
        parent_node = ParentNode("p", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<p><span color=\"red\">child1</span><b color=\"green\">child2</b></p>")

if __name__ == "__main__":
    unittest.main()