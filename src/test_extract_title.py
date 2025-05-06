import unittest
from extract_title import extract_title


class Test_ExtractTitle(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extract_title("# Hello World"), "Hello World")

    def test_paragraph(self):
        md = "# First Title\n\nSome paragraph.\n## Subtitle\nAnother paragraph."
        self.assertEqual(extract_title(md), "First Title")

    def test_special_characters(self):
        md = "# Special Title@World! 2020"
        self.assertEqual(extract_title(md), "Special Title@World! 2020")

    def test_leading_spaces(self):
        md = "#     Title"
        self.assertEqual(extract_title(md), "    Title")

    def test_notitle(self):
        md = "Title\n\nSome paragraph."
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header")

    def test_title_not_at_start(self):
        md = "Not title\n\n\n# Title in middle\n\nNot title 2"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header")

    def test_multiple_titles(self):
        md = "# Title 1\n\n## Title 2\n\n### Title 3"
        self.assertEqual(extract_title(md), "Title 1")
