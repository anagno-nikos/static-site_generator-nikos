import os, shutil

from block_markdown import markdown_to_html_node

def copy_source_destination(source = "", destination= ""):
        
    if not os.path.exists(source):
        raise Exception(f"source dir {source} does not exist inside {os.getcwd()}")

    if not os.path.exists(destination):
        os.mkdir(destination)

    for file in os.listdir(source):

        if os.path.isfile(os.path.join(source, file)):
            print(f"Copying file {os.path.join(source, file)}")
            shutil.copy(os.path.join(source, file), os.path.join(destination, file))
            print(f"File {os.path.join(source, file)} successfully copied")

        else:
            copy_source_destination(  os.path.join(source, file) , os.path.join(destination, file) )


def extract_title(markdown:str):
    lines = markdown.split("\n")
    for line in lines:
        if not line.startswith("# "):
            continue
        return line.removeprefix("# ").strip()
    raise Exception("no h1 header found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_path_content = f.read()
    with open(template_path) as f:
        template_html = f.read()
    
    from_html_string = markdown_to_html_node(from_path_content).to_html()
    
    title_md = extract_title(from_path_content)
    
    new_template_html = template_html.replace("{{ Title }}", title_md)
    
    html_to_write = new_template_html.replace("{{ Content }}", from_html_string)
    
    html_to_write = html_to_write.replace('href="/', f'href="{basepath}')
    html_to_write = html_to_write.replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, "x") as write_file:
        write_file.write(html_to_write)
        

def generate_pages_recursive(
    dir_path_content, 
    template_path,
    dest_dir_path,
    basepath,
):
    
    for dir in os.listdir(dir_path_content):
        new_dir_content_path = os.path.join(dir_path_content, dir)
        new_dir_dest_path = os.path.join(dest_dir_path, dir.replace(".md", ".html"))
        if os.path.isdir(new_dir_content_path):
            generate_pages_recursive(new_dir_content_path, template_path, new_dir_dest_path, basepath)
        elif os.path.isfile(new_dir_content_path):
            generate_page(new_dir_content_path, template_path, new_dir_dest_path, basepath)
    