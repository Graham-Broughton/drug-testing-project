import dash_bootstrap_components as dbc

import os
import dotenv
dotenv.load_dotenv()

app_name = os.getenv("DASH_APP_PATH", "/app")


def NavBar():
    navbar = 