import discord

from .config import config

from .cogs import cogs


def main():
    intents = discord.Intents.default()
    bot = discord.Bot(intents=intents)

    for cog in cogs:
        bot.add_cog(cog(bot))

    bot.run(config.discord_token)
