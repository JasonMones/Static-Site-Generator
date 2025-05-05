import unittest

from main import *


class TestMain(unittest.TestCase): 
    def test_extract_title(self):
        md = """
# TITLE

normal paragraph
"""

        bad_md = """
## TITLE

normal paragraph
"""
        self.assertEqual(extract_title(md), "TITLE")
        #self.assertRaises(ValueError("markdown document must have an h1 tag"), extract_title(bad_md))
        #raises correct ValueError

if __name__ == "__main__":
    unittest.main()