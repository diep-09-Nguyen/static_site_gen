import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_bold(text) -> list[str]:
    return re.findall(r"\*\*([^\*]*)\*\*", text)


def extract_markdown_italic(text) -> list[str]:
    return re.findall(r"\_([^\_]*)\_", text)


def extract_markdown_code(text) -> list[str]:
    return re.findall(r"([^\`]*)", text)
