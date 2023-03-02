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

mainLayout = html.Div([
    dbc.Row([
    dbc.Col([
        dbc.Tabs([
            dbc.Tab([
                html.Br(),
                dcc.Graph(id='all-samples'),
            ], label='Summary'),
            dbc.Tab([
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dcc.Label('Select the Year(s):'),
                        dcc.Slider(2018, 2023, 1 ,value=2022,
                                id='geographic-year-slider',)
                    ]),
                ]),
                dbc.Graph(id='geographic'),
            ], label='Geographic'),
            dbc.Tab([
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Selectors')
                    ]),
                    
                ])
                
            ])
        ])
    
])


if __name__ == "__main__":
    app.run_server(debug=True)