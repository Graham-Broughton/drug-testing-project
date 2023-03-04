import os
import sys
from datetime import date

import callbacks
import dash_bootstrap_components as dbc
import dotenv
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
from utils import date_picker

from app import app, srv

sys.path.append('..')
from config import CFG

CFG = CFG()
CFG.DATE = date(2023, 3, 1)

dotenv.load_dotenv()

df = pd.read_csv(os.path.join(CFG.PROCESSED_DATA_PATH, f"df-processed-{CFG.DATE}.csv"), parse_dates=['visit date'])
categories = df['category'].unique()
cities = df['city'].unique()
sites = df['site'].unique()

app_name = os.getenv("DASH_APP_PATH", "/app")

sidebar = [ #dbc.Col(
    html.H3('Filters'),
    html.Hr(),
    html.P("Filter the data by selecting from various properties"),
    dbc.Nav([
        html.I(className="bi bi-clock"),
        dbc.Label('Select the Date Range:'),
        date_picker('drug-info-date-selector'),
        dcc.Slider(
            df['visit date'].min().year,
            df['visit date'].max().year,
            1,
            value = df['visit date'].max().year,
            id='drug-info-year-slider',
        ),
        html.Br(),
        html.Br(),
        dbc.Label('Select the Category:'),
        dcc.Checklist(
            df['category'].unique().tolist(),
            df['category'].unique().tolist(),
            id='drug-info-category-checklist',
            ),
    ], vertical=True),
]#, className="position-fixed top-0 left-0 bottom-0 w-17 pt-2 pt-1 bg-light", width=3)


mainLayout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H1('British Columbia Illicit Drug Testing'),
            html.H2('Dashboard'),
            html.Hr(),
        ], style={'textAlign': 'center'}),
        html.Br(),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab([
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Choose Date Range:"),
                                    date_picker('summary-date-range'),
                                ]) # width={"size": 12})
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='benzos-in-opioids'),
                                ]),
                                dbc.Col([
                                    dcc.Graph(id='category-piechart'),
                                ]),
                                dbc.Col([
                                    dcc.Graph(id='total-opioids'),
                                ]),
                                dbc.Col([
                                    dcc.Graph(id='total-benzos'),
                                ]),
                            ], className='hstack g-0'),
                        ], lg=12, width={'size': 12}),
                    ]),
                ], label='Summary'),
                
                dbc.Tab([
                    html.Br(),
                    dbc.Col([
                        html.H3('Geographic Representation of the Number of Samples Tested'),
                    ], style={'textAlign': 'center'}),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Select the Date Range:'),
                            date_picker(id='geographic-date-selector'),
                            html.Br(),
                            dcc.RangeSlider(
                                df['visit date'].min().year,
                                df['visit date'].max().year,
                                1,
                                marks={
                                    2018: '2018',
                                    2019: '2019',
                                    2020: '2020',
                                    2021: '2021',
                                    2022: '2022',
                                    2023: '2023'
                                },
                                value = [df['visit date'].min().year, df['visit date'].max().year],
                                id='geography-year-slider',
                            ),
                            html.Br(),
                            dbc.Label('Select the Category:'),
                            dcc.Checklist(
                                df['category'].unique().tolist(),
                                df['category'].unique().tolist(),
                                id='geographic-category-checklist',
                                ),
                        ], lg=3, style={'textAlign': 'center'}),
                        dbc.Col([
                            dcc.Graph(id='geographic-chart'),
                        ]),
                        dbc.Col(lg=1)
                    ]),
                ], label='Geographic'),
                
                dbc.Tab([
                    html.Br(),
                    html.Div([
                        dbc.ListGroup([
                            dbc.ListGroupItem([
                                
                            ]),
                            dbc.ListGroupItem([
                                #dbc.Col([
                                    dcc.Graph(id='unexpected-opioids'),
                                ]),
                            #]),
                            dbc.ListGroupItem([
                                dcc.Graph(id='unexpected-benzos'),
                            ]),
                        ]), # , horizontal=True
                    ]),
                ], label='Drug Info'),
                
                dbc.Tab([
                    html.Br(),
                    
                ], label='Insights'),
            ])
        ])
    ])
])

app.layout = mainLayout

if __name__ == "__main__":
    app.run_server(debug=True)