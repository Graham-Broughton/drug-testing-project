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
import threading
import queue

class Pages(queue.Queue):
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue

    def __len__(self):
        return len(self.queue)


def get_page_num(driver, url, sec_wait):
    print("Connecting to Selenium")
    driver.get(url)
    driver.set_window_size(1280, 680)
    time.sleep(sec_wait)
    driver.switch_to.frame(0)
    driver.find_element(By.XPATH, '//*[@id="tab_container"]/li[3]/a').click()
    pages = driver.find_element(By.XPATH,
        '/html/body/div/div/div[3]/div/div/div[3]/div/div/div[2]/div/div/div/div[3]/div/div[2]'
    ).text
    print(f"Found {pages} pages")
    driver.quit()
    return int(pages)


class Crawler():
    def __init__(self, Queue, **kwargs):
        # sourcery skip: remove-pass-body
        self.queue = Queue
        self.url = kwargs['url']
        self.seconds_to_wait = kwargs['sec_wait']
        self.data_file_path = kwargs['data_file_path']

    def teardown_method(self):
        self.driver.quit()

    def connect_multi(self, thread_num):
        print(f"Connecting thread {thread_num} to Selenium")
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.set_window_size(1280, 680)
        time.sleep(self.seconds_to_wait)
        self.driver.switch_to.frame(0)
        self.driver.find_element(By.XPATH, '//*[@id="tab_container"]/li[3]/a').click()
        print(f"Successfully connected thread {thread_num} to Selenium")

    def make_df(self):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table')
        return pd.read_html(str(table))[0]

    def collect_data(self, page=0):
        print("Starting data collection")
        self.driver.find_element(By.CLASS_NAME, "current-page").click()
        self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(str(page))
        self.driver.find_element(By.CLASS_NAME, "current-page").send_keys(Keys.ENTER)
        df = self.make_df()
        print("Finished data collection")
        return df

    def run(self):
        # sourcery skip: remove-pass-body, remove-redundant-if
        while True:
            page = self.queue.get()
            try:
                if page is None:
                    break
                df = self.collect_data(page=page)
            except Exception as e:
                print("Encountered exception: ", e)
            self.queue.task_done()
        self.teardown_method()
        return df


if __name__ == "__main__":
    Q = Pages()
    driver = webdriver.Chrome()
    pages = get_page_num(driver, "https://drugcheckingbc.ca/dashboard/", 40)
    Q.put(pages)
    crawlers =[Crawler(Q, url="https://drugcheckingbc.ca/dashboard/", sec_wait=40, data_file_path="../../data/") for _ in range(2)]
    for crawler in crawlers:
        t = threading.Thread(target=crawler.run)
        t.daemon = True
        t.start()
    Q.join()
