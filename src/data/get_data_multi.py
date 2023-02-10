import pandas as pd
import time
import datetime
import pickle
from multiprocessing import Queue, Pool, Process

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

import warnings; warnings.simplefilter('ignore')

import os
import sys
sys.path.append(os.getcwd())
from config import CFG

CFG=CFG()

from src.utils.PageLoader import PageLoader
import src.utils.Worker as work

def get_df(product_queue):
    counter = 0
    dfs = []
    big_dfs = []
    time.sleep(180)
    while not product_queue.empty():
        dfs.append(product_queue.get())
        counter += 1
        if counter % 250:
            print(f"Processing {counter}th df")
            big_dfs.append(pd.concat(dfs, ignore_index=True))
            dfs = []
    return pd.concat(big_dfs, ignore_index=True)

def main(page_path, date):
    """
    Main entry point for the script, call
    """
    DQ, PQ = Queue(), Queue()
    
    loader = PageLoader()
    loader.run(DQ, page_path, date)

    workers = []
    for _ in range(CFG.NUM_WORKERS):
        worker = Process(target=work.run, args=(DQ, PQ), daemon=True)
        worker.start()
        workers.append(worker)

    df = get_df(PQ)

    for worker in workers:
        worker.join()

    return df


if __name__ == '__main__':
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data_files")
    page_path = os.path.join(data_dir, "page_data")
    
    df = main(page_path, date)
    print(df.head())
    df.to_csv(data_dir + '/data.csv', index=False)