from PIL import Image, ImageDraw
from datetime import datetime
import os

RESOLUTION = (1024, 768)

def analyze(base, target, difference_dir):

    try:
        columns = 60
        rows = 80
        test_failed = False

        screenshot_base = Image.open(base)
        screenshot_base.resize(RESOLUTION)
        screenshot_target = Image.open(target)
        screenshot_target.resize(RESOLUTION)
        screen_width, screen_height = screenshot_target.size

        block_width = ((screen_width - 1) // columns) + 1 # this is just a division ceiling
        block_height = ((screen_height - 1) // rows) + 1

        for y in range(0, screen_height, block_height+1):
            for x in range(0, screen_width, block_width+1):
                region_target = process_region(screenshot_target, x, y, block_width, block_height)
                region_base = process_region(screenshot_base, x, y, block_width, block_height)

                if region_base is not None and region_target is not None and region_base != region_target:
                    test_failed = True
                    draw = ImageDraw.Draw(screenshot_target)
                    draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")

        if test_failed:
            print('*** There are visual differences. Saving results to /difference.')
            file_name = os.path.join( difference_dir , f'{datetime.now()}.png')
            screenshot_target.save(file_name)
            return file_name
        else:
            print('*** No visual differences.')
    except Exception as ex:
        print(ex)
        return 'Error file was not proccesed'

def process_region(image, x, y, width, height):
    region_total = 0

    # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
    factor = 100

    for coordinateY in range(y, y+height):
        for coordinateX in range(x, x+width):
            try:
                pixel = image.getpixel((coordinateX, coordinateY))
                region_total += sum(pixel)/4
            except:
                return

    return region_total/factor