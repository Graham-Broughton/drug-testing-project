from dash.dependencies import Input, Output
import plotly.graph_objects as go

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

import pandas as pd

from app import app

df = pd.read_csv("data_files/processed/df-processed-2023-02-10.csv")




@app.callback(
    Output("sample-counts", "figure"),
    [Input("sample-type", "value")],
)
def sample_counts(sample_type):
    flitered_df = df.value_counts(sample_type).head(10).sort_values(ascending=False)

    fig1 = go.Figure(go.Bar(
        x=flitered_df.values,
        y=flitered_df.index,
        orientation='h',
    ))
    return fig1


