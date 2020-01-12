from vvs.model.crossbrowser import CrossBrowserModel
from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import sys

CHROME_LOCATION =  './drivers/chromedriver'
FIREFOX_LOCATION = './drivers/geckodriver'
RESOLUTION = {'x':1024, 'y':768}

# STAGING_URL = 'https://www.google.com/?q=keren'
TEST_NAME = 'cross_browser'
SCREENSHOTS_DIR = 'screenshots_cross'
BASE_DIR = 'base'
DIFFERENCES_DIR = 'differences'
TARGETS_DIR = 'targets'

class ImageCapture():

    def __init__(self, url, crossbrowser):
        self.url = url
        self.crossbrowser = crossbrowser   
        self.setup_folders()

    def setup_folders(self):
        self.screenshots_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), SCREENSHOTS_DIR)
        self.base_dir = os.path.join(self.screenshots_dir, BASE_DIR)
        self.differences_dir = os.path.join(self.screenshots_dir, DIFFERENCES_DIR)
        self.targets_dir = os.path.join(self.screenshots_dir, TARGETS_DIR)

        # set the folders to store differences
        self.crossbrowser.set_differences_folder(self.differences_dir)

        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)    
        if not os.path.exists(self.differences_dir):
            os.makedirs(self.differences_dir)    
        if not os.path.exists(self.targets_dir):
            os.makedirs(self.targets_dir)    
    
    def capture_screens(self):
        x = RESOLUTION.get("x")
        y = RESOLUTION.get("y")
        try:
            # capture base
            base_browser = self.crossbrowser.base['browser']
            file_name = f'{ TEST_NAME }_{x}x{y}_base.png'
            file_path = os.path.join(self.base_dir , file_name)
            self.screenshot(self.url, base_browser, file_path, RESOLUTION)       
            self.crossbrowser.set_base_file(file_path)

            # capture targets
            count = 0
            for target in self.crossbrowser.targets:
                count += 1
                target_browser = target['browser']
                target_file_name = f'{ TEST_NAME }_{x}x{y}_target_{count}.png'
                target_file_path = os.path.join(self.targets_dir , target_file_name)
                self.screenshot(self.url, target_browser, target_file_path, RESOLUTION)
                self.crossbrowser.set_target_file(target['browser'], target_file_path)
            return self.crossbrowser

        except NotImplementedError as ex:
            print(ex)
            return None        

    def screenshot(self, url, browser, file_path, resolution):        

        print (f"** Capturing {url} for browser {browser} and screenshot in {file_path} ...")
        driver = self.get_driver(browser)
        driver.set_window_size(resolution.get('x'),resolution.get('y')) # set desired resolution
        driver.get(url) # navigate to test URL

        driver.save_screenshot(file_path)       
        # driver.get_screenshot_as_png()
        print (f"** Finish image capturing ...")
        driver.close()

    @staticmethod
    def get_driver(browser):
        if browser == 'chrome':
            chrome_options = ChromeOptions()  
            chrome_options.add_argument("--headless")  
            return webdriver.Chrome(CHROME_LOCATION,  chrome_options=chrome_options)
        elif browser == 'firefox':
            firefox_options = FirefoxOptions()
            firefox_options.headless = True
            return webdriver.Firefox(firefox_options = firefox_options, executable_path=FIREFOX_LOCATION)
