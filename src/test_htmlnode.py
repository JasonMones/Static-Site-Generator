import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    
    node = HTMLNode("zzz","yyy","xxx",{"a": "aa", "b": "bb", "c": "cc"})

    def test_comparison(self):
        node1 = self.node
        node2 = HTMLNode("zzz","yyy","xxx",{"a": "aa", "b": "bb", "c": "cc"})
        self.assertEqual(node1, node2)

    def test_comparison_noteq(self):
        node1 = self.node
        node2 = HTMLNode("zz","yy","xx",{"a": "aa", "b": "bb", "c": "cc"})

    def test_props_to_html(self):
        actual = self.node.props_to_html()
        expected = " a=\"aa\" b=\"bb\" c=\"cc\""
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()