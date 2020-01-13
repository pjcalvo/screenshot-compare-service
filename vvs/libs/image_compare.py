from PIL import Image, ImageDraw
from datetime import datetime
import os

DEFAULT_RESOLUTION = (1024, 768)
COLUMNS = 120
ROWS = 80


def analyze(base, target, source_dir, differences_dir, resolution=DEFAULT_RESOLUTION):

    try:
        test_failed = False

        # open images and resize them
        screenshot_base = Image.open(os.path.join(source_dir, base))
        screenshot_base = screenshot_base.resize(resolution)
        screenshot_target = Image.open(os.path.join(source_dir, target))
        screenshot_target = screenshot_target.resize(resolution)

        screen_width, screen_height = screenshot_target.size

        # this is just a division ceiling
        block_width = ((screen_width - 1) // COLUMNS) + 1
        block_height = ((screen_height - 1) // ROWS) + 1

        for y in range(0, screen_height, block_height+1):
            for x in range(0, screen_width, block_width+1):
                region_target = process_region(screenshot_target, x, y, block_width, block_height)
                region_base = process_region(screenshot_base, x, y, block_width, block_height)

                if region_base is not None and region_target is not None \
                        and region_base != region_target:
                    test_failed = True
                    draw = ImageDraw.Draw(screenshot_target)
                    draw.rectangle((x, y, x+block_width, y+block_height), outline="red")

        if test_failed:
            print('*** There are visual differences. Saving results to /difference.')
            file_name = f'{datetime.now()}.png'
            full_path = os.path.join(differences_dir, file_name)
            screenshot_target.save(full_path)
            return file_name
        else:
            print('*** No visual differences.')
    except FileNotFoundError as ex:
        print(ex)
        return None


def process_region(image, x, y, width, height):
    region_total = 0

    # This can be used as the sensitivity factor,
    # the larger it is the less sensitive the comparison
    factor = 150

    for coordinateY in range(y, y+height):
        for coordinateX in range(x, x+width):
            try:
                pixel = image.getpixel((coordinateX, coordinateY))
                region_total += sum(pixel)/4
            except Exception:
                return None

    return region_total/factor
