import sys

from copystatic import sync_static
from gencontent import generate_pages_recursive


def main():
    source_path = "./static"
    # destination_path = "./public" #local testing
    destination_path = "./docs"
    template_path = "./template.html"
    content_path = "./content"

    try:
        if not sys.argv[1:]:
            basepath = "/"
        else:
            basepath = sys.argv[1]

        sync_static(source_path, destination_path)
        print("Generating html page")
        generate_pages_recursive(
            content_path,
            template_path,
            destination_path,
            basepath,
        )
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


main()
