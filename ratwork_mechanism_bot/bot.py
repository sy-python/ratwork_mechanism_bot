import discord

from .config import config

from .cogs import cogs


def main():
    """
    Initializes and runs the Discord bot with all registered cogs.
    
    Creates a Discord bot instance, adds each cog from the cogs collection, and starts the bot using the configured Discord token.
    """
    intents = discord.Intents.default()
    bot = discord.Bot(intents=intents)

    for cog in cogs:
        bot.add_cog(cog(bot))

    bot.run(config.discord_token)
