import dataclasses
import sqlite3
from typing import Literal

import discord

from .logger import logger


class BotSetupError(RuntimeError):
    pass


class AbstractRatworkCog(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class Connector:
    database_location: str
    echo_queries: bool

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_location)
        if self.echo_queries:
            conn.set_trace_callback(logger.debug)
        return conn


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    discord_token: str
    server_id: int
    connector: Connector
    menace_emote_role_map: dict[int, int]
    menace_threshold: int
    environment: Literal["development", "production"]


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class QueryHolder:
    setup: str
    get_reset: str
    update_reset: str
