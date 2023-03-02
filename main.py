from multiprocessing import Queue
from datetime import datetime

import os
import sys
# Adds the current directory (project root) to the path so we can import modules "higher up"
sys.path.append(os.getcwd())

import warnings; warnings.simplefilter('ignore')

from src.data.process_data import process_data
import src.data.get_data_multi as multi
import src.data.get_data as single
from src.crawler.PageLoader import PageLoader
from config import CFG


date = datetime.now().strftime("%Y-%m-%d")
CFG = CFG()
# CFG.DATE = date  ## in case you want to change the date


def get_last_page_count(CFG):
    """
    Retrieves the last page count from the page_count.txt file"""
    page_list = os.listdir(CFG.PAGE_PATH)
    new_page_list = [x.split('.')[0].split('_')[-1] for x in page_list]
    new_page_list.sort()
    most_recent_date = new_page_list[-1]
    CFG.LAST_DATE = most_recent_date
    
    last_page_count_file = os.path.join(CFG.PAGE_PATH, f"page_count_{most_recent_date}.txt")
    with open(last_page_count_file, 'r') as f:
        last_page_count = f.read()
        CFG.PAGE_COUNT = last_page_count
        
    return last_page_count, most_recent_date

def get_data(CFG, multiprocessing, save_raw):
    """
    The main entry point of this module, can be run using single or multiprocessing.
    
    Args:
        CFG -> dataclass: All the configuration parameters
        multiprocessing -> bool: Determine if multiprocessing should be used or not
    """
    last_page_count, last_date = get_last_page_count(CFG)

    Pages = PageLoader()
    Pages.connect()
    new_page_count = Pages.get_page_count()
    CFG.NEW_PAGE_COUNT = new_page_count

    if str(new_page_count) == str(last_page_count):
        print("No change since last scraping, renaming dataframe to current date")
        os.rename(
            os.path.join(CFG.PROCESSED_DATA_PATH, f"df-processed-{last_date}.csv"), 
            os.path.join(CFG.PROCESSED_DATA_PATH, f"df-processed-{CFG.DATE}.csv")
        )
        sys.exit("Data up to date")
    
    if not multiprocessing:
        print("Using single process to scrape")
        df = single.main(CFG)
        df.to_csv(f'{CFG.RAW_DATA_PATH}/df-{CFG.DATE}.csv', index=False)
        return df
        
    print("Using multiprocessing to scrape")
    DQ, PQ = Queue(), Queue()
    df = multi.main(DQ, PQ, CFG)
    df.to_csv(f'{CFG.RAW_DATA_PATH}/df-{CFG.DATE}.csv', index=False)
    return df


if __name__ == "__main__":
    import argparse
    args = argparse.ArgumentParser()
    args.add_argument("--save", '-s', action="store_true", default=False)
    args.add_argument("--save-raw", '-S', action="store_true", default=False)
    args.add_argument("--multiprocessing", "-m", action="store_true", default=False)
    args.add_argument("--new-dataframe", "-n", action="store_true", default=False)
    args = args.parse_args()

    CFG.NEW_DATAFRAME = args.new_dataframe

    df = get_data(CFG, multiprocessing=args.multiprocessing, save_raw=args.save_raw)
    df = process_data(df)
    if args.save: df.to_csv(f'{CFG.PROCESSED_DATA_PATH}/df-processed-{CFG.DATE}.csv', index=False)
    


    