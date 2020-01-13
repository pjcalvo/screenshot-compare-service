import os
from datetime import datetime

# need to config this

TEMP_FOLDER = 'temp'


def create_folders():
    screenshots_dir = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        screenshots_directory)
    base_dir = os.path.join(screenshots_dir, BASE_DIR)
    differences_dir = os.path.join(screenshots_dir, DIFFERENCES_DIR)
    targets_dir = os.path.join(screenshots_dir, TARGETS_DIR)

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    if not os.path.exists(differences_dir):
        os.makedirs(differences_dir)
    if not os.path.exists(targets_dir):
        os.makedirs(targets_dir)

    return screenshots_dir


def create_temp_folder():
    screenshots_dir = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        TEMP_FOLDER, str(datetime.now()))
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    
    return screenshots_dir
    

def delete_temp_folder(temp_folder):
    for root, dirs, files in os.walk(temp_folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_folder)
