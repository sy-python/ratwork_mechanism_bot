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
        Handles the bot's ready event by verifying the user object and printing login details.
        
        Raises:
            RuntimeError: If the bot's user object is None after login.
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
        Sends a debug message in response to the slash command.
        
        Args:
            ctx: The context of the command invocation.
            message: The message to send as a response.
        """
        await ctx.respond(message)
