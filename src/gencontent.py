import os
from pathlib import Path

from markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("H1 header not found.")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        md_content = f.read()

    with open(template_path) as f:
        template_content = f.read()

    title_page = extract_title(md_content)
    html_body = markdown_to_html_node(md_content).to_html()
    template_content = template_content.replace("{{ Title }}", title_page)
    template_content = template_content.replace("{{ Content }}", html_body)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_list = os.listdir(dir_path_content)
    for obj in dir_list:
        from_path = os.path.join(dir_path_content, obj)
        dest_path = os.path.join(dest_dir_path, obj)
        if os.path.isfile(from_path):
            if Path(from_path).suffix == ".md":  # ignore non md files
                generate_page(
                    from_path,
                    template_path,
                    Path(dest_path).with_suffix(".html"),
                    basepath,
                )
        elif os.path.isdir(from_path):
            generate_pages_recursive(
                from_path,
                template_path,
                dest_path,
                basepath,
            )
        else:
            raise ValueError(f"Unexpected path type: {from_path}")
