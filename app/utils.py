import pandas as pd
import numpy as np
import re


def opioid_present(col):
    """
    This function uses a list of regex strings to find if any opioids are present in a given column (ftir components).
    """
    return 1 if re.search(
    '(.*an(y|i)l|heroin|(code|morph|buprenorph)ine|(oxy|hydro)(cod|morph)one|.*tazene|w-1(8|9)|opium|(furanyl\s)?uf-17|6-mam)',
    col,
    re.IGNORECASE) else 0

def ftir_benzo(col):
    if col == 'Escitalopram': 
        return 0
    else:
        return 1 if re.search(r'[a-z]*[^m]am(?!\w)', col, re.IGNORECASE) else 0