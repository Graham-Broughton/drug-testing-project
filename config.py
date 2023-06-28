from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import os

today = datetime.now().strftime("%Y-%m-%d")
# main_path = os.path.abspath(os.path.dirname(__file__))
# data_path = os.path.join(main_path, "data_files")
# raw_data_path = os.path.join(data_path, "raw")
# page_path = os.path.join(data_path, "page_count_data")
# processed_data_path = os.path.join(data_path, "processed")
# dash_app_path = os.path.join(main_path, "app")
PATH = Path.cwd()
DATA = PATH / "data_files"
RAW_DATA = DATA / "raw"
PROCESSED_DATA = DATA / "processed"
PAGE_PATH = DATA / "page_count_data"
DASH_APP = PATH / "app"



@dataclass
class CFG:
    PATH_TO_DRIVER: str = r"/opt/chromedriver"
    URL: str = "https://drugcheckingbc.ca/dashboard/"
    WINDOW_SIZE: tuple = field(default_factory=lambda: (1280, 680))
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    CHROME_OPTS: list = field(default_factory=lambda: ["--start-maximized", "--headless", "--incognito"])
    FIRST_IFRAME_WAIT: int = 30
    SECOND_IFRAME_WAIT: int = 10
    HEROKU_WAIT: int = 10
    REACT_WAIT: int = 10
    RESULT_BUTTON_WAIT: int = 30
    MAX_TRIES: int = 5
    WAIT: int = 60
    NUM_WORKERS: int = 3
    WAIT_INTERVAL: int = 5
    SEC_HEADSTART: int = 60
    USE_OLDER_DATA: bool = True
    MAIN_PATH: Path = PATH
    DATA_PATH: Path = DATA
    RAW_DATA_PATH: Path = RAW_DATA
    PAGE_PATH: Path = PAGE_PATH
    PROCESSED_DATA_PATH: Path = PROCESSED_DATA
    DATE: str = today

    def __post_init__(self):
        self.CHROME_OPTS = self.CHROME_OPTS + [f"user-agent={self.USER_AGENT}"]

@dataclass
class WEB:
    THEME: str = "BOOTSTRAP"
    DASH_APP_PATH: Path = DASH_APP
