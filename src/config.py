import logging
import os

from dotenv import load_dotenv
from rich import print
from rich.panel import Panel

load_dotenv()


class Config:
    DEV = os.getenv("ENVIRONMENT").lower() == "dev"
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")

    CHANNEL_MANNY_ASKAI = 1052270064059039834
    CHANNEL_GLIF_TEST = 1072164461420498974

    if DEV:
        logging.basicConfig(level=logging.DEBUG)

    config_content = "\n".join(
        [
            f"DEV mode: {DEV}",
            f"DISCORD_TOKEN: {DISCORD_TOKEN is not None}",
            f"DATABASE_URL: {DATABASE_URL is not None}",
        ]
    )
    print(Panel(config_content, title="Config", style="bold blue"))
