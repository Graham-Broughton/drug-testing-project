import pandas as pd
import numpy as np
import re


def opioid_present(col):
    """
    This function uses a list of regex strings to find if any opioids are present in a given column (ftir components).
    """
    opioid_list = ['(despropionyl\s)?(para-fluoro)?(carf|f)entan(i|y)l( base)?', 
                   'heroin',
                   '(hydro|oxy).*one', 
                   'opium', 
                   'w-1(8|9)', 
                   '6-mam', 
                   '.*tazene', 
                   '(code|morph)ine',
                   '(furanyl\s)?uf-17']
    score = sum(
        1 if re.search(item, col, re.IGNORECASE) else 0 for item in opioid_list
    )
    return 1 if score > 0 else 0

def ftir_benzo(col):
    if col == 'Escitalopram': 
        return 0
    else:
        return 1 if re.search(r'[a-z]*[^m]am(?!\w)', col, re.IGNORECASE) else 0