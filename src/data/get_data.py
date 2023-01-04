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


class Crawler():
    def __init__(self, **kwargs):
        # sourcery skip: remove-pass-body
        self.url = kwargs['url']
        self.seconds_to_wait = kwargs['sec_wait']
        self.data_file_path = kwargs['data_file_path']

    def connect(self):
        print("Connecting to Selenium")
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.set_window_size(1280, 680)
        time.sleep(self.seconds_to_wait)
        self.driver.switch_to.frame(0)
        self.driver.find_element(By.XPATH, '//*[@id="tab_container"]/li[3]/a').click()
        self.pages = self.driver.find_element(By.XPATH,
            '/html/body/div/div/div[3]/div/div/div[3]/div/div/div[2]/div/div/div/div[3]/div/div[2]'
        ).text
        print("Successfully connected to Selenium")

    def teardown_method(self):
        self.driver.quit()

    def click_button(self, selector, value, sleep_time=0):
        button = self.driver.find_element(selector, value)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(sleep_time)

    def make_df(self):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table')
        return pd.read_html(str(table))[0]

    def collect_data(self, num_clicks=None, start_page=0, save=True):
        previous_date = None
        print("Starting data collection")
        if num_clicks is None:
            num_clicks = int(self.pages) - 1
        if start_page != 0:
            self.driver.find_element(By.CLASS_NAME, "current-page").click()
            self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(str(start_page))
            self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(Keys.ENTER)
        dfs = [self.make_df()]
        for i in range(num_clicks):
            WebDriverWait(self.driver, 5).until(
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

    def run(self, num_clicks=None, save=True):
        # sourcery skip: remove-pass-body, remove-redundant-if
        df = self.collect_data(num_clicks)
        self.teardown_method()
        df.columns = df.columns.str.replace('  ', ' ')
        df = df.dropna(how='all')
        if save:
            today = datetime.date.today()
            path = join(self.data_file_path, f'scraped_data-{today}.csv')
            df.to_csv(path, index=False)
        return df

def main(url, sec_wait, data_file_path):
    crawler = Crawler(url=url, sec_wait=sec_wait, data_file_path=data_file_path)
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

if __name__ == "__main__":
    main()
