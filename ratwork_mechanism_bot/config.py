import dotenv

import dataclasses
import os

dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise RuntimeError("Missing environment variable(s)")


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    discord_token: str


config = Config(discord_token=DISCORD_TOKEN)
