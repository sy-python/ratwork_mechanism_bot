import logging

import discord

from .base import AbstractRatworkCog
from ..config import config

logger = logging.getLogger("ratwork_mechanism_bot")


class DebugCog(AbstractRatworkCog):
    """
    A cog for debugging purposes.
    """

    @discord.Cog.listener(once=True)
    async def on_ready(self):
        """
        Called when the bot is ready.
        """
        user = self.bot.user
        if user is None:
            raise RuntimeError("User is None after login")
        logger.info(f"Logged in as {user} (ID: {user.id})")

    @discord.slash_command(
        name="debug", description="Debug command", guild_ids=[config.test_server_id]
    )
    @discord.option(
        name="message",
        description="Message to send",
        required=True,
        default="Debug message",
    )
    async def debug(self, ctx: discord.ApplicationContext, message: str) -> None:
        """
        Debug command.
        """
        logger.info('Debug command called with message: "%s"', message)
        await ctx.respond(message)
