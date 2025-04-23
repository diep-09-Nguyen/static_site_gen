import unittest

from blocks import (
    Blocktype,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


class Test_MarkdownBlocks(unittest.TestCase):
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

    def test_empty_input(self):
        markdown = ""
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [])

    def test_only_whitespace(self):
        markdown = "     \n\n  \t\n   "
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [])

    def test_valid_content(self):
        markdown = "This is a valid block.\n\nAnother block."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["This is a valid block.", "Another block."])

    def test_mixed_with_empty_blocks(self):
        markdown = "This is a valid block.\n\n     \n\nAnother block.\n\n  \t\n\n"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["This is a valid block.", "Another block."])

    def test_multiple_empty_blocks_between_content(self):
        markdown = "Content before.\n\n\n\nContent after."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Content before.", "Content after."])

    def test_edge_case_single_empty_block(self):
        markdown = "\n\n"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [])


class MarkdownBlockToBlock(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), Blocktype.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), Blocktype.HEADING)
        self.assertNotEqual(block_to_block_type("####### Too many"), Blocktype.HEADING)

    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), Blocktype.CODE)

        not_code = "```\nprint('hi')\n"
        self.assertEqual(block_to_block_type(not_code), Blocktype.PARAGRAPH)

    def test_quote_block(self):
        quote = "> First line\n> Second line\n> Still quoting"
        self.assertEqual(block_to_block_type(quote), Blocktype.QUOTE)

    def test_unordered_list(self):
        ulist = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ulist), Blocktype.UNORDERED_LIST)

    def test_ordered_list(self):
        olist = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(olist), Blocktype.ORDERED_LIST)

        skip_number = "1. First\n3. Skipped"
        self.assertEqual(block_to_block_type(skip_number), Blocktype.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a normal paragraph."), Blocktype.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("Just some text\nacross multiple lines."),
            Blocktype.PARAGRAPH,
        )


class BlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")

    def test_blockquote(self):
        md = "> This is a blockquote\n> with two lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with two lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- First item\n- Second item\n- Third item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )
