from dataclasses import dataclass, field


@dataclass
class CFG:
    URL: str = "https://drugcheckingbc.ca/results/"
    URL2: str = "https://drugcheckingbc.ca/dashboard/"
    WINDOW_SIZE: tuple = field(default_factory=lambda: (1280, 680))
    CHROME_OPTS: list = field(default_factory=lambda: ["--headless", "--disable-gpu",]) 
    MAX_TRIES: int = 5
    WAIT: int = 30
    DATA_PATH: str = field(default=None)
    NUM_WORKERS: int = 5
    