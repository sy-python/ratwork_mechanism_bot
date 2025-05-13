import sys

import discord

from .config import config, logger, BotSetupError
from .cogs import cogs


def main():
    intents = discord.Intents.default()
    bot = discord.Bot(intents=intents)

    for cog in cogs:
        bot.add_cog(cog(bot))

    @bot.event
    async def on_error(event, *args, **kwargs):
        exc_type, exc, tb = sys.exc_info()
        logger.error("Error in event %s", event, exc_info=True)
        if isinstance(exc, BotSetupError):
            await bot.close()

    bot.run(config.discord_token)
