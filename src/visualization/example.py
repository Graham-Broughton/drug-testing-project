from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash.dash_table import DataTable
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np


app = Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
data = pd.read_csv('data_files/processed/df-2021-02-10.csv')
