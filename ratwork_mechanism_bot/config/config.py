import dotenv

import dataclasses
import os

dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
TEST_SERVER_ID = os.getenv("TEST_SERVER_ID", "")

required_envars = {
    "DISCORD_TOKEN": DISCORD_TOKEN,
    "TEST_SERVER_ID": TEST_SERVER_ID,
}

missing = [var for var, value in required_envars.items() if value == ""]
if missing:
    raise ValueError(f"Missing environment variables: {', '.join(missing)}")

try:
    _TEST_SERVER_ID = int(TEST_SERVER_ID)
except ValueError as e:
    raise ValueError("TEST_SERVER_ID must be an integer") from e


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    discord_token: str
    test_server_id: int


config = Config(
    discord_token=DISCORD_TOKEN,
    test_server_id=_TEST_SERVER_ID,
)
