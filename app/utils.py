import os
import sys
from datetime import date

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dcc, html

sys.path.append('..')
from config import CFG

CFG = CFG()
CFG.DATE = date(2023, 3, 1)

df = pd.read_csv(os.path.join(CFG.PROCESSED_DATA_PATH, f"df-processed-{CFG.DATE}.csv"), parse_dates=['visit date'])


def date_picker(id):
    return dcc.DatePickerRange(
        min_date_allowed=df['visit date'].min().date(),
        max_date_allowed=df['visit date'].max().date(),
        initial_visible_month=df['visit date'].min().date(),
        end_date=df['visit date'].max().date(),
        start_date=df['visit date'].min().date(),
        id=id
    )