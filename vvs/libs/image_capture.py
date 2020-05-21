from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os

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

    # close screenshot
    try: 
        driver.find_element_by_css_selector('.new-alert-x-close').click()
    except:
        print(f"** Problem clicking the x ...")

    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height'))
    driver.find_element_by_tag_name('body').screenshot(file_path)

    print(f"** Finish image capturing ...")
    driver.close()

    return file_name


def get_driver(browser):
    if browser == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        if os.environ.get("GOOGLE_CHROME_BIN"):
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    elif browser == 'firefox':
        firefox_options = FirefoxOptions()
        firefox_options.headless = True
        return webdriver.Firefox(
            firefox_options=firefox_options,
            executable_path=FIREFOX_LOCATION)
