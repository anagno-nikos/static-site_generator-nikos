import os
import shutil

from copystatic import copy_source_destination

source_dir = "static"
destination_dir = "public"

def main():
    print("Deleting public directory")
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    
    print("Copying files from static to public directory...") 
    copy_source_destination(source_dir, destination_dir)
    
main()
