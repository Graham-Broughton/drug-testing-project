import pandas as pd
import os
import time
import datetime
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

import sys
sys.path.append('..')
from config import CFG
from src.utils.CrawlerBase import Crawler
CFG=CFG()


class Worker(Crawler):
    def get_from_queue(self, data_queue):
        """
        Gets the next item from the queue and returns it as a string, if the queue is empty, it returns None
        Args:
            queue: An instance of multiprocessing.Queue
        """
        try:
            page = data_queue.get()
        except Exception:
            data_queue.empty()
            print("Queue is empty")
        return str(page)

    def change_page(self, data_queue):
        """
        Gets page number from get_from_queue and enters it into the page box
        Args:
            queue: An instance of multiprocessing.Queue
        """
        page = self.get_from_queue(data_queue)
        page_box = self.driver.find_element(By.CLASS_NAME, "current-page")
        page_box.send_keys(page)
        return page

    def make_df(self):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table')
        return pd.read_html(str(table))[0]

    def collect_data(self, data_queue, product_queue):
        """
        Collects the data from the webpage after changing pages, compiles it into a pd.DataFrame,
        then puts it into the product queue
        """
        print("Starting data collection")
        while True:
            page = self.change_page(data_queue)
            if  page == "END":
                print("Finished collecting data")
                break
            df = self.make_df()
            product_queue.put(df)

def run(data_queue, product_queue):
    """
    Runs the collect_data function
    """
    worker = Worker()
    try:
        worker.connect()
    except Exception as e:
        try:
            worker.connect()
        except Exception:
            del worker
    worker.collect_data(data_queue, product_queue)
