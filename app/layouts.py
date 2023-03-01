from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

import os
import pandas as pd
import dotenv
dotenv.load_dotenv()

app_name = os.getenv("DASH_APP_PATH", "/app")

df = pd.read_csv("data_files/processed/df-processed-2023-02-10.csv")


appMenu = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Summary", href=f"{app_name}/Summary", active='exact', external_link=True)),
        dbc.NavItem(dbc.NavLink("Geographic", href=f"{app_name}/Geographic", active='exact', external_link=True)),
        dbc.NavItem(dbc.NavLink("Drug Info", href=f"{app_name}/Drug_Info", active='exact', external_link=True)),
        dbc.NavItem(dbc.NavLink("Insights", href=f"{app_name}/Insights", active='exact', external_link=True)),
    ]
)