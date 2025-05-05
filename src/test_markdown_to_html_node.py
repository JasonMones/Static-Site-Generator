import unittest

from markdown_to_html_node import *


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(
            html,
            expected,
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    
    def test_header(self):
        md = """
#### this is a header (h4)

this is a normal paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>this is a header (h4)</h4><p>this is a normal paragraph</p></div>"
        )

    def test_quote(self):
        md = """
> this is the first line
> and the second
> and the third
> poetry

this is a normal paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is the first line\nand the second\nand the third\npoetry</blockquote><p>this is a normal paragraph</p></div>"
        )

    def test_uo_list(self):
        md = """
- this is the first line
- and the second
- and the third
- poetry

this is a normal paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is the first line</li><li>and the second</li><li>and the third</li><li>poetry</li></ul><p>this is a normal paragraph</p></div>"
        )

    def test_o_list(self):
        md = """
1. this is the first line
2. and the second
3. and the third
4. poetry

this is a normal paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is the first line</li><li>and the second</li><li>and the third</li><li>poetry</li></ol><p>this is a normal paragraph</p></div>"
        )


if __name__ == "__main__":
    unittest.main() 