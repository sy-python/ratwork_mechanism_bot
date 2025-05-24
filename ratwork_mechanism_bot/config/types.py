from contextlib import contextmanager
from dataclasses import dataclass
import sqlite3
from typing import Generator, Literal

import discord

from .logger import logger


class BotSetupError(RuntimeError):
    pass


class AbstractRatworkCog(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot


@dataclass(frozen=True, slots=True, kw_only=True)
class Connector:
    database_location: str
    echo_queries: bool

    @contextmanager
    def connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.database_location)
        if self.echo_queries:
            conn.set_trace_callback(logger.debug)
        try:
            with conn:
                yield conn
        finally:
            conn.close()


@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    discord_token: str
    server_id: int
    connector: Connector
    menace_emote_role_map: dict[int, int]
    menace_threshold: int
    environment: Literal["development", "production"]


@dataclass(frozen=True, slots=True, kw_only=True)
class QueryHolder:
    setup: str
    get_reset: str
    update_reset: str
