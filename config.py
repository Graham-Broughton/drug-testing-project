import os
from os.path import join


BASEPATH = os.path.realpath(os.path.dirname(__file__))
DATA = join(BASEPATH, join('src', 'data'))
VIZ = join(BASEPATH, join('src', 'visualization'))
DATA_FILES = join(BASEPATH, join('data_files'))

URL = "https://drugcheckingbc.ca/dashboard/"
HEADLESS = False
SEC_WAITING = 40
N_WORKERS = 4
