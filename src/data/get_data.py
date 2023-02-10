import pandas as pd
from bs4 import BeautifulSoup
from os.path import join
import time
import os
import datetime
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

import sys
sys.path.append(os.getcwd())
from config import CFG

current_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
data_path = os.path.join(current_dir, "data_files")

CFG = CFG()

class Crawler():
    def connect(self):
        print("Connecting to Selenium")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--start-maximized")
        options.add_argument("--headless")#CFG.CHROME_OPTS
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(CFG.URL)
        self.driver.set_window_size(CFG.WINDOW_SIZE[0], CFG.WINDOW_SIZE[1])
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "iframe-class")))

        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-entry-point"]/div')))
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div'))) 
        except TimeoutException as e:
            pass
        else:
            self.refresh_page()

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

    def get_page_count(self):
        """
        Finds the container holding the last page number and returns it as a string
        """
        page_path = os.path.join(data_path, f"page_data\page_count_{CFG.DATE}.txt")
        if os.path.isfile(page_path):
            with open(page_path, 'r') as f:
                pages = f.read()
            print(f"Using cached page count: {str(pages)}")
            return str(pages)
        pages = self.driver.find_element(By.CLASS_NAME,
            'last-page'
        ).text
        print(f"Page count: {pages}")
        return str(pages)

    def click_button(self, selector, value, sleep_time=0):
        button = self.driver.find_element(selector, value)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(sleep_time)

    def make_df(self):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table')
        return pd.read_html(str(table))[0]

    def collect_data(self, pages, start_page=0, save=True):
        previous_date = None
        print("Starting data collection")
        if start_page != 0:
            self.driver.find_element(By.CLASS_NAME, "current-page").click()
            self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(str(start_page))
            self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(Keys.ENTER)
        dfs = [self.make_df()]
        for i in range(1, int(pages)-1):
            WebDriverWait(self.driver, 0.1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "next-page"))
            )
            self.click_button(By.CLASS_NAME, "next-page", 0)
            dfs.append(self.make_df())
            if i % 100 == 0:
                print(f"Collected {i} pages")
            if (i % 500 == 0) and save:
                if previous_date is not None:
                    try:
                        path = join(data_path, f'df-{previous_date}.pkl')
                        os.remove(path)
                    except Exception as e:
                        print(f'Unable to delete previous saved file because of: {e}')
                print("Saving data")
                previous_date = datetime.date.today()
                path = join(data_path, f'df-{previous_date}.pkl')
                pickle.dump(pd.concat(dfs), open(path, 'wb'))
        print("Finished data collection")
        return pd.concat(dfs, ignore_index=True).reset_index(drop=True)

    def run(self, save=True):
        # sourcery skip: remove-pass-body, remove-redundant-if
        pages = self.get_page_count()
        df = self.collect_data(pages)
        self.teardown_method()
        df.columns = df.columns.str.replace('  ', ' ')
        df = df.dropna(how='all')
        if save:
            today = datetime.date.today()
            path = join(data_path, f'scraped_data-{today}.csv')
            df.to_csv(path, index=False)
        return df

def main():
    crawler = Crawler()
    try:
        crawler.connect()
    except Exception as e:
        crawler.teardown_method()
        print(e)
        print("Something went wrong, trying again")
        try:
            crawler.connect()
        except Exception as e:
            print(e)
            print("Something went wrong again, try again later")
    return crawler.run()
