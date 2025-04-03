import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links


class Test_ExtractMarkdown(unittest.TestCase):
    def test_single_image(self):
        text = "This is a single image ![single_image](https://www.image.com)"
        result = extract_markdown_images(text)
        expected = [("single_image", "https://www.image.com")]

        self.assertListEqual(result, expected)

    def test_single_link(self):
        text = "This is a single link [single_link](https://www.link.com)"
        result = extract_markdown_links(text)
        expected = [("single_link", "https://www.link.com")]

        self.assertListEqual(result, expected)

    def test_mixed_link_image(self):
        text = "This is a single link [single_link](https://www.link.com) and single image ![single_image](https://www.image.com)"

        result = extract_markdown_links(text)
        expected = [("single_link", "https://www.link.com")]
        self.assertListEqual(result, expected)

        result = extract_markdown_images(text)
        expected = [("single_image", "https://www.image.com")]
        self.assertListEqual(result, expected)

    def test_multiple_images(self):
        text = "This is image one ![image_one](https://www.image.com/1) and this is image two ![image_two](https://www.image.com/2)"
        result = extract_markdown_images(text)
        expected = [
            ("image_one", "https://www.image.com/1"),
            ("image_two", "https://www.image.com/2"),
        ]

        self.assertListEqual(result, expected)

    def test_multiple_links(self):
        text = "This is link one [link_one](https://www.link.com/1) and this is link two [link_two](https://www.link.com/2)"
        result = extract_markdown_links(text)
        expected = [
            ("link_one", "https://www.link.com/1"),
            ("link_two", "https://www.link.com/2"),
        ]

        self.assertListEqual(result, expected)

    def test_no_links_no_image(self):
        text = "No links or images"
        result = extract_markdown_links(text)
        expected = []
        self.assertListEqual(result, expected)

        result = extract_markdown_images(text)
        expected = []
        self.assertListEqual(result, expected)

    def test_empty_alt_text(self):
        text_link = "This is an empty alt link [](https://www.link.com)"
        text_image = "This is an empty alt image ![](https://www.image.com)"

        result = extract_markdown_links(text_link)
        expected = [("", "https://www.link.com")]
        self.assertListEqual(result, expected)

        result = extract_markdown_images(text_image)
        expected = [("", "https://www.image.com")]
        self.assertListEqual(result, expected)

    def test_empty_url(self):
        text_link = "This is an empty url link [empty_link]()"
        text_image = "This is an empty url image ![empty_image]()"

        result = extract_markdown_links(text_link)
        expected = [("empty_link", "")]
        self.assertListEqual(result, expected)

        result = extract_markdown_images(text_image)
        expected = [("empty_image", "")]
        self.assertListEqual(result, expected)

    def test_malformed_markdown(self):
        text_link = "Missing end parentheses [broken](https://broken.com"
        text_image = "Missing end parentheses ![broken](https://broken.com"

        result = extract_markdown_links(text_link)
        expected = []
        self.assertListEqual(result, expected)

        result = extract_markdown_images(text_image)
        expected = []
        self.assertListEqual(result, expected)

    def test_special_characters(self):
        text_link = "[click-here_123](https://example.com/test?foo=bar&baz=qux)"
        text_image = "![image-name](https://img.site/image.png?size=large#anchor)"

        result = extract_markdown_links(text_link)
        self.assertListEqual(
            result, [("click-here_123", "https://example.com/test?foo=bar&baz=qux")]
        )

        result = extract_markdown_images(text_image)
        self.assertListEqual(
            result, [("image-name", "https://img.site/image.png?size=large#anchor")]
        )
