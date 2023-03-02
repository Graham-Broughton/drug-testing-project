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


@app.callback(
    Output(),
    Input()
)
def category_piechart():
    fig = go.Figure(go.Pie(
        labels=df.category.value_counts().index,
        values=df.category.value_counts().values,
        hole=0.65
    ))
    fig.update_traces(hoverinfo='value+percent', textinfo='label', textfont_size=20,
                    marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        annotations=[
            dict(text="Categories", x=0.5, y=0.5, font_size=20, showarrow=False)
        ]
    )