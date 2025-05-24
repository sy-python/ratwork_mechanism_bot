import json
import os
import sqlite3

import dotenv

from .queries import SETUP_QUERY
from .types import Config, Connector

dotenv.load_dotenv(override=True)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
SERVER_ID = os.getenv("SERVER_ID", "")
DATABASE_LOCATION = os.getenv("DATABASE_LOCATION", "")
MENACE_EMOTE_ROLE_MAP = os.getenv("MENACE_EMOTE_ROLE_MAP", "")
MENACE_THRESHOLD = os.getenv("MENACE_THRESHOLD", "")
ENVIRONMENT = os.getenv("ENVIRONMENT", "")

required_envars = {
    "DISCORD_TOKEN": DISCORD_TOKEN,
    "SERVER_ID": SERVER_ID,
    "DATABASE_LOCATION": DATABASE_LOCATION,
    "MENACE_EMOTE_ROLE_MAP": MENACE_EMOTE_ROLE_MAP,
    "MENACE_THRESHOLD": MENACE_THRESHOLD,
    "ENVIRONMENT": ENVIRONMENT,
}

missing = [var for var, value in required_envars.items() if value == ""]
if missing:
    raise ValueError(f"Missing environment variables: {', '.join(missing)}")

try:
    _SERVER_ID = int(SERVER_ID)
except ValueError as e:
    raise ValueError("SERVER_ID must be an integer") from e

try:
    _MENACE_EMOTE_ROLE_MAP = json.loads(MENACE_EMOTE_ROLE_MAP)
    if not isinstance(_MENACE_EMOTE_ROLE_MAP, dict):
        raise ValueError("MENACE_EMOTE_ROLE_MAP must be a mapping")
    bad_keys = []
    bad_values = []
    _MENACE_EMOTE_ROLE_MAP_PARSED = {}
    for key, value in _MENACE_EMOTE_ROLE_MAP.items():
        try:
            key = int(key)
        except ValueError:
            bad_keys.append(key)
        if not isinstance(value, int):
            bad_values.append(value)
        _MENACE_EMOTE_ROLE_MAP_PARSED[key] = value
    if bad_keys or bad_values:
        suffix = ""
        if bad_keys:
            suffix += f"Bad keys: {', '.join(map(str, bad_keys))}. "
        if bad_values:
            suffix += f"Bad values: {', '.join(map(str, bad_values))}."
        raise ValueError(
            f"Keys and values of MENACE_EMOTE_ROLE_MAP must be integers. {suffix}"
        )

except json.JSONDecodeError as e:
    raise ValueError("MENACE_EMOTE_ROLE_MAP must be a valid JSON object") from e

try:
    _MENACE_THRESHOLD = int(MENACE_THRESHOLD)
except ValueError as e:
    raise ValueError("MENACE_THRESHOLD must be an integer") from e

if ENVIRONMENT not in ("development", "production"):
    raise ValueError("ENVIRONMENT must be development or production")

connector = Connector(
    database_location=DATABASE_LOCATION,
    echo_queries=False,
)

config = Config(
    discord_token=DISCORD_TOKEN,
    server_id=_SERVER_ID,
    connector=connector,
    menace_emote_role_map=_MENACE_EMOTE_ROLE_MAP_PARSED,
    menace_threshold=_MENACE_THRESHOLD,
    environment=ENVIRONMENT,
)


try:
    with connector.connection() as conn:
        conn.executescript(SETUP_QUERY)
except sqlite3.Error as e:
    raise RuntimeError("Database setup failed") from e
