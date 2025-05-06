import sys

from copytree import copytree
from generate_page import generate_page_recursive


def main():
    basepath = "/"
    if sys.argv[1]:
        basepath = sys.argv[1]
    print(basepath)
    copytree("static", "docs")
    generate_page_recursive("content", "template.html", "docs", basepath)


main()
