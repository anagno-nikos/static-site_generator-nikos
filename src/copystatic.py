import os, shutil

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

