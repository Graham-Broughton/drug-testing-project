import src.data.get_data as gd
import pandas as pd
import config

def get_data():
    df = gd.main(
        url=config.URL,
        sec_wait=config.SECONDS_TO_WAIT,
        data_file_path=config.DATA_FILE_PATH
    )
    return df

