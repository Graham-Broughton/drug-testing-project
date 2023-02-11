import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

import sys
sys.path.append('..')
from config import CFG
from src.crawler.CrawlerBase import Crawler
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
        page_box = WebDriverWait(self.driver, CFG.RESULT_BUTTON_WAIT).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "current-page"))
            )
        page_box.send_keys(page)
        page_box.send_keys(Keys.RETURN)
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
        while not data_queue.empty():
            page = self.change_page(data_queue)
            if  page == "END":
                print("Finished collecting data")
                break
            df = self.make_df()
            product_queue.put(df)
        return

def run(data_queue, product_queue, conn):
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
            conn.send(0)
    else:
        conn.send(1)
        worker.collect_data(data_queue, product_queue)
    return
