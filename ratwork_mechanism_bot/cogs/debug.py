from .base import AbstractRatworkCog
from ..config import config

import discord


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
        print(f"Logged in as {user} (ID: {user.id})")

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
        await ctx.respond(message)
