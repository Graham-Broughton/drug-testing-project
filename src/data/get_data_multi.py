from dataclasses import dataclass
import pandas as pd
import time
import datetime
from multiprocessing import Queue, Process, Pipe

import warnings; warnings.simplefilter('ignore')

import os

from src.crawler.PageLoader import PageLoader
import src.crawler.Worker as work

def get_df(data_queue: Queue, page_queue: Queue, CFG: dataclass) -> pd.DataFrame:
    """
    This function takes dfs from the product queue from the workers and appends them into a list,
    every so often it compiles the list into a list of concatenated dfs until the product queue is empty.
    Finally, it returns a concated df from the list. The Queues are needed because we are using multiprocessing,
    they are a method of sharing information between processes. 
    Here, the page queue keeps track of which page number is currently being scraped, allowing us to coordinate the workers.
    The data queue is where the workers put the dfs they scrape, allowing the main process to collect them.
    """
    counter = 0
    dfs = []
    big_dfs = []
    time.sleep(CFG.SEC_HEADSTART)  # Need to give a head start to the workers for them to connect
    while not page_queue.empty():  # While there are still pages to be scraped, keep scraping
        dfs.append(data_queue.get())  # First, list the dfs straight from the queue
        counter += 1
        
        if counter % 250 == 0:
            print(f"Processing {counter}th df. Product queue and data queue are {data_queue.qsize()} and {page_queue.qsize()} long")
            big_dfs.append(pd.concat(dfs, ignore_index=True))  # Second, concatenate the list of dfs and make another list (probably reduntant)
            dfs = []  # Clear the first list for refilling

    # Now that the page queue is empty, we need to make sure that we processed all the data in the data queue
    if not data_queue.empty():
        while not data_queue.empty():
            dfs.append(data_queue.get())
        big_dfs.append(pd.concat(dfs, ignore_index=True))
    return pd.concat(big_dfs, ignore_index=True)

def main(DQ: Queue, PQ: Queue, CFG: dataclass) -> pd.DataFrame:
    """
    Main entry point for the script, organizes the loaders, workers and reciever
    """
    # Get the number of pages needed to be scraped, uses date to check if there is a file already
    loader = PageLoader()
    loader.run(PQ, CFG)

    # Initiate process 'pool' of workers, daemon option runs the in the background so we can use the main process for the reciever
    workers = []
    for _ in range(CFG.NUM_WORKERS):
        conn1, conn2 = Pipe()  # Simple pipe to communicate if the child process was able to connect to website
        worker = Process(target=work.run, args=(DQ, PQ, conn2))
        worker.start()
        resp = conn1.recv()

        # If child process was able to connect, add it to the list of workers, if not then terminate it
        if resp == 1:
            print("Appening worker")
            workers.append(worker)
        else:
            print("Terminating worker")
            worker.terminate()
        conn1.close()
        
    df = get_df(DQ, PQ, CFG)
    print('joining workers')
    for worker in workers:
        worker.join()

    return df


if __name__ == '__main__':
    # Defining required variables and classes
    DQ, PQ = Queue(), Queue()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data_files")
    raw_data_path = os.path.join(data_dir, "raw")
    page_path = os.path.join(data_dir, "page_data")

    # Running the program
    df = main(DQ, PQ, page_path, date)
    print(df.head())
    df.to_csv(raw_data_path + f'/df-{date}.csv', index=False)
