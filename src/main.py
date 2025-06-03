import os, sys
import shutil

from copystatic import copy_source_destination, generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

if sys.argv[1]:
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_source_destination(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(
        os.path.join(dir_path_content),
        template_path,
        os.path.join(dir_path_public),
        basepath=basepath
    )


main()
