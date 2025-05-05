import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node1 = TextNode("this is a code node", TextType.CODE)
        node2 = TextNode("this is another code node", TextType.CODE)
        self.assertNotEqual(node1, node2)

    def test_urlcomp(self):
        node1 = TextNode("this TextNode has a url", TextType.LINK, "https://fakeurl.com")
        node2 = TextNode("this TextNode has a url", TextType.LINK, "https://fakeurl.com")
        self.assertEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_and_image(self):
        node_link = TextNode("link", TextType.LINK, url="https://thisalink.com")
        leafnodelink = node_link.text_node_to_html_node()
        node_image = TextNode("alt image", TextType.IMAGE, url="https://imageoops.com")
        leafnodeimg = node_image.text_node_to_html_node()
        actual_link_node = LeafNode("a", "link", props={"href": "https://thisalink.com"})
        actual_img_node = LeafNode("img", "", props={"src": "https://imageoops.com", "alt": "alt image"})
        self.assertEqual(leafnodelink.to_html(), actual_link_node.to_html())
        self.assertEqual(leafnodeimg.to_html(), actual_img_node.to_html())

if __name__ == "__main__":
    unittest.main()