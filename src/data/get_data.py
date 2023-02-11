import pandas as pd

import time
import os
import datetime
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


class Crawler():
    def connect(self, CFG):
        """
        Initializes the chrome webdriver and navigates to the page where the data is located.
        Nearly all parameters are stored in the config file and able to be modified.
        """
        print("Connecting to Selenium")

        # Iterate through the list of chrome options and add them to the webdriver
        options = webdriver.ChromeOptions()
        for option in CFG.CHROME_OPTS:
            options.add_argument(option)
        self.driver = webdriver.Chrome(options=options, executable_path=CFG.PATH_TO_DRIVER)
        self.driver.get(CFG.URL)
        self.driver.set_window_size(CFG.WINDOW_SIZE[0], CFG.WINDOW_SIZE[1])

        # Wait for the first iframe to load
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "iframe-class")))
        try:
            # These two are errors which often pop up, so we wait for them to load and then refresh the page
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-entry-point"]/div')))
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div'))) 
        except TimeoutException as e:
            pass
        else:
            self.refresh_page()

        # Now we can switch to the results tab where the data is
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "#tab_container > li:nth-child(3) > a"))
        ).click()
        print("Successfully connected to Selenium")

    def teardown_method(self):
        self.driver.quit()

    def refresh_page(self, error):
        print(f"{error}, trying again")
        self.driver.refresh()

    def get_page_count(self, CFG):
        """
        Finds the container holding the last page number and returns it as a string
        """
        # First we see if we have a saved page count from today which we can use
        pagefile = os.path.join(CFG.PAGE_PATH, f"page_count_{CFG.DATE}.txt")
        if os.path.isfile(pagefile):
            with open(pagefile, 'r') as f:
                pages = f.read()
            print(f"Using cached page count: {str(pages)}")
            return str(pages)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "last-page"))  # Add a wait in just incase it loads too fast
        )
        pages = self.driver.find_element(By.CLASS_NAME,
            'last-page'
        ).text
        print(f"Page count: {pages}")
        return str(pages)

    def click_button(self, selector, value, sleep_time=0):
        """
        A method to find a given web element using a selector and value and click it using a heavier duty method than click.
        This is followed by an optional sleep time to allow the page to load

        Args:
            selector -> web element: The type of web element to search for from the common.by.By class, eg. XPATH, CLASS_NAME, etc.
            value -> str: The value of the web element
            sleep_time -> int: The amount of time to sleep after clicking the button
        """
        button = self.driver.find_element(selector, value)
        # The javascript is difficult for selenium to handle, so sometimes we need to use "execute_script" to properly interact with it
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(sleep_time)

    def make_df(self):
        """
        Creates a pd.DataFrame from the table on the page using BeautifulSoup to save the pagesource
        """
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table')
        return pd.read_html(str(table))[0]

    def collect_data(self, pages, CFG):
        """
        This function organizes the previous methods to collect the data from the website
        """
        print("Starting data collection")
        
        previous_date = None
        dfs = [self.make_df()]
        for i in range(1, int(pages)-1):
            WebDriverWait(self.driver, 0.1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "next-page"))  # This element loads the next page of data
            )
            self.click_button(By.CLASS_NAME, "next-page", 0)
            dfs.append(self.make_df())
            if i % 100 == 0:
                print(f"Collected {i} pages")

            # We save frequently in case of interuption/error but replace the saved file each time to reduce clutter
            if (i % 500 == 0) and CFG.SAVE:
                if previous_date is not None:
                    try:
                        path = os.path.join(CFG.RAW_DATA_PATH, f'df-{previous_date}.pkl')
                        os.remove(path)
                    except Exception as e:
                        print(f'Unable to delete previous saved file because of: {e}')
                print("Saving data")
                previous_date = datetime.date.today()
                path = os.path.join(CFG.RAW_DATA_PATH, f'df-{previous_date}.pkl')
                pickle.dump(pd.concat(dfs), open(path, 'wb'))

        print("Finished data collection")
        return pd.concat(dfs, ignore_index=True).reset_index(drop=True)

    def run(self, CFG):
        """
        A high level compilation of the crawlers functionality to use at runtime
        """
        # sourcery skip: remove-pass-body, remove-redundant-if
        pages = self.get_page_count(CFG)
        df = self.collect_data(pages, CFG)
        self.teardown_method()
        if CFG.SAVE:
            path = os.path.join(CFG.RAW_DATA_PATH, f'scraped_data-{CFG.DATE}.csv')
            df.to_csv(path, index=False)
        return df

def main(CFG):
    """
    Since this website often produces terminal errors, we repeat the looped connect method to improve chances of success
    """
    crawler = Crawler()
    try:
        crawler.connect(CFG)
    except Exception as e:
        crawler.teardown_method()
        print(e)
        print("Something went wrong, trying again")
        try:
            crawler.connect(CFG)
        except Exception as e:
            print(e)
            print("Something went wrong again, try again later")
    return crawler.run(CFG)
