import pandas as pd
import numpy as np
import os
import re
import warnings; warnings.simplefilter('ignore')


def opioid_present(col):
    """
    This function uses a list of regex strings to find if any opioids are present in a given column (ftir components).
    """
    return 1 if re.search(
    '(.*an(y|i)l|heroin|(code|morph|buprenorph)ine|(oxy|hydro)(cod|morph)one|.*tazene|w-1(8|9)|opium|(furanyl\s)?uf-17|6-mam|tramadol)',
    col,
    re.IGNORECASE) else 0

def ftir_benzo(col):
    if col == 'Escitalopram': 
        return 0
    else:
        return 1 if re.search(r'[a-z]*[^m]am(?!\w)', col, re.IGNORECASE) else 0

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
    ftirs = [x for x in df.columns.tolist() if x.startswith('ftir')]
    for col in ftirs:
        df[col] = df[col].astype(str)

    # This is a list of regex strings that will be used to find if any opioids are present in a given column (ftir components).
    opioids = df.loc[:, ftirs].applymap(lambda x: opioid_present(x))
    opioids = opioids.apply(sum, axis=1).astype(bool).astype(int)
    df['contains_opioids'] = opioids

    df['total_opioids'] = np.where((df['contains_opioids'] == 1) | (df['fentanyl strip'] == 1), 1, 0)

    # This is a list of regex strings that will be used to find if any benzos are present in a given column (ftir components).
    benzos = df.loc[:, ftirs].applymap(lambda x: ftir_benzo(x))
    benzos = benzos.apply(sum, axis=1).astype(bool).astype(int)
    df['ftir_benzo'] = benzos

    df['total_benzos'] = np.where((df['ftir_benzo'] == 1) | (df['benzo strip'] == 1), 1, 0)

    return df
