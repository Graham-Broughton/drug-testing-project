import pandas as pd
import time
import datetime
from multiprocessing import Queue, Pool, Process

import warnings; warnings.simplefilter('ignore')

import os
import sys
sys.path.append(os.getcwd())
from config import CFG

CFG=CFG()

from src.utils.PageLoader import PageLoader
import src.utils.Worker as work

def get_df(product_queue, data_queue):
    """
    This function takes dfs from the product queue from the workers and appends them into a list,
    every so often it compiles the list into a list of concatenated dfs until the product queue is empty.
    Finally, it returns a concated df from the list
    """
    counter = 0
    dfs = []
    big_dfs = []
    time.sleep(CFG.SEC_HEADSTART)  # Need to give a head start to the workers for them to connect
    while (not product_queue.empty()) & (not data_queue.empty()):
        dfs.append(product_queue.get())  # First list of dfs straight from the queue
        counter += 1
        if counter % 250 == 0:
            print(f"Processing {counter}th df")
            big_dfs.append(pd.concat(dfs, ignore_index=True))  # Second, concated list of dfs
            dfs = []
    return pd.concat(big_dfs, ignore_index=True)

def main(page_path, date):
    """
    Main entry point for the script, organizes the loaders, workers and reciever
    """
    # start the Queues in parent process for communication between processes, otherwise it wont work
    DQ, PQ = Queue(), Queue()

    # Get the number of pages needed to be scraped, uses date to check if there is a file already
    loader = PageLoader()
    loader.run(DQ, page_path, date)

    # initiate process 'pool' of workers, daemon option runs the in the background so we don't need another process for the reciever
    workers = []
    for _ in range(CFG.NUM_WORKERS):
        worker = Process(target=work.run, args=(DQ, PQ), daemon=True)
        worker.start()
        workers.append(worker)

    df = get_df(PQ, DQ)

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