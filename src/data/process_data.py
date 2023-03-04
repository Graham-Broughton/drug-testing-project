import pandas as pd
import numpy as np

import re
import warnings; warnings.simplefilter('ignore')
# ['trazadone', 'gabapentin', 'Carisoprodol', 'Deschloroetizolam', 'Ghb (wet)', 'Etizolam', 'Bromazolam', 'Zopiclone',
#  'Methaqualone', '1,4-butanediol', 'Zolpidem', 'Xylazine', '4-chloro-deschloroalprazolam', 'Pregabalin', '4-fluorophenibut'
#  'Gbl', '']

def process_colours(df):
    """
    Process colours for use in the sunburst chart
    """
    df['colour2'] = df['colour'].replace(r'([a-zA-Z]+)(\s)\((light|dark)\)', r'\3\2\1', regex=True)
    df['colour2'] = df['colour2'].replace({
        "Purple": '#A020F0',
        "light Brown": "#C4A484",
        "light Green": "#90EE90",
        "Pink": "#FFC0CB",
        "Colourless": "#F8F8FF",
        "White": "#FFFFFF",
        "Black": "#000000",
        "dark Purple": "#301934",
        "Brown": "#964B00",
        "dark Blue": "#00008B",
        "Blue": "#0000FF",
        "light Yellow": "#FFFFE0",
        "light Pink": "#FFB6C1",
        "dark Brown": "#654321",
        "light Grey": "#D3D3D3",
        "dark Pink": "#FF1493",
        "light Blue": "#ADD8E6",
        "light Purple": "#E6E6FA",
        "light Orange": "#FFA07A",
        "light Red": "#FFA07A",
        "dark Orange": "#FF8C00",
        "dark Green": "#006400",
        "dark Grey": "#A9A9A9",
        "dark Red": "#8B0000",
        "dark Yellow": "#FFD700",
        "Other": "#F8F8FF"    
    })
    return df

def opioid_present(col):
    """
    This function uses a list of regex strings to find if any opioids are present in a given column (ftir components).
    """
    return 1 if re.search(
    '(.*an(y|i)l|heroin|(code|morph|buprenorph)ine|(oxy|hydro)(cod|morph)one|.*tazene|opium|(furanyl\s)?uf-17|6-mam|tramadol)',
    col,
    re.IGNORECASE) else 0

def ftir_benzo(col):
    """
    Uses regex to find if any benzos are present in a given column (ftir components).
    It also rejects escitalopram which would otherwise be a match.
    """
    if col == 'Escitalopram': 
        return 0
    else:
        return 1 if re.search(r'[a-z]*[^m]am(?!\w)', col, re.IGNORECASE) else 0

def process_data(df):
    """
    Process the raw scraped dataframe: fixing columns, dropping nans, converting to datetime,
    changing strip results to numeric and splitting ftir spectrometer column into multiple columns.
    It also prepares the data for the dashboard.
    """
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

    df['city'] = df['city'] + ", BC"

    df = process_colours(df)

    return df
