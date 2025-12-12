import os
from md_functions import markdown_to_html_node

def extract_title(markdown):
    heading = None
    for line in markdown.splitlines():
        if not line.startswith("# "):
            continue
        heading = line[2:]
        break
    if heading == None:
        raise Exception ("No h1 header in markdown")
    return heading

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path, "r")
    md_file_contents = md_file.read()
    template_file = open(template_path, "r")
    template_file_contents = template_file.read()
    html_str = markdown_to_html_node(md_file_contents).to_html()
    page_title = extract_title(md_file_contents)
    template_file_contents = template_file_contents.replace("{{ Title }}", page_title)
    template_file_contents = template_file_contents.replace("{{ Content }}", html_str)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    dest_file = open(dest_path, 'w')
    dest_file.write(template_file_contents)
    
    md_file.close()
    template_file.close()
    dest_file.close()