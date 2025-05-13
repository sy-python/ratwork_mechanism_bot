import dataclasses
import json
import os
import sqlite3

import dotenv

from .queries import SETUP_QUERY

dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
TEST_SERVER_ID = os.getenv("TEST_SERVER_ID", "")
MAIN_SERVER_ID = os.getenv("MAIN_SERVER_ID", "")
DATABASE_LOCATION = os.getenv("DATABASE_LOCATION", "")
MENACE_EMOTE_ROLE_MAP = os.getenv("MENACE_EMOTE_ROLE_MAP", "")
MENACE_THRESHOLD = os.getenv("MENACE_THRESHOLD", "")

required_envars = {
    "DISCORD_TOKEN": DISCORD_TOKEN,
    "TEST_SERVER_ID": TEST_SERVER_ID,
    "MAIN_SERVER_ID": MAIN_SERVER_ID,
    "DATABASE_LOCATION": DATABASE_LOCATION,
    "MENACE_EMOTE_ROLE_MAP": MENACE_EMOTE_ROLE_MAP,
    "MENACE_THRESHOLD": MENACE_THRESHOLD,
}

missing = [var for var, value in required_envars.items() if value == ""]
if missing:
    raise ValueError(f"Missing environment variables: {', '.join(missing)}")

try:
    _TEST_SERVER_ID = int(TEST_SERVER_ID)
except ValueError as e:
    raise ValueError("TEST_SERVER_ID must be an integer") from e

try:
    _MAIN_SERVER_ID = int(MAIN_SERVER_ID)
except ValueError as e:
    raise ValueError("MAIN_SERVER_ID must be an integer") from e

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

try:
    conn = sqlite3.connect(DATABASE_LOCATION)
    with conn:
        conn.executescript(SETUP_QUERY)
except sqlite3.Error as e:
    raise RuntimeError("Database setup failed") from e


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    discord_token: str
    test_server_id: int
    main_server_id: int
    connection: sqlite3.Connection
    menace_emote_role_map: dict[int, int]
    menace_threshold: int


config = Config(
    discord_token=DISCORD_TOKEN,
    test_server_id=_TEST_SERVER_ID,
    main_server_id=_MAIN_SERVER_ID,
    connection=conn,
    menace_emote_role_map=_MENACE_EMOTE_ROLE_MAP_PARSED,
    menace_threshold=_MENACE_THRESHOLD,
)
