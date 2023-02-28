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
from config import CFG


date = datetime(2023, 2, 10).strftime("%Y-%m-%d")
CFG = CFG()
CFG.DATE = date


def get_data(CFG, multiprocessing, save_raw):
    """
    The main entry point of this module, can be run using single or multiprocessing.
    
    Args:
        CFG -> dataclass: All the configuration parameters
        multiprocessing -> bool: Determine if multiprocessing should be used or not
    """
    if not multiprocessing:
        return single.main(CFG)
    DQ, PQ = Queue(), Queue()
    df = multi.main(DQ, PQ, CFG)
    print(df.head())
    if save_raw: df.to_csv(f'{CFG.RAW_DATA_PATH}/df-{CFG.DATE}.csv', index=False)
    return df


if __name__ == "__main__":
    import argparse
    args = argparse.ArgumentParser()
    args.add_argument("--save", '-s', action="store_true", default=False)
    args.add_argument("--save-raw", '-S', action="store_true", default=False)
    args.add_argument("--multiprocessing", "-m", action="store_true", default=True)
    args = args.parse_args()

    df = get_data(CFG, multiprocessing=args.multiprocessing, save_raw=args.save_raw)
    df = process_data(CFG)
    df.to_csv(f'{CFG.PROCESSED_DATA_PATH}/df-{CFG.DATE}.csv', index=False)
    


    