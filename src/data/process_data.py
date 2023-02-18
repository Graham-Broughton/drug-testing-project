import pandas as pd
import numpy as np
import os
import warnings; warnings.simplefilter('ignore')


def process_data(CFG):
    """
    Process the raw scraped dataframe: fixing columns, dropping nans, converting to datetime,
    changing strip results to numericand splitting ftir spectrometer column into multiple columns.
    """
    df = pd.read_csv(os.path.join(CFG.RAW_DATA_PATH, f"df-{CFG.DATE}.csv"))
    df.columns = df.columns.str.replace('  ', ' ').str.lower()
    df['visit date'] = pd.to_datetime(df['visit date'])
    df = df.dropna(how='all').reset_index(drop=True)

    # Changing these to numeric allows us to do calculations on them
    df = df.replace({
        "fentanyl strip": {'Neg':-1, np.nan:0, 'Inv':0, 'Pos':1},
        "benzo strip": {'Neg':-1, np.nan:0, 'Inv':0, 'Pos':1},
    })

    # Having a list in a dataframe makes it more challenging to access the data
    ftir = df['ftir spectrometer'].str.split(', ', expand=True).add_prefix('ftir component ')
    df = pd.concat([df, ftir], axis=1).drop('ftir spectrometer', axis=1)
    if CFG.SAVE:
        df.to_csv(os.path.join(CFG.PROCESSED_DATA_PATH, f"df-processed-{CFG.DATE}.csv"), index=False)
    return df
