from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os

CHROME_LOCATION = './drivers/chromedriver'
FIREFOX_LOCATION = './drivers/geckodriver'

DEFAULT_RESOULUTION = (1024, 768)
DEFAULT_TEST_NAME = 'image-test'


def capture_screens(
        url, browser, file_identificator, directory_path,
        test_name=DEFAULT_TEST_NAME,
        resolution=DEFAULT_RESOULUTION):
    x = resolution[0]
    y = resolution[1]

    file_name = f'{ test_name }_{ x }x{ y }_{ file_identificator }.png'
    file_path = os.path.join(directory_path, file_name)

    print(f"** Capturing {url} for browser {browser} and screenshot in {file_path} ...")
    driver = get_driver(browser)
    driver.set_window_size(x, y)  # set desired resolution
    driver.get(url)  # navigate to test URL

    driver.save_screenshot(file_path)
    print(f"** Finish image capturing ...")
    driver.close()

    return file_path


def get_driver(browser):
    if browser == 'chrome':
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(CHROME_LOCATION,  chrome_options=chrome_options)
    elif browser == 'firefox':
        firefox_options = FirefoxOptions()
        firefox_options.headless = True
        return webdriver.Firefox(
            firefox_options=firefox_options,
            executable_path=FIREFOX_LOCATION)
