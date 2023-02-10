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

CFG = CFG()


class Crawler():
    def __init__(self, CFG):
        # sourcery skip: remove-pass-body
        self.url = CFG.URL2
        self.seconds_to_wait = CFG.WAIT
        self.data_file_path = CFG.DATA_PATH
        self.window_size = CFG.WINDOW_SIZE

    def connect(self):
        print("Connecting to Selenium")
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.set_window_size(self.window_size[0], self.window_size[1])
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
        # if num_clicks is None:
        #     num_clicks = int(self.pages) - 1
        if start_page != 0:
            self.driver.find_element(By.CLASS_NAME, "current-page").click()
            self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(str(start_page))
            self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(Keys.ENTER)
        dfs = [self.make_df()]
        for i in range(1, int(pages)+1):
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
                        path = join(self.data_file_path, f'df_lists-{previous_date}.pkl')
                        os.remove(path)
                    except Exception as e:
                        print(f'Unable to delete previous saved file because of: {e}')
                print("Saving data")
                previous_date = datetime.date.today()
                path = join(self.data_file_path, f'df_lists-{previous_date}.pkl')
                pickle.dump(dfs, open(path, 'wb'))
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
            path = join(self.data_file_path, f'scraped_data-{today}.csv')
            df.to_csv(path, index=False)
        return df

def main(CFG):
    crawler = Crawler(CFG)
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
