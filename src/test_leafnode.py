import unittest

from leafnode import *


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leafnode_atag(self):
        node_props = dict({"href": "https://something.com"})

        node = LeafNode("a","this is a link to something", props=node_props)
        expected = "<a href=\"https://something.com\">this is a link to something</a>"
        self.assertEqual(node.to_html(), expected)

    def test_no_tag(self):
        node = LeafNode(None, "raw html text")
        self.assertEqual(node.to_html(), "raw html text")

if __name__ == "__main__":
    unittest.main()