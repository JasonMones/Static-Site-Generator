from textnode import *
import os
import shutil
from markdown_to_html_node import markdown_to_html_node

ROOT_PATH = "/home/masonjones/projects/python/Static-Site-Generator"

def remove_public_files(path):
    in_dir = os.listdir(path)
    for file in in_dir:
        current_file = path + "/" + file
        if os.path.isfile(current_file):
            os.remove(current_file)
            print(f"deleting '{current_file}'")
        elif os.path.exists(current_file):
            remove_public_files(current_file)
            shutil.rmtree(current_file)

def copy_static_files(static_path, public_path):
    #shutil.copy(src, dst)
    in_dir = os.listdir(static_path)
    for file in in_dir:
        current_file = static_path + "/" + file
        if os.path.isfile(current_file):
            shutil.copy(current_file, public_path)
            print(f"copying '{current_file}' to '{public_path}'")
        elif os.path.exists(current_file):
            new_public_dir = public_path + "/" + file
            os.mkdir(new_public_dir)
            copy_static_files(current_file, new_public_dir)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line == "":
            continue
        if line[0] != "#":
            continue
        if line[1] == "#":
            raise ValueError("markdown document must have an h1 tag")
        return line.strip("# ")
    raise ValueError("markdown document must have an h1 tag")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()
    with open(template_path, "r") as template_file:
        template = template_file.read()

    page_html = markdown_to_html_node(markdown).to_html()
    html_title = extract_title(markdown)

    template = template.replace("{{ Title }}", html_title)
    template = template.replace("{{ Content }}", page_html)

    dest_path = dest_path.replace("md", "html")
    with open(dest_path, "w") as dest_file:
        dest_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    in_dir = os.listdir(dir_path_content)
    for file in in_dir:
        current_path = dir_path_content + "/" + file
        if os.path.isfile(current_path):
            generate_page(current_path, template_path, dest_dir_path + "/" + file)
        elif os.path.exists(current_path):
            new_dest_dir = dest_dir_path + "/" + file
            os.mkdir(new_dest_dir)
            generate_pages_recursive(current_path, template_path, new_dest_dir)

def main():
    global ROOT_PATH
    public_dir = ROOT_PATH + "/public"
    static_dir = ROOT_PATH + "/static"
    content_dir = ROOT_PATH + "/content"
    template_file = ROOT_PATH + "/template.html"

    remove_public_files(public_dir)
    copy_static_files(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_file, public_dir)


if __name__ == "__main__":
    main()