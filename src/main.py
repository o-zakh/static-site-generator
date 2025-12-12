import shutil
import os
from html_gen_functions import generate_page

# Static
PATH = '/home/oleg/workspace/github.com/o-zakh/static-site-generator/public'
ORIG_PATH = '/home/oleg/workspace/github.com/o-zakh/static-site-generator/static'

# Generation files
FROM_PATH = '/home/oleg/workspace/github.com/o-zakh/static-site-generator/content/index.md'
TEMPLATE_PATH = '/home/oleg/workspace/github.com/o-zakh/static-site-generator/template.html'
DEST_PATH = '/home/oleg/workspace/github.com/o-zakh/static-site-generator/public/index.html'

# Copy all files from 'original_directory' to 'dest_directory'
def file_сopy(original_directory, dest_directory):
    for file in os.listdir(original_directory):
        file_path = os.path.join(original_directory, file)
        if os.path.isfile(file_path):
            print(f'copying file "{file}"')
            shutil.copy(file_path, dest_directory)
        else:
            new_destination = os.path.join(dest_directory, file)
            os.mkdir(new_destination)
            print(f'opening directory "{file}"')
            file_сopy(file_path, new_destination)
    return

def main():

    # Deleting everything in the public directory.
    if os.path.exists(PATH):
        shutil.rmtree(PATH)
    os.mkdir(PATH)
    
    # Copying static files
    file_сopy(ORIG_PATH, PATH)

    # Generating html from md
    generate_page(FROM_PATH, TEMPLATE_PATH, DEST_PATH)


main()