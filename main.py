from src.data.get_data import main
from src.data import process_data
import sys
import os
sys.path.append(os.getcwd())
from config import CFG
CFG = CFG()


if __name__ == "__main__":
    df = main()
    