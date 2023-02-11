import pandas as pd
import time
import datetime
from multiprocessing import Queue, Process, Pipe

import warnings; warnings.simplefilter('ignore')

import os

from src.crawler.PageLoader import PageLoader
import src.crawler.Worker as work

def get_df(product_queue, data_queue, CFG):
    """
    This function takes dfs from the product queue from the workers and appends them into a list,
    every so often it compiles the list into a list of concatenated dfs until the product queue is empty.
    Finally, it returns a concated df from the list
    """
    counter = 0
    dfs = []
    big_dfs = []
    time.sleep(CFG.SEC_HEADSTART)  # Need to give a head start to the workers for them to connect
    while not data_queue.empty():
        dfs.append(product_queue.get())  # First list of dfs straight from the queue
        counter += 1
        # n_left = data_queue.qsize()
        if counter % 250 == 0:
            print(f"Processing {counter}th df. Product queue and data queue are {product_queue.qsize()} and {data_queue.qsize()} long")
            big_dfs.append(pd.concat(dfs, ignore_index=True))  # Second, concated list of dfs
            dfs = []
    if not product_queue.empty():
        while not product_queue.empty():
            dfs.append(product_queue.get())
        big_dfs.append(pd.concat(dfs, ignore_index=True))
    return pd.concat(big_dfs, ignore_index=True)

def main(DQ, PQ, CFG):
    """
    Main entry point for the script, organizes the loaders, workers and reciever
    """
    # Get the number of pages needed to be scraped, uses date to check if there is a file already
    loader = PageLoader()
    loader.run(DQ, CFG)

    # initiate process 'pool' of workers, daemon option runs the in the background so we don't need another process for the reciever
    workers = []
    for _ in range(CFG.NUM_WORKERS):
        conn1, conn2 = Pipe()
        worker = Process(target=work.run, args=(DQ, PQ, conn2), daemon=True)
        worker.start()
        # time.sleep(CFG.WAIT_INTERVAL)
        resp = conn1.recv()
        if resp == 1:
            print("Appening worker")
            workers.append(worker)
        else:
            print("terminating worker")
            worker.terminate()
        
    df = get_df(PQ, DQ, CFG)
    print('joining workers')
    for worker in workers:
        worker.join()

    return df


if __name__ == '__main__':
    DQ, PQ = Queue(), Queue()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data_files")
    raw_data_path = os.path.join(data_dir, "raw")
    page_path = os.path.join(data_dir, "page_data")
    
    df = main(DQ, PQ, page_path, date)
    print(df.head())
    df.to_csv(raw_data_path + f'/df-{date}.csv', index=False)