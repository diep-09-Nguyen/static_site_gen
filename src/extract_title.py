import re


def extract_title(markdown: str) -> str:
    m = re.search(r"(?<=^# )(.+)", markdown)
    if not m:
        raise Exception("No h1 header")
    return m.group(0)
