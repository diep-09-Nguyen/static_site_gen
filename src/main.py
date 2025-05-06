from copytree import copytree
from generate_page import generate_page, generate_page_recursive


def main():
    copytree("static", "public")
    generate_page_recursive("content", "template.html", "public")


main()
