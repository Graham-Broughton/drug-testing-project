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
categories = df['category'].unique()
cities = df['city'].unique()
sites = df['site'].unique()

app_name = os.getenv("DASH_APP_PATH", "/app")

mainLayout = html.Div([
    dbc.Col([
        html.Br(),
        html.H1('British Columbia Illicit Drug Testing'),
        html.H2('Dashboard'),
    ], style={'textAlign': 'center'}),
    html.Br(),
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
                            dbc.Label('Select the Year(s):'),
                            dcc.Slider(2018, 2023, 1 ,value=2022,
                                    id='geographic-year-slider',)
                        ]),
                    ]),
                    dcc.Graph(id='geographic-chart'),
                ], label='Geographic'),
                dbc.Tab([
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Selectors')
                        ]),                    
                    ])                
                ], label='Drug Info'),
                dbc.Tab([
                    html.Br(),
                    
                ])
            ])
        ])
    ])
])

app.layout = mainLayout

if __name__ == "__main__":
    app.run_server(debug=True)