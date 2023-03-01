import os

from selenium.webdriver.common.by import By

import sys
sys.path.append('..')
from config import CFG
from src.crawler.CrawlerBase import Crawler
CFG=CFG()


class PageLoader(Crawler):
    def get_page_count(self, pagefile):
        """
        Finds the container holding the last page number and returns it as a string
        """
        pages = self.driver.find_element(By.CLASS_NAME,
            'last-page'
        ).text
        print(f"Page count: {pages}")
        with open(pagefile, 'w') as f:
            f.write(pages)
        return str(pages)

    def load_queue(self, data_queue, pages):
        """
        Loads an instance of multiprocessing.Queue with the listified output obtained from get_page_count
        Args:
            queue: An instance of multiprocessing.Queue
        """
        [data_queue.put(x) for x in range(1, int(pages)+1)]
        data_queue.put("END")
        print("Loaded queue")
        return

    def run(self, data_queue, CFG):
        pagefile = os.path.join(CFG.PAGE_PATH, f"page_count_{CFG.DATE}.txt")
        if os.path.exists(pagefile):
            print("Using saved page count")
            with open(pagefile, 'r') as f:
                pages = f.read()
            self.load_queue(data_queue, pages)
            return
        self.connect()
        pages = self.get_page_count(pagefile)
        self.load_queue(data_queue, pages)
        self.driver.quit()
        return
