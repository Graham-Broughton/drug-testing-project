from dataclasses import dataclass, field


@dataclass
class CFG:
    URL: str = "https://drugcheckingbc.ca/results/"
    URL2: str = "https://drugcheckingbc.ca/dashboard/"
    WINDOW_SIZE: tuple = field(default_factory=lambda: (1280, 680))
    CHROME_OPTIONS: list = field(default_factory=lambda: ["--headless", "--disable-gpu"])
    