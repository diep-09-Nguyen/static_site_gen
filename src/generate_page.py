import os

from blocks import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_md = f.read()

    with open(template_path) as f:
        template = f.read()

    title = extract_title(from_md)
    html = markdown_to_html_node(from_md).to_html()

    generated_html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html
    )
    dir = os.path.dirname(dest_path)
    if not os.path.exists(dir):
        os.makedirs(dir)

    print(dest_path)
    with open(dest_path, "x") as f:
        f.write(generated_html)

    print("Finished generating page")


def generate_page_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    print(
        f"Generating pages recursively from {dir_path_content} to {dest_dir_path} using {template_path}"
    )

    ls = os.listdir(dir_path_content)
    print(ls)
    for item in ls:
        new_content_path = os.path.join(dir_path_content, item)
        new_dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
        if os.path.isfile(new_content_path):
            generate_page(new_content_path, template_path, new_dest_path)
        elif os.path.isdir(new_content_path):
            generate_page_recursive(new_content_path, template_path, new_dest_path)
