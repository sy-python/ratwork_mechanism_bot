import dotenv

import dataclasses
import os

from .logger import logger  # noqa: F401

dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TEST_SERVER_ID = os.getenv("TEST_SERVER_ID")

if not DISCORD_TOKEN or not TEST_SERVER_ID:
    raise RuntimeError("Missing environment variable(s)")


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    discord_token: str
    test_server_id: int


config = Config(
    discord_token=DISCORD_TOKEN,
    test_server_id=int(TEST_SERVER_ID),
)
