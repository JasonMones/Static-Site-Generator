import unittest

from block_methods import *


class TestBlockMethods(unittest.TestCase):    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items



    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_type_code(self):
        block = """
```
code
```
"""
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_block_type_heading(self):
        block = """
## a header
random shit
"""
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_type_quote(self):
        block = """
> first quote
> second quote
> ahhhhh
"""
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_block_type_uo_list(self):
        block = """
- first
- second
- third
"""
        self.assertEqual(BlockType.UO_LIST, block_to_block_type(block))

    def test_block_type_o_list(self):
        block = """
1. first
2. second
3. third
"""
        self.assertEqual(BlockType.O_LIST, block_to_block_type(block))

    def test_block_type_paragraph(self):
        block = """
this is a normal paragraph
heeheehah
meow
"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

if __name__ == "__main__":
    unittest.main()