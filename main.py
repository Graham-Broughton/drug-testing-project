from src.data.get_data import Crawler, main
import sys
import os
sys.path.append(os.getcwd())
from config import CFG
CFG = CFG()

current_dir = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(current_dir, "data_files")

CFG.DATA_PATH = data_path

if __name__ == "__main__":
    df = main(CFG)