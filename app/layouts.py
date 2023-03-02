from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

import os
import pandas as pd
import dotenv
dotenv.load_dotenv()

app_name = os.getenv("DASH_APP_PATH", "/app")

df = pd.read_csv("data_files/processed/df-processed-2023-02-10.csv")


# navBar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Geographic", href=f"{app_name}/Geographic", active='exact', external_link=True)),
#         dbc.NavItem(dbc.NavLink("Drug Info", href=f"{app_name}/Drug_Info", active='exact', external_link=True)),
#         dbc.NavItem(dbc.NavLink("Insights", href=f"{app_name}/Insights", active='exact', external_link=True)),
#     ]
#     [
#         dbc.NavItem(dbc.NavLink("Summary", href=f"{app_name}/Summary", active='exact', external_link=True)),
#     ]
# )

navTabs = dbc.Row([
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