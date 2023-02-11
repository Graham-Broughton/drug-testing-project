from multiprocessing import Queue
from datetime import datetime

import os
import sys
# Adds the current directory (project root) to the path so we can import modules "higher up"
sys.path.append(os.getcwd())

import warnings; warnings.simplefilter('ignore')

from src.data.get_data import main
from src.data import process_data
import src.data.get_data_multi as multi
import src.data.get_data as single
from config import CFG

CFG = CFG()

date = datetime.now().strftime("%Y-%m-%d")
current_dir = os.path.abspath(os.getcwd())
data_dir = os.path.join(current_dir, "data_files")
raw_data_path = os.path.join(data_dir, "raw")
page_path = os.path.join(data_dir, "page_data")

CFG.DATE = date
CFG.CURRENT_DIR = current_dir
CFG.DATA_DIR = data_dir
CFG.RAW_DATA_PATH = raw_data_path
CFG.PAGE_PATH = page_path


def main(CFG, multiprocessing=True):
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
    if CFG.SAVE: df.to_csv(f'{CFG.RAW_DATA_PATH}/df-{CFG.DATE}.csv', index=False)
    return df


if __name__ == "__main__":
    CFG.SAVE = False
    df = main(CFG, multiprocessing=True)
    


    