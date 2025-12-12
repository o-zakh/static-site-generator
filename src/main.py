import shutil
import os
import sys

from html_gen_functions import generate_pages_recursive, generate_page

# Static files
ORIG_PATH = './static'

# Generation files
FROM_PATH = './content'
TEMPLATE_PATH = './template.html'
DEST_PATH = './docs'

basepath = '/'
if len(sys.argv) > 1:
    basepath = sys.argv[1]

print(f'basepath is {basepath}')

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
    if os.path.exists(DEST_PATH):
        shutil.rmtree(DEST_PATH)
    os.mkdir(DEST_PATH)
    
    # Copying static files
    file_сopy(ORIG_PATH, DEST_PATH)

    # Generating html from md
    generate_pages_recursive(FROM_PATH, TEMPLATE_PATH, DEST_PATH, basepath)


main()