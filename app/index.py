import os
import sys

import pandas as pd
import plotly.graph_objects as go

from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from app import app, srv
import dotenv
dotenv.load_dotenv()

df = pd.read_csv("data_files/processed/df-processed-2023-02-10.csv")

app_name = os.getenv("DASH_APP_PATH", "/app")


if __name__ == "__main__":
    app.run_server(debug=True)