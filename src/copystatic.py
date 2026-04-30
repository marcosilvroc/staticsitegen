import os
import shutil


def copy_content(source, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for entry in os.listdir(source):
        entry_path = os.path.join(source, entry)
        dest_path = os.path.join(dest, entry)
        print(f"Copying: {entry_path} -> {dest_path}")
        if os.path.isfile(entry_path):
            shutil.copy(entry_path, dest_path)
        elif os.path.isdir(entry_path):
            print("Folder located, copying subdirectory and files.")
            copy_content(entry_path, dest_path)


def sync_static(source, dest):
    if not os.path.exists(source):
        raise ValueError("Source directory doesn't exist.")

    print("Cleaning public directory")
    if os.path.exists(dest):
        shutil.rmtree(dest)

    print("Copying static files to public directory")
    copy_content(source, dest)
