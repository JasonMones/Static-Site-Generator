import unittest

from markdown_conversion_methods import *

class TestMarkDownConversionMethods(unittest.TestCase): 
    def test_split_inline_markdown_bold(self):
        node_text = "this has an inline **bold** tag"
        node = TextNode(node_text, TextType.TEXT)
        expected = [
                    TextNode("this has an inline ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" tag", TextType.TEXT)
        ]
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(actual, expected)

    def test_split_inline_markdown_italic(self):
        node_text = "this has an inline _italic_ tag"
        node = TextNode(node_text, TextType.TEXT)
        expected = [
                    TextNode("this has an inline ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" tag", TextType.TEXT)
        ]
        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(actual, expected)

    def test_split_multiple_inline(self):
        node_text1 = "this has an inline **bold** tag"
        node_text2 = "this has another inline **bold** tag"
        node1 = TextNode(node_text1, TextType.TEXT)
        node2 = TextNode(node_text2, TextType.TEXT)
        expected = [
                    TextNode("this has an inline ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" tag", TextType.TEXT),
                    TextNode("this has another inline ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" tag", TextType.TEXT)
        ]
        actual = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(actual, expected)

    def test_split_no_delimiter(self):
        node_text = "no inline tags here"
        node = TextNode(node_text, TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [node])

    def test_defined_text_type(self):
        node_text = "already has a texttype"
        node = TextNode(node_text, TextType.ITALIC)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [node])

    def test_image_regex(self):
        text = "this has an image![alt text](https://boobs)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "https://boobs")])

    def test_multiple_image_regex(self):
        text = "this has two images, first: ![first](https://first/bootdev.com) and second: ![second](https://second.com)"
        self.assertEqual(extract_markdown_images(text), [("first", "https://first/bootdev.com"), ("second", "https://second.com")])

    def test_link_regex(self):
        text = "this has a link[anchor text](https://boobs)"
        self.assertEqual(extract_markdown_links(text), [("anchor text", "https://boobs")])

    def test_multiple_link_regex(self):
        text = "this has two links, first: [first](https://first/bootdev.com) and second: [second](https://second.com)"
        self.assertEqual(extract_markdown_links(text), [("first", "https://first/bootdev.com"), ("second", "https://second.com")])

    def test_node_images_singular(self):
        node = TextNode("this has an image ![alt text](https://whatever) other stuff", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
                                                    TextNode("this has an image ", TextType.TEXT),
                                                    TextNode("alt text", TextType.IMAGE, "https://whatever"),
                                                    TextNode(" other stuff", TextType.TEXT)
        ])

    def test_node_images_no_end_no_start(self):
        node = TextNode("![alt text](https://whatever)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
                                                    TextNode("", TextType.TEXT),
                                                    TextNode("alt text", TextType.IMAGE, "https://whatever"),
                                                    TextNode("", TextType.TEXT)
        ])

    def test_node_images_several_images(self):
        node = TextNode("first img ![alt text](https://whatever) second img ![alt text](https://something) hooray", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
                                                    TextNode("first img ", TextType.TEXT),
                                                    TextNode("alt text", TextType.IMAGE, "https://whatever"),
                                                    TextNode(" second img ", TextType.TEXT),
                                                    TextNode("alt text", TextType.IMAGE, "https://something"),
                                                    TextNode(" hooray", TextType.TEXT)
        ])

    def test_node_links(self):
        node = TextNode("this has a link [anchored text](https://whatever) other stuff", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
                                                    TextNode("this has a link ", TextType.TEXT),
                                                    TextNode("anchored text", TextType.LINK, "https://whatever"),
                                                    TextNode(" other stuff", TextType.TEXT)
        ])

    def test_node_links_several_links(self):
        node = TextNode("first img [alt text](https://whatever) second img [alt text](https://something) hooray", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
                                                    TextNode("first img ", TextType.TEXT),
                                                    TextNode("alt text", TextType.LINK, "https://whatever"),
                                                    TextNode(" second img ", TextType.TEXT),
                                                    TextNode("alt text", TextType.LINK, "https://something"),
                                                    TextNode(" hooray", TextType.TEXT)
        ])

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
                TextNode("", TextType.TEXT)
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode("", TextType.TEXT)
                    ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)

    def test_text_to_textnodes_missing_texttype(self):
        text = "This is an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
                    TextNode("This is an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode("", TextType.TEXT)
                    ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)

    def test_text_to_textnodes_missing_link(self):
        text = "This is an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
                    TextNode("This is an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode("", TextType.TEXT)
                    ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)

    def test_text_to_textnodes_one_tag(self):
        text = "This is an _italic_ word"
        expected = [
                    TextNode("This is an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word", TextType.TEXT)
                    ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()