import pandas as pd
from bs4 import BeautifulSoup
import time
import yaml
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Crawler():
    def __init__(self, url):
        # sourcery skip: remove-pass-body
        self.url = url
        self.connect(self.url)
        self.pages = self.driver.find_element(
            By.XPATH,
            '/html/body/div/div/div[3]/div/div/div[3]/div/div/div[2]/div/div/div/div[3]/div/div[2]'
        ).text

    def connect(self, url):
        print("Connecting to Selenium")
        self.driver = webdriver.Chrome()
        self.driver.get(CFG['URL2'])
        self.driver.set_window_size(1280, 680)
        time.sleep(40)
        self.driver.switch_to.frame(0)
        self.driver.find_element(By.XPATH, '//*[@id="tab_container"]/li[3]/a').click()
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

    def collect_data(self, num_clicks=None, start_page=0):
        print("Starting data collection")
        if num_clicks is None:
            num_clicks = self.pages
        if start_page != 0:
            self.driver.find_element(By.CLASS_NAME, "current-page").click()
            self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(str(start_page))
            self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(Keys.ENTER)
        dfs = [self.make_df()]
        for i in range(num_clicks):
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "next-page"))
            )
            self.click_button(By.CLASS_NAME, "next-page", 0.1)
            dfs.append(self.make_df())
            if i % 100 == 0:
                print(f"Collected {i} pages")
        print("Finished data collection")
        return pd.concat(dfs, ignore_index=True).reset_index(drop=True)

    def run(self, num_clicks=None, num_threads=1, save=True):
        # sourcery skip: remove-pass-body, remove-redundant-if
        if num_threads > 1:
            pass
        else:
            df = self.collect_data(num_clicks)
        self.teardown_method()
        df.columns = df.columns.str.replace('  ', ' ')
        df = df.dropna(how='all')
        if save:
            today = datetime.date.today()
            df.to_csv(f'../../data_files/scraped_data-{today}.csv', index=False)
        return df


if __name__ == "__main__":
    with open("../config.yaml", "r") as f:
        CFG = yaml.safe_load(f)

    Crawler(CFG['URL2']).run()
