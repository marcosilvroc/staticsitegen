from copystatic import sync_static
from gencontent import generate_pages_recursive


def main():
    source_path = "./static"
    destination_path = "./public"
    template_path = "./template.html"
    content_path = "./content"

    sync_static(source_path, destination_path)
    print("Generating html page")
    generate_pages_recursive(content_path, template_path, destination_path)


main()
