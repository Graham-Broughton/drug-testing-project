from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

import os
import sys
sys.path.append('..')
from config import CFG
CFG=CFG()

class Crawler(object):
    # Use class attributes so that the values can be inherited
    chrome_options = CFG.CHROME_OPTS
    options = webdriver.ChromeOptions()
    if bool(chrome_options) is not None:
        for opt in chrome_options:
            options.add_argument(opt)
    
    def start(self):
        """
        Constructor function that loads any options and connects to the webpage

        Args:
            chrome_options: A list of chrome options to be passed to the webdriver
            url: The url to connect to
            window_size: The size of the window to be opened
        """
        # sourcery skip: remove-pass-body
        print("starting selenium")
        if bool(self.chrome_options) is not None:
            self.driver = webdriver.Chrome(executable_path=CFG.PATH_TO_DRIVER, options=self.options)
        else:
            self.driver = webdriver.Chrome(executable_path=CFG.PATH_TO_DRIVER)

        print("Connected to website")
        self.driver.get(CFG.URL)
        self.driver.set_window_size(CFG.WINDOW_SIZE[0], CFG.WINDOW_SIZE[1])
        return

    def load_webpage(self):
        """
        Loads the results tab by switching frames and clicking on the results tab,
        also contains an intermediate try/except block to look for an error msg, all using explicit waits.        
        """
        print("waiting to switch frames")
        # Need to switch frames to enable interaction with the loaded javascript
        WebDriverWait(self.driver, CFG.FIRST_IFRAME_WAIT).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "iframe-class")))
        print("switched frames, waiting for error messages")

        # checking to see if the error messages are present, if they are, refresh and if not, pass
        try:
            WebDriverWait(self.driver, CFG.SECOND_IFRAME_WAIT).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "/html/body/iframe")))
            WebDriverWait(self.driver, CFG.HEROKU_WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, 'message__title'))) 
            WebDriverWait(self.driver, CFG.REACT_WAIT).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div'))) 
        except TimeoutException as e:
            pass
        else:
            print("Found error messages, refreshing page")
            self.refresh_page()

        # waiting to click results tab
        print("Waiting on results button")
        WebDriverWait(self.driver, CFG.RESULT_BUTTON_WAIT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#tab_container > li:nth-child(3) > a"))
            ).click()
        print("selected results tab")
        return

    def connect(self):
        """
        Implements a counted try/except loop to load the webpage and refresh it in case of a timeout error.
        It also refreshes the page if there is any other exception thrown.
        
        Args:
            max_tries: The max number of loops to try and load the webpage
        """
        self.start()
        loaded = False
        counter = 0
        # While the results tab is not loaded, it goes through N loops trying to open it
        while not loaded:
            try:
                self.load_webpage()
                loaded = True
            except TimeoutException as e:
                self.refresh_page(e)
            except Exception as e:
                print(f"Exception: {e}, trying again")
                self.refresh_page(e)
            counter += 1
            if counter == CFG.MAX_TRIES:  # Found in the CFG python file
                print("Too many attempts, try again")
                self.driver.quit()
                

    def refresh_page(self, error):
        print(f"{error} trying again")
        self.driver.refresh()

    def __del__(self):
        self.driver.quit()
        