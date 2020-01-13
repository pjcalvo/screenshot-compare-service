import os

# need to config this
BASE_DIR = 'base'
DIFFERENCES_DIR = 'differences'
TARGETS_DIR = 'targets'


def create_folders(screenshots_directory):
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
