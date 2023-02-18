from dataclasses import dataclass, field
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")


@dataclass
class CFG:
    PATH_TO_DRIVER: str = r"C:\\Users\\broug\\chromedriver.exe"
    URL: str = "https://drugcheckingbc.ca/dashboard/"
    WINDOW_SIZE: tuple = field(default_factory=lambda: (1280, 680))
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    CHROME_OPTS: list = field(default_factory=lambda: ["--start-maximised", "--headless"])
    FIRST_IFRAME_WAIT: int = 30
    SECOND_IFRAME_WAIT: int = 10
    HEROKU_WAIT: int = 10
    REACT_WAIT: int = 10
    RESULT_BUTTON_WAIT: int = 30
    MAX_TRIES: int = 5
    WAIT: int = 60
    DATA_PATH: str = field(default=None)
    NUM_WORKERS: int = 5
    WAIT_INTERVAL: int = 5
    SEC_HEADSTART: int = 30
    DATE: str = str(today)
    SAVE: bool = True
    USE_OLDER_DATA: bool = True

    def __post_init__(self):
        self.CHROME_OPTS = self.CHROME_OPTS + [f"user-agent={self.USER_AGENT}"]
    